# Pipeline completo: HDFS -> MapReduce -> Spark -> CSV para Power BI
# Uso: powershell -ExecutionPolicy Bypass -File scripts\run_pipeline.ps1

$ErrorActionPreference = "Continue"
$proyecto = Split-Path -Parent $PSScriptRoot
Set-Location $proyecto

Write-Host "1) Levantando el cluster..." -ForegroundColor Cyan
docker compose up -d | Out-Null

Write-Host "   Esperando NameNode healthy..."
$intentos = 0
while ((docker inspect --format '{{.State.Health.Status}}' namenode 2>$null) -ne "healthy" -and $intentos -lt 40) {
    Start-Sleep -Seconds 3
    $intentos++
}
if ($intentos -ge 40) { Write-Host "NameNode no quedo healthy" -ForegroundColor Red; exit 1 }

Write-Host "2) Ingesta a HDFS (estructurado y no estructurado)..." -ForegroundColor Cyan
docker exec namenode hdfs dfs -mkdir -p /data/raw | Out-Null
docker exec namenode hdfs dfs -put -f /data/ventas.csv /data/raw/ventas.csv | Out-Null
docker exec namenode hdfs dfs -put -f /data/comentarios.txt /data/raw/comentarios.txt | Out-Null

Write-Host "3) MapReduce: total por producto..." -ForegroundColor Cyan
docker exec namenode hdfs dfs -rm -r -f /data/ventas_por_producto_mr | Out-Null
docker exec namenode bash -c "mkdir -p /tmp/mr-classes; javac -classpath `$(hadoop classpath) -d /tmp/mr-classes /data/mapreduce/VentaTotal.java && jar cf /tmp/venta-total.jar -C /tmp/mr-classes . && hadoop jar /tmp/venta-total.jar VentaTotal /data/raw/ventas.csv /data/ventas_por_producto_mr" 2>&1 | Select-String -Pattern "completed successfully|FAILED|Error:"

Write-Host "4) Spark: filtro > 100 y agregados..." -ForegroundColor Cyan
docker exec spark-master /spark/bin/spark-submit --master spark://spark-master:7077 /jobs/01_filtro_ventas.py 2>&1 | Select-String -Pattern "Total de registros|Registros con monto"
docker exec spark-master /spark/bin/spark-submit --master spark://spark-master:7077 /jobs/02_resumen_ventas.py 2>&1 | Select-String -Pattern "Ventas por producto|Ventas por cliente|Resumen general"
docker exec spark-master /spark/bin/spark-submit --master spark://spark-master:7077 /jobs/03_conteo_palabras.py 2>&1 | Out-Null

Write-Host "5) Exportando resultados a powerbi\..." -ForegroundColor Cyan
docker exec namenode bash -c "hdfs dfs -get -f /data/analitica/ventas_por_producto/part-* /powerbi/ventas_por_producto.csv; hdfs dfs -get -f /data/analitica/ventas_por_cliente/part-* /powerbi/ventas_por_cliente.csv; hdfs dfs -get -f /data/analitica/ventas_por_mes/part-* /powerbi/ventas_por_mes.csv; hdfs dfs -get -f /data/analitica/resumen_general/part-* /powerbi/resumen_general.csv; hdfs dfs -get -f /data/analitica/palabras_comentarios/part-* /powerbi/palabras_comentarios.csv; rm -rf /powerbi/ventas_altas_parts; hdfs dfs -get /data/ventas_altas /powerbi/ventas_altas_parts; hdfs dfs -getmerge /data/ventas_por_producto_mr /powerbi/ventas_por_producto_mr_raw.tsv"

# Une los part-* de ventas_altas en un solo CSV con una unica cabecera
$dir = Join-Path $proyecto "powerbi"
$parts = Get-ChildItem "$dir\ventas_altas_parts\part-*" | Sort-Object Name
$lineas = New-Object System.Collections.Generic.List[string]
$header = $null
foreach ($p in $parts) {
    $l = Get-Content $p.FullName
    if ($null -eq $header) { $header = $l[0]; $lineas.Add($header) }
    if ($l.Count -gt 1) { $lineas.AddRange([string[]]$l[1..($l.Count - 1)]) }
}
Set-Content "$dir\ventas_altas.csv" $lineas -Encoding UTF8
Remove-Item "$dir\ventas_altas_parts" -Recurse -Force

# Convierte la salida de MapReduce (TSV) a CSV
$mr = New-Object System.Collections.Generic.List[string]
$mr.Add("Producto,Total,Ventas")
Get-Content "$dir\ventas_por_producto_mr_raw.tsv" | ForEach-Object {
    if ($_.Trim()) { $c = $_ -split "`t"; $mr.Add("$($c[0]),$($c[1]),$($c[2])") }
}
Set-Content "$dir\ventas_por_producto_mr.csv" $mr -Encoding UTF8
Remove-Item "$dir\ventas_por_producto_mr_raw.tsv" -Force -ErrorAction SilentlyContinue

Write-Host "6) Generando dashboard..." -ForegroundColor Cyan
python (Join-Path $proyecto "scripts\generar_dashboard.py")
Start-Process (Join-Path $dir "dashboard.html")

Write-Host "Listo. NameNode: http://localhost:9870 | YARN: http://localhost:8088 | Spark: http://localhost:8080" -ForegroundColor Green

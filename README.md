# Caso práctico — Hadoop 3 + Spark en Docker + Power BI

Arquitectura OpenSource para Big Data: **Spark sobre HDFS → ventas filtradas → Power BI**.

## Escenario

Analista de datos que procesa las ventas de una tienda, filtra las compras con
monto superior a **$100**, guarda el resultado en HDFS y lo consulta desde
Spark, la interfaz web del NameNode y Power BI.

Datos de prueba (5 registros):

| Cliente | Producto | Monto |
|---|---|---|
| Carlos | Laptop | 1200 |
| Ana | Mouse | 25 |
| Beatriz | Monitor | 300 |
| David | Teclado | 45 |
| Elena | Celular | 800 |

Resultado: 3 ventas superiores a $100 → **$2,300**.

## Componentes

| Servicio | Imagen | Puerto | Interfaz |
|---|---|---|---|
| namenode | bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8 | 9870 / 9000 | http://localhost:9870 |
| datanode | bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8 | 9864 | http://localhost:9864 |
| resourcemanager | bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8 | 8088 | http://localhost:8088 |
| nodemanager | bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8 | - | (YARN) |
| spark-master | bde2020/spark-master:3.0.0-hadoop3.2 | 8080 / 7077 | http://localhost:8080 |
| spark-worker | bde2020/spark-worker:3.0.0-hadoop3.2 | 8081 | http://localhost:8081 |

Red propia `hadoop-spark-net`; volúmenes `hadoop_namenode` y `hadoop_datanode`.

## Puesta en marcha

```powershell
cd C:\hadoop-spark-cluster
docker compose up -d
docker compose ps
```

## Ejecutar el caso práctico

```powershell
docker exec -it spark-master /spark/bin/pyspark --master spark://spark-master:7077
```

En la consola `>>>`:

```python
ventas = [
    ("Carlos", "Laptop", 1200),
    ("Ana", "Mouse", 25),
    ("Beatriz", "Monitor", 300),
    ("David", "Teclado", 45),
    ("Elena", "Celular", 800),
]
columnas = ["Cliente", "Producto", "Monto"]
df_ventas = spark.createDataFrame(ventas, columnas)

df_filtrado = df_ventas.filter(df_ventas.Monto > 100)
df_filtrado.show()

df_filtrado.write.mode("overwrite").option("header", "true") \
    .csv("hdfs://namenode:9000/data/ventas_altas")
```

## Verificación

- NameNode: http://localhost:9870 → *Utilities → Browse the file system* → `/data/ventas_altas`
  (`_SUCCESS` y `part-*.csv`).
- YARN: http://localhost:8088 → *All Applications*.
- Spark: http://localhost:8080 → maestro `ALIVE`, 1 worker.
- Dashboard web: `powerbi/dashboard.html`.
- Power BI: `powerbi/Dashboard_Ventas.pbix` (tarjeta de total, columnas por
  cliente y tabla de detalle).

## Documentación

`Informe_Caso_Practico.docx` contiene una captura y descripción de cada paso,
desde la terminal de PySpark hasta el informe final de Power BI.

## Estructura

```
├── docker-compose.yml        # 6 servicios propios
├── hadoop.env                # variables Hadoop/YARN
├── Informe_Caso_Practico.docx
├── data/                     # datos e intermediarios HDFS
├── evidencias/               # capturas del caso práctico (cp01–cp09)
├── jobs/                     # jobs Spark / MapReduce
├── powerbi/                  # CSV, Dashboard_Ventas.pbix, dashboard.html
├── scripts/                  # scripts de ejecución y construcción
└── tools/                    # utilidades de automatización
```

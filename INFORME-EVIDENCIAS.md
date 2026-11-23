# Evidencias del proyecto - Hadoop 3 y Spark en Docker

Fecha de ejecucion: 23/11/2026. Proyecto: `C:\hadoop-spark-cluster` (nuevo, red y volumenes propios).

## 1. Cluster

6 contenedores propios sobre `hadoop-spark-net`:

| Contenedor | Imagen | Puerto | Estado |
|---|---|---|---|
| namenode | bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8 | 9870 / 9000 | healthy |
| datanode | bde2020/hadoop-datanode:2.0.0-hadoop3.2.1-java8 | 9864 | healthy |
| resourcemanager | bde2020/hadoop-resourcemanager:2.0.0-hadoop3.2.1-java8 | 8088 | healthy |
| nodemanager | bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8 | - | healthy |
| spark-master | bde2020/spark-master:3.0.0-hadoop3.2 | 8080 / 7077 | up |
| spark-worker | bde2020/spark-worker:3.0.0-hadoop3.2 | 8081 | up |

## 2. Interfaces web (capturas en `evidencias/`)

| Captura | URL | Que se observa |
|---|---|---|
| `namenode.png` | http://localhost:9870 | Hadoop 3.2.1, `hdfs://namenode:9000` activo, 1 Live Node, 1,43 MB usados, 50 bloques |
| `yarn.png` | http://localhost:8088 | 1 nodo activo, Capacity Scheduler, 1 aplicacion `FINISHED / SUCCEEDED` |
| `spark.png` | http://localhost:8080 | `Status: ALIVE`, 1 worker con 1 core y 1024 MiB, 3 aplicaciones completadas |
| `datanode.png` | http://localhost:9864 | DataNode activo y registrado |
| `dashboard.png` | `powerbi/dashboard.html` | KPIs, ventas por producto/cliente/mes y validacion MapReduce |

## 3. Ingesta (ETL estructurado + ELT no estructurado)

| Archivo local | Destino HDFS | Tamano |
|---|---|---|
| `data/ventas.csv` (245 filas, 8 columnas) | `/data/raw/ventas.csv` | 10,9 KB |
| `data/comentarios.txt` (96 lineas) | `/data/raw/comentarios.txt` | 5,9 KB |

## 4. Procesamiento

**MapReduce (Java, YARN)** - `VentaTotal.java`: total y numero de ventas por producto.
Salida: `/data/ventas_por_producto_mr` (job `FINISHED / SUCCEEDED`).

**Spark 3.0 (PySpark)**:
- `01_filtro_ventas.py`: 245 leidos -> 164 con `Monto > 100` -> `/data/ventas_altas`
- `02_resumen_ventas.py`: agregados -> `/data/analitica/*`
- `03_conteo_palabras.py`: ELT de comentarios -> `/data/analitica/palabras_comentarios`

## 5. Resultados

| Metrica | Valor |
|---|---|
| Ventas totales | $107.685,00 |
| Transacciones | 245 |
| Ticket promedio | $439,53 |
| Ventas > $100 | 66,9 % (164) |

| Producto | Total | Ventas |
|---|---:|---:|
| Laptop | 60.000,00 | 32 |
| Tablet | 15.620,00 | 42 |
| Monitor | 14.400,00 | 31 |
| Impresora | 8.400,00 | 36 |
| Audifonos | 5.440,00 | 39 |
| Teclado | 2.500,00 | 33 |
| Mouse | 1.325,00 | 32 |

| Cliente | Total |
|---|---:|
| Carlos | 23.855,00 |
| Ana | 23.420,00 |
| Elena | 22.220,00 |
| David | 20.160,00 |
| Beatriz | 18.030,00 |

## 6. Power BI

Los CSV listos estan en `powerbi/`. Guia de 6 pasos en `powerbi/GUIA-POWERBI.md`.
Dashboard de verificacion: `powerbi/dashboard.html`.

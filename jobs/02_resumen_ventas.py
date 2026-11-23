# Analitica para Power BI: agrega ventas por producto, cliente y mes en HDFS.
# Ejecutar: spark-submit /jobs/02_resumen_ventas.py

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("ResumenVentasParaPowerBI") \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("hdfs://namenode:9000/data/raw/ventas.csv")

df.createOrReplaceTempView("ventas")

por_producto = spark.sql("""
    SELECT Producto,
           SUM(Cantidad)          AS Unidades,
           ROUND(SUM(Monto), 2)   AS TotalVendido,
           ROUND(AVG(Monto), 2)   AS TicketPromedio,
           COUNT(*)               AS NumVentas
    FROM ventas
    GROUP BY Producto
    ORDER BY TotalVendido DESC
""")

por_cliente = spark.sql("""
    SELECT Cliente,
           ROUND(SUM(Monto), 2) AS TotalVendido,
           COUNT(*)             AS NumVentas,
           ROUND(AVG(Monto), 2) AS TicketPromedio
    FROM ventas
    GROUP BY Cliente
    ORDER BY TotalVendido DESC
""")

por_mes = spark.sql("""
    SELECT Mes,
           ROUND(SUM(Monto), 2) AS TotalVendido,
           COUNT(*)             AS NumVentas
    FROM ventas
    GROUP BY Mes
    ORDER BY Mes
""")

resumen = spark.sql("""
    SELECT COUNT(*)                                            AS NumVentas,
           ROUND(SUM(Monto), 2)                                AS TotalVendido,
           ROUND(AVG(Monto), 2)                                AS TicketPromedio,
           ROUND(100.0 * SUM(CASE WHEN Monto > 100 THEN 1 ELSE 0 END) / COUNT(*), 1) AS PctVentasAltas
    FROM ventas
""")

def guardar(df_out, ruta):
    df_out.coalesce(1).write.mode("overwrite").option("header", "true").csv(ruta)

guardar(por_producto, "hdfs://namenode:9000/data/analitica/ventas_por_producto")
guardar(por_cliente,  "hdfs://namenode:9000/data/analitica/ventas_por_cliente")
guardar(por_mes,      "hdfs://namenode:9000/data/analitica/ventas_por_mes")
guardar(resumen,      "hdfs://namenode:9000/data/analitica/resumen_general")

print("=== Ventas por producto ===")
por_producto.show(truncate=False)
print("=== Ventas por cliente ===")
por_cliente.show(truncate=False)
print("=== Resumen general ===")
resumen.show(truncate=False)

spark.stop()

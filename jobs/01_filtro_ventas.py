# Caso practico del documento: filtrar ventas > $100 y guardar en HDFS.
# Ejecutar: spark-submit /jobs/01_filtro_ventas.py

from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("FiltroVentasMayores100") \
    .getOrCreate()

df_ventas = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("hdfs://namenode:9000/data/raw/ventas.csv")

print("Total de registros leidos: %d" % df_ventas.count())

df_filtrado = df_ventas.filter(df_ventas.Monto > 100).repartition(2)

df_filtrado.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("hdfs://namenode:9000/data/ventas_altas")

print("Registros con monto > 100: %d" % df_filtrado.count())
df_filtrado.show(10, truncate=False)

spark.stop()

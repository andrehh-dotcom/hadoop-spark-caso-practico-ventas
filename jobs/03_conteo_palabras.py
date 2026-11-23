# ELT de datos no estructurados: conteo de palabras de los comentarios.
# Ejecutar: spark-submit /jobs/03_conteo_palabras.py

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder \
    .appName("ConteoPalabrasComentarios") \
    .getOrCreate()

texto = spark.read.text("hdfs://namenode:9000/data/raw/comentarios.txt")

palabras = texto \
    .select(F.explode(F.split(F.lower(F.col("value")), "\\W+")).alias("palabra")) \
    .filter(F.length("palabra") > 3) \
    .groupBy("palabra") \
    .count() \
    .orderBy(F.desc("count"))

palabras.coalesce(1).write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("hdfs://namenode:9000/data/analitica/palabras_comentarios")

palabras.show(15, truncate=False)

spark.stop()

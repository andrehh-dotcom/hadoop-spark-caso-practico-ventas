"""Genera el informe documental del caso práctico con capturas paso a paso.

Estilo basado en el documento de referencia 'proyecto final.docx':
secciones con título, descripción en viñeta e imagen debajo de cada paso.
"""
from __future__ import annotations

import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

REF = r'C:\Users\USUARIO\Downloads\proyecto final.docx'
EV = r'C:\hadoop-spark-cluster\evidencias'
OUT = r'C:\hadoop-spark-cluster\Informe_Caso_Practico.docx'

doc = Document(REF)
for par in list(doc.paragraphs):
    par._element.getparent().remove(par._element)
for table in list(doc.tables):
    table._element.getparent().remove(table._element)


def p(text='', *, center=False, bold=False, size=None, bullet=False,
      space_after=6):
    par = doc.add_paragraph(style='normal')
    run = par.add_run(('• ' if bullet else '') + text)
    run.bold = bold
    if size:
        run.font.size = Pt(size)
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    par.paragraph_format.space_after = Pt(space_after)
    return par


def heading(text):
    par = doc.add_paragraph(style='normal')
    run = par.add_run(text)
    run.bold = True
    run.font.size = Pt(15)
    par.paragraph_format.space_before = Pt(14)
    par.paragraph_format.space_after = Pt(8)
    return par


def img(name, caption=None, width=6.2):
    path = os.path.join(EV, name)
    if not os.path.exists(path):
        print('FALTA:', path, flush=True)
        return
    par = doc.add_paragraph(style='normal')
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(6)
    par.paragraph_format.space_after = Pt(4)
    par.add_run().add_picture(path, width=Inches(width))
    if caption:
        cap = doc.add_paragraph(style='normal')
        cap.paragraph_format.space_after = Pt(10)
        cap.add_run(caption)


# ------------------------------------------------------------------ PORTADA
p('FACULTAD DE INGENIERÍA y ARQUITECTURA', center=True)
p('ESCUELA PROFESIONAL DE INGENIERÍA DE SISTEMAS\n\n\nArquitectura Empresarial', center=True)
p('')
p('Hadoop 3 y Spark en Docker', center=True, bold=True, size=16)
p('')
p('Integrantes:', center=True)
p('-Huapaya Huapaya Orlando Andre', center=True)
p('-Ramirez Ccoyllo Johan Brayan', center=True)
p('-Arana Alarcón Joseph Alfonso', center=True)
p('')
p('DOCENTE:\nCladuio Isaias Huancahuire Bravo', center=True)
for _ in range(8):
    p('')
p('PERÚ, LIMA, 2026', center=True)
doc.add_page_break()

# --------------------------------------------------------------- ESCENARIO
heading('Escenario del caso práctico')
p('Imagina que eres un analista de datos y quieres procesar las ventas de una '
  'tienda, filtrar las compras con montos superiores a $100, guardarlas en el '
  'cluster de HDFS y finalmente consultar esos datos guardados.')

# ------------------------------------------------------------ TERMINAL PYSPARK
heading('Terminal PySpark')
img('cp01_pyspark_terminal.png')
p('Descripción: Se muestra la terminal de PowerShell. El usuario ejecuta el '
  'comando para entrar al contenedor spark-master y abrir la consola '
  'interactiva de PySpark (docker exec -it spark-master /spark/bin/pyspark '
  '--master spark://spark-master:7077). Se muestran los mensajes de inicio de '
  'Spark (versión 3.0.0, Python 2.7.18) y las advertencias (WARN) normales.',
  bullet=True)

# ------------------------------------------------------- CREAR Y PROCESAR
heading('Crear y procesar los datos')
img('cp02_dataframe.png')
p("Descripción: En la consola >>> se pega y ejecuta el código Python. Se crea "
  "la lista con los datos de prueba (Carlos, Ana, Beatriz, David, Elena) y se "
  "convierte en un DataFrame de Spark llamado df_ventas definiendo las "
  "columnas ('Cliente', 'Producto', 'Monto').", bullet=True)

heading('Filtrar las ventas mayores a 100 USD')
img('cp03_filtro.png')
p('Descripción: Se aplica el filtro df_ventas.Monto > 100 y se muestra el '
  'resultado en pantalla con df_filtrado.show(). Se retienen tres registros: '
  'Carlos (Laptop, 1200), Beatriz (Monitor, 300) y Elena (Celular, 800). '
  'Se excluyen Ana (Mouse, 25) y David (Teclado, 45).', bullet=True)

# --------------------------------------------------------------- HDFS
heading('Guardar el resultado en Hadoop (HDFS)')
img('cp04_guardar_hdfs.png')
p('Descripción: Sin salir del shell >>>, se escribe el comando para persistir '
  'los datos filtrados en el sistema de archivos distribuido de Hadoop. Se '
  'utiliza df_filtrado.write.mode("overwrite").option("header", "true").csv(...) '
  'apuntando a la ruta hdfs://namenode:9000/data/ventas_altas. Se confirma con '
  'el mensaje "Datos guardados con éxito en HDFS!".', bullet=True)

# ------------------------------------------------------------- VERIFICACIÓN
heading('Verificación en la interfaz web de Hadoop')
img('cp05_namenode_browse.png')
p('Descripción: Se abre el navegador en http://localhost:9870 (NameNode de '
  'Hadoop) y se dirige a Utilities → Browse the file system. Se navega hasta '
  'la carpeta /data/ventas_altas. La imagen muestra cómo Spark generó los '
  'archivos dentro de HDFS: el archivo _SUCCESS (que indica que la operación '
  'terminó bien) y los archivos part-00000.csv y part-00001.csv, confirmando '
  'que los datos filtrados se guardaron correctamente en el clúster.',
  bullet=True)

# ---------------------------------------------------------------- POWER BI
heading('Informe en Power BI Desktop')
p('Descripción: Se carga el archivo ventas_filtradas.csv en Power BI Desktop '
  'y se construye el informe Dashboard_Ventas.pbix con tres visuales: una '
  'tarjeta con el total filtrado, un gráfico de columnas del monto por cliente '
  'y una tabla de detalle.', bullet=True)

img('cp06_pbi_card.png')
p('Tarjeta (Card) con la suma del campo Monto: $2,300 correspondiente a las '
  'tres ventas mayores a $100.')

img('cp07_pbi_chart.png')
p('Gráfico de columnas agrupadas con el Monto por Cliente: Carlos $1,200, '
  'Elena $800 y Beatriz $300.')

img('cp08_pbi_table.png')
p('Tabla de detalle con las columnas Cliente, Producto y Monto de los registros '
  'guardados en HDFS.')

img('cp09_pbi_final.png')
p('Informe terminado y guardado como Dashboard_Ventas.pbix.')

# -------------------------------------------------------------- RESULTADO
heading('Resultado final')
p('Al finalizar el trabajo se dejaron abiertos: Visual Studio Code con la '
  'carpeta del proyecto, Docker Desktop con el clúster Hadoop 3 + Spark, las '
  'interfaces web del NameNode (9870), ResourceManager de YARN (8088) y Spark '
  'Master (8080), el dashboard HTML con los resultados del caso práctico y '
  'Power BI Desktop con el informe Dashboard_Ventas.pbix.')

doc.save(OUT)
print('GUARDADO:', OUT, os.path.getsize(OUT), flush=True)
print('PÁRRAFOS:', len(doc.paragraphs), 'IMÁGENES:', len(doc.inline_shapes),
      flush=True)

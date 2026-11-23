"""Genera el informe documental del proyecto con capturas y descripciones.

Usa como base el estilo de 'proyecto final.docx' (márgenes, fuentes y estilo normal).
"""
from __future__ import annotations

import os

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

REF = r'C:\Users\USUARIO\Downloads\proyecto final.docx'
EV = r'C:\hadoop-spark-cluster\evidencias'
OUT = r'C:\hadoop-spark-cluster\Informe_Proyecto_Hadoop_Spark_PowerBI.docx'

doc = Document(REF)

# Vaciar el contenido conservando estilos, márgenes y configuración de página
for par in list(doc.paragraphs):
    par._element.getparent().remove(par._element)
for table in list(doc.tables):
    table._element.getparent().remove(table._element)


def p(text='', *, center=False, bold=False, size=None, style='normal', space_after=6):
    par = doc.add_paragraph(style=style)
    run = par.add_run(text)
    run.bold = bold
    if size:
        run.font.size = Pt(size)
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    par.paragraph_format.space_after = Pt(space_after)
    return par


def heading(text, size=14):
    par = doc.add_paragraph(style='normal')
    run = par.add_run(text)
    run.bold = True
    run.font.size = Pt(size)
    par.paragraph_format.space_before = Pt(12)
    par.paragraph_format.space_after = Pt(8)
    return par


def img(name, caption, width=6.2):
    path = os.path.join(EV, name)
    if not os.path.exists(path):
        print('FALTA:', path)
        return
    par = doc.add_paragraph(style='normal')
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    par.paragraph_format.space_before = Pt(8)
    par.paragraph_format.space_after = Pt(4)
    par.add_run().add_picture(path, width=Inches(width))
    cap = doc.add_paragraph(style='normal')
    cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    cap.paragraph_format.space_after = Pt(10)
    cap.add_run(caption)


# ---------------------------------------------------------------- PORTADA
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

# --------------------------------------------------- 1. PROYECTO Y VS CODE
heading('1. Explorador de archivos y Visual Studio Code')
img('00_explorador.png',
    'Explorador de archivos: se muestra la carpeta principal del proyecto hadoop-spark-cluster, '
    'creada especialmente para este trabajo. Dentro se observan las carpetas data, evidencias, '
    'jobs, powerbi, scripts y tools, además de los archivos docker-compose.yml y hadoop.env. '
    'El proyecto es nuevo y aislado: no se reutilizaron contenedores de trabajos anteriores.')

p('VS Code - Explorer: se muestra la barra lateral izquierda de Visual Studio Code con la '
  'carpeta raíz hadoop-spark-cluster abierta. Desde este editor se revisaron y crearon todos '
  'los archivos de configuración, los jobs de Spark y el código Java del job MapReduce.')

img('01_vscode_compose.png',
    'Código docker-compose.yml: se muestra el archivo de configuración abierto en VS Code. '
    'En él se definen la versión 3.8, la red hadoop-spark-net con driver bridge, los volúmenes '
    'hadoop_namenode y hadoop_datanode para persistencia, y los seis servicios del clúster: '
    'namenode (9870/9000), datanode (9864), resourcemanager (8088), nodemanager, '
    'spark-master (8080/7077) y spark-worker (8081).')

# --------------------------------------------------------------- 2. DOCKER
heading('2. Levantamiento del clúster en Docker')
p('Se ejecutó docker compose up -d desde la carpeta C:\\hadoop-spark-cluster. La salida confirmó '
  'la creación de los seis contenedores del proyecto: datanode, namenode, spark-master, '
  'resourcemanager, nodemanager y spark-worker, todos con estado "Up" y healthcheck en '
  'namenode, datanode, resourcemanager y nodemanager.')

img('02_docker_desktop.png',
    'Docker Desktop: se muestra la aplicación ejecutándose con los contenedores del proyecto. '
    'Cada contenedor fue creado para este trabajo, con su propia red y volúmenes, '
    'garantizando que el entorno sea independiente y reproducible.')

# ----------------------------------------------------------- 3. LOCALHOSTS
heading('3. Interfaces web de administración del clúster')

img('03_namenode.png',
    'NameNode de Hadoop (http://localhost:9870): se observa el panel Overview (Resumen) con '
    'Hadoop 3.2.1, un nodo vivo (Live Nodes: 1) y el estado saludable del sistema de archivos '
    'distribuido HDFS.')

img('04_yarn.png',
    'ResourceManager de YARN (http://localhost:8088): se confirma el clúster activo con 1 nodo '
    'en estado RUNNING y el planificador Capacity Scheduler. En la tabla de aplicaciones se '
    'registran los trabajos ejecutados con estado FINISHED / SUCCEEDED.')

img('05_spark.png',
    'Spark Master (http://localhost:8080): se muestra el estado ALIVE del maestro, 1 worker '
    'conectado, 1 core y 1024 MiB de memoria. En la sección de aplicaciones se listan los '
    'trabajos Spark completados correctamente.')

# --------------------------------------------------------- 4. CASO PRÁCTICO
heading('4. Caso práctico: ventas superiores a $100')
p('Escenario: se analizan las ventas de una tienda. El objetivo es filtrar las compras con '
  'monto superior a $100, guardarlas en HDFS y consultarlas desde Spark y Power BI.')
p('Los datos se generaron con la semilla 2026 en el archivo scripts/generar_datos.py, '
  'obteniendo 245 transacciones y 96 comentarios. Ambos archivos se ingestaron en /data/raw '
  'de HDFS.')
p('Procesamiento Spark: el job 01_filtro_ventas.py aplicó el filtro Monto > 100 y generó '
  '164 registros en /data/ventas_altas. El job 02_resumen_ventas.py produjo los agregados '
  'por producto, cliente y mes en /data/analitica. El job 03_conteo_palabras.py procesó los '
  'comentarios.')
p('Procesamiento MapReduce: el job Java VentaTotal.java se compiló dentro del contenedor '
  'namenode y se ejecutó con yarn jar, escribiendo los resultados en '
  '/data/ventas_por_producto_mr.')
p('Resultados por producto (MapReduce): Laptop $60,000; Tablet $15,620; Monitor $14,400; '
  'Impresora $8,400; Audifonos $5,440; Teclado $2,500 y Mouse $1,325.')

heading('4.1 Verificación del caso práctico en el NameNode', size=12)
p('Para comprobar que Spark guardó correctamente los datos filtrados se abrió '
  'http://localhost:9870 en el navegador y se ingresó a Utilities → Browse the file system, '
  'navegando hasta la carpeta /data/ventas_altas.')

img('08_namenode_ventas_altas.png',
    'Verificación en la interfaz web de Hadoop: en Utilities → Browse the file system, '
    'dentro de /data/ventas_altas, se listan el archivo _SUCCESS (que indica que la operación '
    'terminó correctamente) y los archivos part-00000 y part-00001 con extensión .csv, '
    'confirmando que los datos filtrados por Spark se guardaron en HDFS.')

# ------------------------------------------------------------- 5. POWER BI
heading('5. Construcción del informe en Power BI Desktop')

img('pbi_resumen_general_01_gallery.png',
    'Obtención de datos: desde la página de inicio de Power BI Desktop se seleccionó '
    '"Get data from other sources" y se abrió la galería de orígenes, donde se eligió Text/CSV.')

img('pbi_resumen_general_02_path.png',
    'Se indicó la ruta del archivo C:\\hadoop-spark-cluster\\powerbi\\resumen_general.csv '
    'en el cuadro de archivo de Windows y se confirmó con Abrir.')

img('pbi_resumen_general_03_import.png',
    'Diálogo de importación de Power BI para el archivo CSV. Se verificó la vista previa y '
    'se pulsó el botón Load para incorporar la tabla al modelo.')

img('pbi_resumen_general_04_loaded.png',
    'La tabla resumen_general ya aparece en el panel Data. Se repitió el mismo procedimiento '
    'para ventas_altas, ventas_por_producto, ventas_por_cliente, ventas_por_mes, '
    'palabras_comentarios y ventas_por_producto_mr, hasta completar siete tablas.')

img('pbi_fields_expanded.png',
    'Panel Data de Power BI Desktop con las siete tablas expandidas y sus campos: NumVentas, '
    'TotalVendido, TicketPromedio, PctVentasAltas, Cliente, Producto, Mes, Monto, count y palabra.')

img('pbi_visual_01.png',
    'Primer visual: tarjeta (Card) con la suma de TotalVendido, que muestra $107,685.00 '
    'como venta total del periodo.')

img('pbi_visual_02.png',
    'Segundo visual: tarjeta con NumVentas, correspondiente a 245 transacciones procesadas.')

img('pbi_visual_03.png',
    'Tercer visual: tarjeta con TicketPromedio, con un valor de $439.53 por transacción.')

img('pbi_visual_04.png',
    'Cuarto visual: tarjeta con PctVentasAltas, que indica que el 66.9% de las ventas superan $100.')

img('pbi_visual_05.png',
    'Gráfico de columnas agrupadas de ventas por producto. Laptop lidera con $60,000, '
    'seguido de Tablet con $15,620 y Monitor con $14,400.')

img('pbi_visual_06.png',
    'Gráfico de columnas agrupadas de ventas por cliente. Carlos encabeza la lista con '
    '$23,855, seguido de Ana con $23,420.')

img('pbi_visual_07.png',
    'Gráfico de líneas con la evolución mensual de TotalVendido, construido desde la tabla '
    'ventas_por_mes.')

img('pbi_visual_08.png',
    'Tabla de detalle de ventas altas: Monto, Cliente, Producto y Ciudad de las transacciones '
    'superiores a $100.')

img('pbi_visual_09.png',
    'Gráfico de columnas con los resultados del job MapReduce por producto, proporcionando '
    'la comparación directa entre el procesamiento MapReduce y Spark.')

img('pbi_visual_10.png',
    'Gráfico de barras de palabras más frecuentes en los comentarios, generado a partir del '
    'conteo de palabras del job Spark.')

# --------------------------------------------------------- 6. RESULTADO FINAL
heading('6. Dashboard y resultado final')

img('06_dashboard_web.png',
    'Dashboard web complementario (powerbi/dashboard.html): muestra los KPIs calculados '
    '- $107,685.00 en ventas, 245 transacciones, $439.53 de ticket promedio y 66.9% de '
    'ventas altas- junto con las tablas de productos, clientes y meses.')

img('07_powerbi_final.png',
    'Informe terminado en Power BI Desktop, guardado como Dashboard_Ventas.pbix. '
    'El informe contiene diez visuales: cuatro tarjetas KPI, tres gráficos de columnas, '
    'un gráfico de líneas, una tabla de detalle y un gráfico de barras.')

p('Al finalizar el trabajo se dejaron abiertos: Visual Studio Code con el proyecto, '
  'Docker Desktop con los seis contenedores, las interfaces web de NameNode (9870), '
  'ResourceManager (8088) y Spark Master (8080), el dashboard HTML y Power BI Desktop '
  'con el informe Dashboard_Ventas.pbix.')

doc.save(OUT)
print('GUARDADO:', OUT, os.path.getsize(OUT), flush=True)

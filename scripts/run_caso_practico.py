"""Ejecuta el caso práctico exacto en la consola interactiva de PySpark.

Ventas: Carlos/Ana/Beatriz/David/Elena -> filtro Monto > 100
-> persistencia en hdfs://namenode:9000/data/ventas_altas
Captura una imagen por etapa para la documentación.
"""
from __future__ import annotations

import os
import sys
import time

import pyperclip
from PIL import ImageGrab
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

EV = r'C:\hadoop-spark-cluster\evidencias'
os.makedirs(EV, exist_ok=True)


def find_console():
    for w in Desktop(backend='uia').windows():
        try:
            if (w.is_visible() and 'powershell.exe' in w.window_text().lower()):
                return w
        except Exception:
            pass
    return None


def shot(name):
    p = os.path.join(EV, name + '.png')
    ImageGrab.grab().save(p)
    print('CAPTURA:', name, os.path.getsize(p), flush=True)


def paste(code, wait=1.2):
    pyperclip.copy(code)
    send_keys('^v')
    time.sleep(0.35)
    send_keys('{ENTER}')
    time.sleep(wait)


win = find_console()
if win is None:
    raise RuntimeError('No se encontró la consola de PySpark')
win.set_focus()
time.sleep(1.0)
print('CONSOLA:', win.window_text(), flush=True)

# 1. Estado inicial: terminal con PySpark ya iniciado
shot('cp01_pyspark_terminal')

# 2. Crear la lista y el DataFrame
paste('ventas = [("Carlos", "Laptop", 1200), ("Ana", "Mouse", 25), '
      '("Beatriz", "Monitor", 300), ("David", "Teclado", 45), '
      '("Elena", "Celular", 800)]')
paste('columnas = ["Cliente", "Producto", "Monto"]')
paste('df_ventas = spark.createDataFrame(ventas, columnas)')
paste('df_ventas.show()', wait=2.0)
shot('cp02_dataframe')

# 3. Filtrar las ventas mayores a 100 USD
paste('df_filtrado = df_ventas.filter(df_ventas.Monto > 100)')
paste('print("=== VENTAS MAYORES A 100 USD ===")')
paste('df_filtrado.show()', wait=2.5)
shot('cp03_filtro')

# 4. Guardar el resultado en HDFS
paste('df_filtrado.write.mode("overwrite").option("header", "true")'
      '.csv("hdfs://namenode:9000/data/ventas_altas")', wait=25.0)
paste('print("Datos guardados con exito en HDFS!")', wait=1.5)
shot('cp04_guardar_hdfs')

print('FIN', flush=True)

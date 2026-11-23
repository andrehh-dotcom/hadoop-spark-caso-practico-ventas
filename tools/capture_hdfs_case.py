"""Captura la verificación del caso práctico en el explorador HDFS del NameNode."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto import Desktop

EV = r'C:\hadoop-spark-cluster\evidencias'


def find_window(needle):
    for w in Desktop(backend='uia').windows():
        try:
            if w.is_visible() and needle.lower() in w.window_text().lower():
                return w
        except Exception:
            pass
    return None


w = find_window('Browsing HDFS')
if w is None:
    raise RuntimeError('No se encontró la ventana Browsing HDFS')
w.set_focus()
time.sleep(2)
p = os.path.join(EV, '08_namenode_ventas_altas.png')
ImageGrab.grab().save(p)
print('capturado:', p, os.path.getsize(p), flush=True)
print('titulo:', w.window_text().encode('ascii', 'replace').decode(), flush=True)

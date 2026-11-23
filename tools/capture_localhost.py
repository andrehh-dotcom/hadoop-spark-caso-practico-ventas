"""Captura cada interfaz web en su propia ventana de Edge."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto import Desktop

EV = r'C:\hadoop-spark-cluster\evidencias'

SPECS = [
    ('Namenode information', '03_namenode'),
    ('All Applications', '04_yarn'),
    ('Spark Master', '05_spark'),
    ('Dashboard de Ventas', '06_dashboard_web'),
]


def find_window(needle):
    for w in Desktop(backend='uia').windows():
        try:
            if w.is_visible() and needle.lower() in w.window_text().lower():
                return w
        except Exception:
            pass
    return None


for needle, name in SPECS:
    w = find_window(needle)
    if w is None:
        print('NO ENCONTRADA:', needle, flush=True)
        continue
    try:
        w.set_focus()
        time.sleep(1.5)
    except Exception as e:
        print('focus error', e, flush=True)
    p = os.path.join(EV, name + '.png')
    ImageGrab.grab().save(p)
    print('capturado:', name, os.path.getsize(p), flush=True)

"""Reconstruye los 3 visuales del caso práctico deseleccionando antes de cada uno.

La clave: hacer clic en un área vacía del lienzo antes de elegir el tipo de
visual en el panel Visualizaciones; si no, Power BI cambia el tipo del visual
seleccionado en lugar de crear uno nuevo.
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
EMPTY = (1050, 800)   # área vacía del lienzo
FIRST = (180, 300)    # sobre el visual existente, para borrarlo

win = main_window(timeout=20)
print('VENTANA:', win.window_text(), flush=True)


def shot(name):
    p = os.path.join(EV, name + '.png')
    ImageGrab.grab().save(p)
    print('CAPTURA:', name, os.path.getsize(p), flush=True)


def deselect():
    mouse.click(coords=EMPTY)
    time.sleep(0.8)
    send_keys('{ESC}')
    time.sleep(0.4)


def listitem(vtype):
    for e in win.descendants(control_type='ListItem'):
        try:
            if (e.is_visible()
                    and (e.element_info.name or '').strip() == vtype):
                return e
        except Exception:
            pass
    raise RuntimeError('tipo no visible: ' + vtype)


def field(name):
    for e in win.descendants(control_type='CheckBox'):
        try:
            if e.is_visible() and (e.element_info.name or '') == name:
                return e
        except Exception:
            pass
    raise RuntimeError('campo no visible: ' + repr(name))


def create(vtype, fields, cap):
    deselect()
    item = listitem(vtype)
    item.click_input()
    time.sleep(1.5)
    for f in fields:
        field(f).click_input()
        time.sleep(1.8)
    deselect()
    shot(cap)
    print('VISUAL:', vtype, fields, flush=True)


# Borrar el visual anterior (tabla con todos los campos)
deselect()
mouse.click(coords=FIRST)
time.sleep(0.8)
send_keys('{DELETE}')
time.sleep(1.5)
deselect()
shot('cp06_pbi_limpio')

create('Card', ['Numeric Field Monto'], 'cp06_pbi_card')
create('Clustered column chart',
       ['Numeric Field Monto', ' Cliente'], 'cp07_pbi_chart')
create('Table', [' Cliente', ' Producto', 'Numeric Field Monto'],
       'cp08_pbi_table')

deselect()
shot('cp09_pbi_final')
print('FIN', flush=True)

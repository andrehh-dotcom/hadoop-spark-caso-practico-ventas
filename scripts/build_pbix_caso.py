"""Construye el informe Power BI del caso práctico usando la GUI.

Crea cada visual seleccionando primero su tipo en el panel Visualizaciones,
lo que garantiza que se genere un visual nuevo y no se acumulen campos en uno
existente. Datos: solo las 3 ventas filtradas en HDFS.
"""
from __future__ import annotations

import os
import shutil
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import find, main_window, write

EV = r'C:\hadoop-spark-cluster\evidencias'
NAME = 'Dashboard_Ventas'
DEST = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'

win = main_window(timeout=20)
print('VENTANA:', win.window_text(), flush=True)


def shot(name):
    p = os.path.join(EV, name + '.png')
    ImageGrab.grab().save(p)
    print('CAPTURA:', name, os.path.getsize(p), flush=True)


def listitem(vtype):
    for e in win.descendants(control_type='ListItem'):
        try:
            if (e.is_visible()
                    and (e.element_info.name or '').strip() == vtype):
                return e
        except Exception:
            pass
    raise RuntimeError('tipo de visual no visible: ' + vtype)


def field(name):
    for e in win.descendants(control_type='CheckBox'):
        try:
            if e.is_visible() and (e.element_info.name or '') == name:
                return e
        except Exception:
            pass
    raise RuntimeError('campo no visible: ' + repr(name))


def create(vtype, fields, cap):
    send_keys('{ESC}')
    time.sleep(0.5)
    item = listitem(vtype)
    item.click_input()
    time.sleep(1.5)
    for f in fields:
        field(f).click_input()
        time.sleep(1.8)
    send_keys('{ESC}')
    time.sleep(0.5)
    shot(cap)
    print('VISUAL:', vtype, fields, flush=True)


# 1. Tarjeta con el total de las ventas filtradas
create('Card', ['Numeric Field Monto'], 'cp06_pbi_card')

# 2. Gráfico de columnas: monto por cliente
create('Clustered column chart',
       ['Numeric Field Monto', ' Cliente'], 'cp07_pbi_chart')

# 3. Tabla de detalle: cliente, producto y monto
create('Table', [' Cliente', ' Producto', 'Numeric Field Monto'],
       'cp08_pbi_table')

# Captura del informe terminado
shot('cp09_pbi_final')

# Guardar
win.set_focus()
send_keys('^s')
time.sleep(3)
dlg = None
for e in win.descendants():
    try:
        if (e.element_info.class_name == 'quick-save-dialog'
                and e.is_visible()):
            dlg = e
            break
    except Exception:
        pass
print('dialogo guardado:', dlg is not None, flush=True)
if dlg is not None:
    dlg.set_focus()
    time.sleep(0.3)
    nm = find(dlg, auto_id='textInputDialogInputField', timeout=8)
    nm.set_edit_text(NAME)
    time.sleep(0.6)
    save = find(dlg, auto_id='okButton', timeout=8)
    print('save enabled:', save.is_enabled(), flush=True)
    if save.is_enabled():
        save.click_input()
        time.sleep(12)

shot('cp10_pbi_guardado')

# Localizar y copiar el archivo guardado
found = []
for root in (os.path.join(os.path.expanduser('~'), 'Documents'),
             r'C:\hadoop-spark-cluster\powerbi'):
    for d, _, files in os.walk(root):
        if NAME + '.pbix' in files:
            found.append(os.path.join(d, NAME + '.pbix'))
print('encontrados:', found, flush=True)
if found:
    src = max(found, key=os.path.getmtime)
    if os.path.abspath(src) != os.path.abspath(DEST):
        shutil.copy2(src, DEST)
    print('DESTINO:', DEST, os.path.getsize(DEST), flush=True)
print('TITULO:', win.window_text(), flush=True)

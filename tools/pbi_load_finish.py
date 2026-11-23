"""Pulsa Load en el diálogo de importación TEXT/CSV y verifica el modelo."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
win = main_window(timeout=15)

dlg = None
for el in win.descendants(control_type='Window'):
    try:
        if el.element_info.automation_id == 'ImportFromTextDialog' and el.is_visible():
            dlg = el
            break
    except Exception:
        pass
print('import dialog:', dlg is not None, flush=True)
if dlg is None:
    raise RuntimeError('No hay diálogo de importación')

load = None
for el in dlg.descendants(control_type='Button'):
    try:
        if el.element_info.name == 'Load' and el.is_visible():
            load = el
            break
    except Exception:
        pass
print('load:', load is not None, flush=True)
load.click_input()
time.sleep(12)
ImageGrab.grab().save(os.path.join(EV, 'pbi_resumen_05_loaded.png'))

print('=== tablas/campos en panel Data ===', flush=True)
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type in ('DataItem', 'ListItem') and el.is_visible():
            nm = (i.name or '')
            if any(k in nm.lower() for k in ('resumen', 'total', 'ventas', 'transacc',
                                             'ticket', 'cliente', 'producto', 'mes')):
                print(i.control_type, repr(nm)[:90], i.automation_id, flush=True)
    except Exception:
        pass
print('=== ventanas ===', flush=True)
for el in win.descendants(control_type='Window'):
    try:
        if el.is_visible():
            print('WIN', repr((el.element_info.name or '')[:60]),
                  el.element_info.automation_id, flush=True)
    except Exception:
        pass

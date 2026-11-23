"""Completa el cuadro Abrir ya visible y examina el Navigator resultante."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
path = os.path.abspath(r'C:\hadoop-spark-cluster\powerbi\resumen_general.csv')
win = main_window(timeout=15)

dlg = None
for el in win.descendants(control_type='Window'):
    try:
        if (el.element_info.class_name or '').strip() == '#32770' and el.is_visible():
            dlg = el
            break
    except Exception:
        pass
print('filedialog:', dlg is not None, flush=True)
if dlg is None:
    raise RuntimeError('No hay cuadro Abrir abierto')

edit = None
for el in dlg.descendants(control_type='Edit'):
    try:
        if el.element_info.automation_id == '1148':
            edit = el
            break
    except Exception:
        pass
print('edit:', edit is not None, flush=True)
if edit is None:
    raise RuntimeError('No hay campo Nombre de archivo')

edit.click_input()
edit.set_edit_text(path)
time.sleep(0.4)
print('ruta:', repr(edit.window_text()), flush=True)
send_keys('{ENTER}')
time.sleep(5)
ImageGrab.grab().save(os.path.join(EV, 'pbi_step3_navigator.png'))

print('=== ventanas ===', flush=True)
for el in win.descendants(control_type='Window'):
    try:
        if el.is_visible():
            i = el.element_info
            print('WIN', repr((i.name or '')[:70]), (i.class_name or '')[:40],
                  i.automation_id, el.rectangle(), flush=True)
    except Exception:
        pass
print('=== checkboxes ===', flush=True)
for el in win.descendants(control_type='CheckBox'):
    try:
        if el.is_visible():
            print('CB', repr(el.element_info.name)[:80],
                  el.element_info.automation_id, el.rectangle(), flush=True)
    except Exception:
        pass
print('=== botones Load/Connect ===', flush=True)
for el in win.descendants(control_type='Button'):
    try:
        if el.is_visible() and any(k in (el.element_info.name or '').lower()
                                   for k in ('load', 'connect', 'transform')):
            print('BTN', repr(el.element_info.name)[:60],
                  el.element_info.automation_id, el.rectangle(), flush=True)
    except Exception:
        pass

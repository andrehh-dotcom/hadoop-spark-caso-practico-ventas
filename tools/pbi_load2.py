"""Carga un CSV en Power BI Desktop (flujo directo desde la página de inicio)."""
import os
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_focus import focus_powerbi
from pbi_ui import find, main_window, write

EV = r'C:\hadoop-spark-cluster\evidencias'
path = os.path.abspath(sys.argv[1])
tag = sys.argv[2] if len(sys.argv) > 2 else 'csv'
stem = os.path.splitext(os.path.basename(path))[0]
shot = lambda n: ImageGrab.grab().save(os.path.join(EV, 'pbi_%s_%s.png' % (tag, n)))

win = focus_powerbi()
win.set_focus()
time.sleep(0.5)
print('ventana:', win.window_text(), flush=True)

# 1) botón de inicio "Get data from other sources"
start = None
for el in win.descendants(control_type='Button'):
    try:
        if el.is_visible() and (el.element_info.name or '') == 'Get data from other sources':
            start = el
            break
    except Exception:
        pass
print('start button:', start is not None, flush=True)
if start is None:
    raise RuntimeError('No está la página de inicio')
start.click_input()
time.sleep(2.0)
shot('01_gallery')

# 2) galería (buscar entre ventanas descendientes por automation_id o class)
gal = None
for el in win.descendants(control_type='Window'):
    try:
        i = el.element_info
        if (i.automation_id == 'DataSourceGalleryDialog'
                or 'DataSourceGalleryDialog' in (i.class_name or '')):
            gal = el
            break
    except Exception:
        pass
print('galería:', gal is not None, flush=True)
if gal is None:
    raise RuntimeError('Galería no encontrada')
item = None
for el in gal.descendants(control_type='DataItem'):
    try:
        if (el.element_info.name or '') == 'Text/CSV' and el.is_visible():
            item = el
            break
    except Exception:
        pass
print('Text/CSV:', item is not None, flush=True)
item.click_input()
time.sleep(0.6)
connect = find(win, name='Connect', control_type='Button', timeout=10)
connect.click_input()
time.sleep(2.0)
shot('02_filedialog')

# 3) diálogo de archivo: escribir ruta con el teclado y Enter
send_keys(path, with_spaces=True, pause=0.01)
time.sleep(0.5)
shot('03_path')
send_keys('{ENTER}')
time.sleep(4.0)
shot('04_navigator')

# 4) Navigator: marcar tabla y Load
nav = None
for el in win.descendants(control_type='Window'):
    try:
        if el.element_info.automation_id == 'NavigatorDialog':
            nav = el
            break
    except Exception:
        pass
print('navigator:', nav is not None, flush=True)
if nav is None:
    raise RuntimeError('Navigator no encontrado')
checks = []
for el in nav.descendants(control_type='CheckBox'):
    try:
        if el.is_visible():
            checks.append((el.element_info.name, el))
    except Exception:
        pass
print('tablas:', [c[0] for c in checks][:10], flush=True)
target = next((el for nm, el in checks if stem.lower() in (nm or '').lower()),
              checks[0][1] if checks else None)
if target is None:
    raise RuntimeError('Sin tablas en Navigator')
if target.get_toggle_state() != 1:
    target.iface_toggle.Toggle()
time.sleep(0.4)
load = find(nav, auto_id='idLoadButton', timeout=10)
print('load enabled:', load.is_enabled(), flush=True)
load.click_input()
time.sleep(10)
shot('05_loaded')
print('CARGADO', stem, flush=True)

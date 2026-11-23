"""Carga un CSV en el modelo de Power BI Desktop mediante la GUI (pywinauto)."""
import os
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import find, main_window, write
from pbi_focus import focus_powerbi

EV = r'C:\hadoop-spark-cluster\evidencias'
path = os.path.abspath(sys.argv[1])
stem = os.path.splitext(os.path.basename(path))[0]
shot = lambda n: ImageGrab.grab().save(os.path.join(EV, 'pbi_%s.png' % n))
win = focus_powerbi()
print('ventana:', win.window_text(), flush=True)

# 1. Abrir galería Get data
search = find(win, auto_id='TellMe-SearchBox', timeout=20)
write(search, 'Get data')
time.sleep(0.9)
sugg = None
for el in win.descendants():
    try:
        i = el.element_info
        if (i.control_type == 'Button' and i.name == 'Get data'
                and 'splitPrimaryMenu' in (i.class_name or '') and el.is_visible()):
            sugg = el
            break
    except Exception:
        pass
if sugg is None:
    raise RuntimeError('No apareció la sugerencia Get data')
sugg.click_input()
time.sleep(1.2)
for el in win.descendants():
    try:
        i = el.element_info
        if (i.control_type == 'Button' and 'other sources' in (i.name or '').lower()
                and el.is_visible()):
            el.click_input()
            break
    except Exception:
        pass
time.sleep(1.5)
gal = find(win, auto_id='DataSourceGalleryDialog', timeout=15)
print('galería abierta', flush=True)

# 2. Elegir Text/CSV y conectar
item = find(gal, name='Text/CSV', control_type='DataItem', timeout=10)
item.click_input()
time.sleep(0.6)
connect = find(win, name='Connect', control_type='Button', timeout=10)
connect.click_input()
time.sleep(2.5)
shot('pbi_01_filedialog')
print('diálogo de archivo abierto', flush=True)

# 3. Escribir la ruta en el cuadro de archivo
combo = None
for el in win.descendants():
    try:
        i = el.element_info
        nm = (i.name or '').lower()
        if i.control_type == 'ComboBox' and el.is_visible() and (
                'archivo' in nm or 'file name' in nm):
            combo = el
            break
    except Exception:
        pass
if combo is None:
    print('=== combos visibles ===', flush=True)
    for el in win.descendants():
        try:
            i = el.element_info
            if i.control_type in ('ComboBox', 'Edit') and el.is_visible():
                print(i.control_type, repr(i.name)[:70], i.automation_id, el.rectangle(), flush=True)
        except Exception:
            pass
    raise RuntimeError('No se encontró el campo Nombre de archivo')

edit = None
for ch in combo.descendants():
    try:
        if ch.element_info.control_type == 'Edit':
            edit = ch
            break
    except Exception:
        pass
if edit is None:
    edit = combo
write(edit, path)
time.sleep(0.6)
shot('pbi_02_path')
print('ruta escrita:', path, flush=True)

# 4. Abrir / Aceptar
opened = False
for label in ('Abrir', 'Open'):
    try:
        btn = find(win, name=label, control_type='Button', timeout=3)
        btn.click_input()
        opened = True
        break
    except LookupError:
        continue
if not opened:
    combo.type_keys('{ENTER}')
time.sleep(4)
shot('pbi_03_navigator')
print('archivo abierto', flush=True)

# 5. Navigator: marcar tabla y Load
nav = find(win, auto_id='NavigatorDialog', timeout=20)
checks = []
for el in nav.descendants():
    try:
        i = el.element_info
        if i.control_type == 'CheckBox' and el.is_visible():
            checks.append((i.name, el))
    except Exception:
        pass
print('checkboxes:', [c[0] for c in checks][:20], flush=True)
target = None
for name, el in checks:
    if stem.lower() in (name or '').lower():
        target = el
        break
if target is None and checks:
    target = checks[0][1]
if target is None:
    raise RuntimeError('Navigator sin tablas')
if target.get_toggle_state() != 1:
    target.iface_toggle.Toggle()
time.sleep(0.5)
load = find(nav, auto_id='idLoadButton', timeout=10)
print('load enabled:', load.is_enabled(), flush=True)
load.click_input()
time.sleep(8)
shot('pbi_04_loaded')
print('CARGADO:', stem, flush=True)

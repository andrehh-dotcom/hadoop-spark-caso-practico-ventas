"""Guarda con nombre simple (el diálogo elige la ubicación) y copia al proyecto."""
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
DOCS = os.path.join(os.path.expanduser('~'), 'Documents', NAME + '.pbix')
DEST = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'

win = main_window(timeout=15)
dlg = None
for el in win.descendants():
    try:
        if el.element_info.class_name == 'quick-save-dialog' and el.is_visible():
            dlg = el
            break
    except Exception:
        pass
if dlg is None:
    win.set_focus()
    send_keys('^s')
    time.sleep(2.5)
    for el in win.descendants():
        try:
            if el.element_info.class_name == 'quick-save-dialog' and el.is_visible():
                dlg = el
                break
        except Exception:
            pass
print('diálogo:', dlg is not None, flush=True)
if dlg is None:
    raise RuntimeError('Sin diálogo de guardado')

name = find(dlg, auto_id='textInputDialogInputField', timeout=8)
name.click_input()
# Borrar contenido previo y escribir nombre simple
send_keys('^a')
time.sleep(0.2)
write(name, NAME)
time.sleep(0.6)
print('campo:', repr(name.window_text()), flush=True)
save = find(dlg, auto_id='okButton', timeout=8)
print('save enabled:', save.is_enabled(), flush=True)
ImageGrab.grab().save(os.path.join(EV, 'pbi_save_simple_dialog.png'))
if not save.is_enabled():
    # Forzar evento de texto
    name.click_input()
    send_keys('{END} x{BACKSPACE}')
    time.sleep(0.6)
    print('save enabled (retry):', save.is_enabled(), flush=True)
    print('campo (retry):', repr(name.window_text()), flush=True)
save.click_input()
time.sleep(12)
ImageGrab.grab().save(os.path.join(EV, 'pbi_save_simple_saved.png'))

print('titulo:', win.window_text(), flush=True)
found = []
for root in (os.path.join(os.path.expanduser('~'), 'Documents'),
             os.path.join(os.path.expanduser('~'), '.config', 'openchamber', 'chats')):
    for d, _, files in os.walk(root):
        if NAME + '.pbix' in files:
            found.append(os.path.join(d, NAME + '.pbix'))
print('encontrados:', found, flush=True)
if found:
    src = max(found, key=os.path.getmtime)
    shutil.copy2(src, DEST)
    print('copiado:', DEST, os.path.getsize(DEST), flush=True)

"""Fuerza el nombre del diálogo de guardado mediante ValuePattern."""
import os
import shutil
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import find, main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
NAME = 'Dashboard_Ventas'
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
print('diálogo:', dlg is not None, flush=True)
if dlg is None:
    raise RuntimeError('Sin diálogo')

dlg.set_focus()
time.sleep(0.3)
name = find(dlg, auto_id='textInputDialogInputField', timeout=8)


def value():
    try:
        return name.iface_value.CurrentValue
    except Exception as e:
        return 'ERR ' + str(e)


print('valor actual:', repr(value()), flush=True)
try:
    name.set_edit_text(NAME)
    print('set_edit_text ->', repr(value()), flush=True)
except Exception as e:
    print('set_edit_text falló:', e, flush=True)
    name.click_input()
    send_keys('^a')
    send_keys(NAME, with_spaces=True)
    print('send_keys ->', repr(value()), flush=True)
time.sleep(0.8)
save = find(dlg, auto_id='okButton', timeout=8)
print('save enabled:', save.is_enabled(), flush=True)
ImageGrab.grab().save(os.path.join(EV, 'pbi_save_fix_dialog.png'))

if not save.is_enabled():
    # enviar un carácter extra y borrarlo para disparar validación
    try:
        name.click_input()
    except Exception:
        pass
    send_keys('x')
    time.sleep(0.3)
    send_keys('{BACKSPACE}')
    time.sleep(0.6)
    print('valor final:', repr(value()), flush=True)
    print('save enabled (retry):', save.is_enabled(), flush=True)

if save.is_enabled():
    save.click_input()
    time.sleep(12)
    ImageGrab.grab().save(os.path.join(EV, 'pbi_save_fix_saved.png'))
    print('titulo:', win.window_text(), flush=True)

# Localizar el archivo guardado
found = []
for root in (os.path.join(os.path.expanduser('~'), 'Documents'),
             r'C:\Users\USUARIO\.config\openchamber\chats'):
    for d, _, files in os.walk(root):
        if NAME + '.pbix' in files:
            found.append(os.path.join(d, NAME + '.pbix'))
print('encontrados:', found, flush=True)
for f in found:
    print(f, os.path.getsize(f), time.ctime(os.path.getmtime(f)), flush=True)
if found:
    src = max(found, key=os.path.getmtime)
    shutil.copy2(src, DEST)
    print('copiado:', DEST, os.path.getsize(DEST), flush=True)

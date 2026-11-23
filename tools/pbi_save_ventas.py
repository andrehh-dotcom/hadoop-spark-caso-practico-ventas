"""Guarda el informe como Dashboard_Ventas.pbix en la carpeta del proyecto."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import find, main_window, write

EV = r'C:\hadoop-spark-cluster\evidencias'
DOCS = os.path.join(os.path.expanduser('~'), 'Documents', 'Dashboard_Ventas.pbix')
DEST = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'

win = main_window(timeout=15)
# Si ya quedó un diálogo de guardado abierto, reutilizarlo
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
    ImageGrab.grab().save(os.path.join(EV, 'pbi_save_fail.png'))
    raise RuntimeError('No apareció el diálogo de guardado')

name = find(dlg, auto_id='textInputDialogInputField', timeout=8)
write(name, DEST)
time.sleep(0.4)
print('campo nombre:', repr(name.window_text()), flush=True)
save = None
for el in dlg.descendants(control_type='Button'):
    try:
        if (el.element_info.name or '') == 'Save' and el.is_visible():
            save = el
            break
    except Exception:
        pass
if save is None:
    save = find(dlg, auto_id='okButton', timeout=8)
print('save:', save.is_enabled(), flush=True)
ImageGrab.grab().save(os.path.join(EV, 'pbi_save_01_dialog.png'))
save.click_input()
time.sleep(12)
ImageGrab.grab().save(os.path.join(EV, 'pbi_save_02_saved.png'))

for p in (DEST, DOCS):
    print(p, os.path.exists(p), os.path.getsize(p) if os.path.exists(p) else 0, flush=True)
print('titulo:', win.window_text(), flush=True)

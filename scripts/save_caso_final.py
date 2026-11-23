"""Recrea la carpeta recordada, guarda con nombre simple y copia al proyecto."""
import os
import shutil
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
NAME = 'Dashboard_Ventas'
REMEMBERED = r'C:\hadoop-spark-cluster\powerbi\probe'
SOURCE = os.path.join(REMEMBERED, NAME + '.pbix')
DEST = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'
win = main_window(timeout=15)

os.makedirs(REMEMBERED, exist_ok=True)
print('carpeta creada:', os.path.isdir(REMEMBERED), flush=True)

# Cerrar el diálogo actual y cualquier error
send_keys('{ESC}')
time.sleep(0.5)
for e in list(win.descendants(control_type='Window')):
    try:
        if (e.is_visible() and e.element_info.automation_id
                in ('MessageDialog', 'ErrorDialog')):
            btns = [b for b in e.descendants(control_type='Button')
                    if b.is_visible() and (b.element_info.name or '') == 'Close']
            if btns:
                btns[-1].click_input()
                time.sleep(0.6)
    except Exception:
        pass

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
print('dialogo:', dlg is not None, flush=True)
if dlg is None:
    raise RuntimeError('sin dialogo')

dlg.set_focus()
time.sleep(0.4)
name = None
for e in dlg.descendants(control_type='Edit'):
    try:
        if e.element_info.automation_id == 'textInputDialogInputField':
            name = e
            break
    except Exception:
        pass
name.click_input()
name.set_edit_text(NAME)
time.sleep(0.8)
print('valor:', repr(name.iface_value.CurrentValue), flush=True)

save = None
for e in dlg.descendants(control_type='Button'):
    try:
        if e.is_visible() and (e.element_info.name or '') == 'Save':
            save = e
            break
    except Exception:
        pass
if save is None:
    for e in dlg.descendants():
        try:
            if e.element_info.automation_id == 'okButton':
                save = e
                break
        except Exception:
            pass
print('save enabled:', save.is_enabled() if save else None, flush=True)
ImageGrab.grab().save(os.path.join(EV, 'cp10_save_final_dialog.png'))
save.click_input()
time.sleep(15)

ImageGrab.grab().save(os.path.join(EV, 'cp10_pbi_guardado.png'))
print('TITULO:', win.window_text(), flush=True)
print('SOURCE:', os.path.exists(SOURCE),
      os.path.getsize(SOURCE) if os.path.exists(SOURCE) else 0, flush=True)
if os.path.exists(SOURCE):
    shutil.copy2(SOURCE, DEST)
    print('DESTINO:', DEST, os.path.getsize(DEST), flush=True)

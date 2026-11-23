"""Cierra diálogos de error pendientes y guarda el informe del caso práctico."""
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
DEST = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'
win = main_window(timeout=15)


def close_error_dialogs():
    n = 0
    for _ in range(6):
        found = False
        for e in list(win.descendants(control_type='Window')):
            try:
                if (e.is_visible() and e.element_info.automation_id
                        in ('MessageDialog', 'ErrorDialog')):
                    btns = [b for b in e.descendants(control_type='Button')
                            if b.is_visible()
                            and (b.element_info.name or '') == 'Close']
                    if btns:
                        btns[-1].click_input()
                        time.sleep(0.8)
                        n += 1
                        found = True
                        break
            except Exception:
                pass
        if not found:
            break
    print('diálogos de error cerrados:', n, flush=True)


close_error_dialogs()
time.sleep(1)
send_keys('{ESC}')
time.sleep(0.4)
win.set_focus()
send_keys('^s')
time.sleep(3)

# Verificar que no haya vuelto a aparecer un error
close_error_dialogs()

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
if dlg is None:
    ImageGrab.grab().save(os.path.join(EV, 'cp10_save_fail.png'))
    raise RuntimeError('sin dialogo de guardado')

dlg.set_focus()
time.sleep(0.5)
name = None
for e in dlg.descendants(control_type='Edit'):
    try:
        if e.element_info.automation_id == 'textInputDialogInputField':
            name = e
            break
    except Exception:
        pass
print('valor inicial:', repr(name.iface_value.CurrentValue), flush=True)
name.click_input()
name.set_edit_text(NAME)
time.sleep(0.8)
print('valor final:', repr(name.iface_value.CurrentValue), flush=True)

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
print('save:', save is not None, save.is_enabled() if save else None, flush=True)
ImageGrab.grab().save(os.path.join(EV, 'cp10_save_dialog2.png'))
save.click_input()
time.sleep(15)

close_error_dialogs()
ImageGrab.grab().save(os.path.join(EV, 'cp10_pbi_guardado.png'))
print('TITULO:', win.window_text(), flush=True)

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

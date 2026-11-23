"""Guarda indicando la ruta completa válida en el diálogo abierto."""
import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
DEST = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'
win = main_window(timeout=15)

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
name.set_edit_text(DEST)
time.sleep(1.0)
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
print('save:', save.is_enabled() if save else None, flush=True)
ImageGrab.grab().save(os.path.join(EV, 'cp10_save_path.png'))
save.click_input()
time.sleep(15)

# Leer errores antes de cerrarlos
for x in win.descendants(control_type='Window'):
    try:
        if (x.is_visible() and x.element_info.automation_id
                in ('MessageDialog', 'ErrorDialog')):
            for e in x.descendants(control_type='Text'):
                try:
                    if e.is_visible() and (e.element_info.name or '').strip():
                        print('ERROR:', e.element_info.name[:200], flush=True)
                except Exception:
                    pass
    except Exception:
        pass

ImageGrab.grab().save(os.path.join(EV, 'cp10_pbi_guardado.png'))
print('TITULO:', win.window_text(), flush=True)
print('EXISTE:', os.path.exists(DEST),
      os.path.getsize(DEST) if os.path.exists(DEST) else 0, flush=True)

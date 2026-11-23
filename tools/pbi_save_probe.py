"""Envía Ctrl+S y vuelca el diálogo de guardado sin confirmar nada."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
win = main_window(timeout=15)
win.set_focus()
send_keys('{ESC}')
time.sleep(0.4)
send_keys('^s')
time.sleep(3)
ImageGrab.grab().save(EV + r'\pbi_save_probe.png')

print('TITULO:', win.window_text(), flush=True)
for el in win.descendants(control_type='Window'):
    try:
        if not el.is_visible():
            continue
        i = el.element_info
        print('WIN', repr((i.name or '')[:80]), 'cls=', (i.class_name or '')[:70],
              'aid=', i.automation_id, 'rect=', el.rectangle(), flush=True)
        if (i.class_name or '') in ('#32770',) or 'save' in (i.class_name or '').lower():
            for c in el.descendants():
                try:
                    ci = c.element_info
                    if c.is_visible() and ci.control_type in ('Edit', 'ComboBox', 'Button'):
                        print('   ', ci.control_type, repr((ci.name or '')[:60]),
                              'aid=', ci.automation_id, 'rect=', c.rectangle(), flush=True)
                except Exception:
                    pass
    except Exception:
        pass

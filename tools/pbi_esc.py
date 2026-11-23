"""Envía Escape a los cuadros modales visibles de Power BI."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pywinauto import Desktop
from pywinauto.keyboard import send_keys

for w in Desktop(backend='uia').windows():
    try:
        if not w.is_visible():
            continue
        cls = w.class_name() or ''
        name = w.window_text() or ''
        if ('#32770' in cls or 'mdc-dialog' in cls) and ('Power BI' not in name):
            print('esc ->', repr(name[:60]), cls[:40], flush=True)
            try:
                w.set_focus()
            except Exception:
                pass
            send_keys('{ESC}')
            time.sleep(0.5)
    except Exception as e:
        print('err', e, flush=True)
time.sleep(1)

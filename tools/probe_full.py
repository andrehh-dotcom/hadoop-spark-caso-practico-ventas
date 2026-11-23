"""Vuelca el árbol UIA visible de Power BI Desktop para diagnóstico."""
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import main_window

win = main_window(timeout=15)
print('TITULO:', repr(win.window_text()), 'RECT:', win.rectangle(), flush=True)
ImageGrab.grab().save(r'C:\hadoop-spark-cluster\evidencias\pbi_full_state.png')

print('=== VENTANAS DESCENDIENTES ===', flush=True)
for el in win.descendants(control_type='Window'):
    try:
        i = el.element_info
        print('WIN', repr((i.name or '')[:80]), 'cls=', (i.class_name or '')[:70],
              'aid=', i.automation_id, 'rect=', el.rectangle(), 'vis=', el.is_visible(), flush=True)
    except Exception as e:
        print('WIN ERR', e, flush=True)

print('=== CONTROLES INTERESANTES ===', flush=True)
types = ('DataItem', 'ListItem', 'Edit', 'ComboBox', 'Button', 'Text')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type in types and el.is_visible():
            nm = (i.name or '')[:90]
            if i.control_type == 'Button' and not any(
                    k in nm.lower() for k in ('get data', 'connect', 'load', 'cancel',
                                              'close', 'ok', 'abrir', 'open', 'save')):
                continue
            print(i.control_type, repr(nm), 'aid=', i.automation_id,
                  'cls=', (i.class_name or '')[:40], 'rect=', el.rectangle(), flush=True)
    except Exception:
        pass

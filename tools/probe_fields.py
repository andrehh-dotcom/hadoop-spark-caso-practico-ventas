"""Expande las tablas del panel Data y lista los campos (checkboxes) disponibles."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
win = main_window(timeout=15)
seen = set()
trees = []
for el in win.descendants(control_type='TreeItem'):
    try:
        if not el.is_visible():
            continue
        nm = el.element_info.name or ''
        key = (nm, el.rectangle().left, el.rectangle().top)
        if key in seen or not nm.startswith('Table '):
            continue
        seen.add(key)
        trees.append((nm, el))
    except Exception:
        pass

print('TABLAS:', [t[0] for t in trees], flush=True)
for nm, el in trees:
    try:
        el.click_input()
        time.sleep(0.5)
        try:
            el.iface_expand_collapse.Expand()
            time.sleep(0.4)
        except Exception:
            pass
    except Exception as e:
        print('err expandir', nm, e, flush=True)

time.sleep(1)
ImageGrab.grab().save(EV + r'\pbi_fields_expanded.png')

print('=== CAMPOS (CheckBox) ===', flush=True)
seen2 = set()
for el in win.descendants(control_type='CheckBox'):
    try:
        if not el.is_visible():
            continue
        nm = el.element_info.name or ''
        r = el.rectangle()
        key = (nm, r.left, r.top)
        if key in seen2 or not nm.strip():
            continue
        seen2.add(key)
        print(repr(nm[:100]), 'rect=', r, flush=True)
    except Exception:
        pass

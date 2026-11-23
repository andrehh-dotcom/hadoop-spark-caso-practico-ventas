import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=15)
print('=== ARBOL DE TABLAS ===', flush=True)
seen = set()
for el in win.descendants(control_type='TreeItem'):
    try:
        if not el.is_visible():
            continue
        nm = el.element_info.name or ''
        if not nm.startswith('Table '):
            continue
        r = el.rectangle()
        key = (nm, r.left, r.top)
        if key in seen:
            continue
        seen.add(key)
        try:
            state = el.iface_expand_collapse.CurrentExpandCollapseState
        except Exception as e:
            state = 'ERR:' + str(e)[:30]
        print(repr(nm), 'top=', r.top, 'left=', r.left, 'state=', state, flush=True)
    except Exception:
        pass
print('=== CHECKBOXES ===', flush=True)
seen = set()
for el in win.descendants(control_type='CheckBox'):
    try:
        if not el.is_visible():
            continue
        nm = el.element_info.name or ''
        r = el.rectangle()
        key = (nm, r.left, r.top)
        if key in seen:
            continue
        seen.add(key)
        print(repr(nm[:70]), 'top=', r.top, flush=True)
    except Exception:
        pass

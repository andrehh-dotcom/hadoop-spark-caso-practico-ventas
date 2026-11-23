"""Lista los visuales y valores visibles en el canvas del informe."""
import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=15)
seen = set()
for el in win.descendants():
    try:
        i = el.element_info
        if not el.is_visible():
            continue
        nm = (i.name or '').strip()
        r = el.rectangle()
        if not nm or r.left > 1650 or r.top < 160:
            continue
        key = (i.control_type, nm, r.left, r.top)
        if key in seen:
            continue
        seen.add(key)
        if i.control_type in ('Text', 'DataItem', 'ListItem', 'Button'):
            print(i.control_type, repr(nm[:110]), 'rect=', r, flush=True)
    except Exception:
        pass

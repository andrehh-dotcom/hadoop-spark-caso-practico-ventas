import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window

w = main_window(timeout=15)
seen = set()
for e in w.descendants():
    try:
        i = e.element_info
        if not e.is_visible() or i.control_type != 'ListItem':
            continue
        nm = (i.name or '').strip()
        r = e.rectangle()
        if not nm or r.left < 1500:
            continue
        key = (nm, r.left, r.top)
        if key in seen:
            continue
        seen.add(key)
        print(repr(nm[:80]), 'rect=', r, flush=True)
    except Exception:
        pass

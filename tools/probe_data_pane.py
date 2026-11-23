import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=15)
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type in ('DataItem', 'ListItem', 'TreeItem', 'Text') and el.is_visible():
            nm = i.name or ''
            if nm.strip():
                print(i.control_type, repr(nm[:100]), 'aid=', i.automation_id,
                      'rect=', el.rectangle(), flush=True)
    except Exception:
        pass

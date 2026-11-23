import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=15)
for el in win.descendants(control_type='Edit'):
    try:
        if el.is_visible():
            print(repr((el.element_info.name or '')[:80]), 'aid=',
                  el.element_info.automation_id, 'rect=', el.rectangle(), flush=True)
    except Exception:
        pass

import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window

w = main_window(timeout=15)
btns = []
for e in w.descendants(control_type='Button'):
    try:
        if (e.is_visible() and (e.element_info.name or '')
                == 'Get data from other sources'):
            btns.append(e)
    except Exception:
        pass
print('botones:', len(btns), flush=True)
if btns:
    btns[0].click_input()
    time.sleep(4)
print('=== VENTANAS ===', flush=True)
for x in w.descendants(control_type='Window'):
    try:
        if x.is_visible():
            i = x.element_info
            print('WIN', repr((i.name or '')[:70]), (i.class_name or '')[:45],
                  i.automation_id, flush=True)
    except Exception:
        pass

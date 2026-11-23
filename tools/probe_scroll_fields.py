import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pywinauto import mouse
from pbi_ui import main_window
win = main_window(timeout=15)
mouse.scroll(coords=(1800, 700), wheel_dist=-5)
time.sleep(0.8)
for el in win.descendants(control_type='CheckBox'):
    try:
        if el.is_visible() and el.rectangle().left > 1600:
            print(repr((el.element_info.name or '')[:70]), 'top=', el.rectangle().top, flush=True)
    except Exception:
        pass

import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_focus import focus_powerbi
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
win = focus_powerbi()
for _ in range(6):
    send_keys('{ESC}')
    time.sleep(0.3)
time.sleep(1)
ImageGrab.grab().save(r'C:\hadoop-spark-cluster\evidencias\pbi_00_clean.png')
print('=== botones cinta ===')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type == 'Button' and el.is_visible():
            nm = i.name or ''
            if any(k in nm.lower() for k in ('get data', 'data', 'transform', 'table')):
                print(repr(nm[:90]), i.class_name, el.rectangle())
    except Exception:
        pass
print('=== ventanas ===')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type == 'Window' and el.is_visible():
            print('WINDOW', repr(i.name)[:80], i.class_name[:60], i.automation_id)
    except Exception:
        pass

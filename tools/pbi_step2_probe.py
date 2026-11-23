"""Explora el diálogo de archivo tras elegir Text/CSV."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import find, main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
win = main_window(timeout=15)
shot = lambda n: ImageGrab.grab().save(rf'{EV}\pbi_{n}.png')

try:
    gal = find(win, auto_id='DataSourceGalleryDialog', timeout=5)
except LookupError:
    gal = find(win, auto_id='DataSourceGalleryDialog', timeout=15)
item = find(gal, name='Text/CSV', control_type='DataItem', timeout=10)
item.click_input()
time.sleep(0.7)
shot('03_textcsv_selected')
connect = find(win, name='Connect', control_type='Button', timeout=10)
print('connect:', connect.rectangle())
connect.click_input()
time.sleep(2.5)
shot('04_filedialog')

print('=== ventanas ===')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type == 'Window' and el.is_visible():
            print('WINDOW', repr(i.name)[:80], i.class_name, i.automation_id, el.rectangle())
    except Exception:
        pass
print('=== combos/edits ===')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type in ('ComboBox', 'Edit') and el.is_visible():
            print(i.control_type, repr(i.name)[:80], i.automation_id, el.rectangle())
    except Exception:
        pass

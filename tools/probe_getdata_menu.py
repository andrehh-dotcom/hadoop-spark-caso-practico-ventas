import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import main_window, write, find

EV = r'C:\hadoop-spark-cluster\evidencias'
win = main_window(timeout=15)
win.set_focus()
time.sleep(0.5)

# Botón Get data del ribbon (el de la cinta, no el de la página de inicio)
target = None
for el in win.descendants(control_type='Button'):
    try:
        i = el.element_info
        if (i.name == 'Get data' and el.is_visible()
                and 'splitMenuButton' in (i.class_name or '')
                and i.rectangle().top < 160):
            target = el
            break
    except Exception:
        pass
print('ribbon Get data:', target is not None, target.rectangle() if target else '', flush=True)
if target:
    target.click_input()
    time.sleep(1.2)
ImageGrab.grab().save(EV + r'\pbi_getdata_menu.png')

print('=== items del menú ===', flush=True)
for el in win.descendants():
    try:
        i = el.element_info
        if el.is_visible() and i.control_type in ('ListItem', 'MenuItem', 'Button', 'DataItem'):
            nm = (i.name or '').strip()
            if nm and any(k in nm.lower() for k in ('text', 'csv', 'web', 'folder',
                                                    'excel', 'other', 'sql', 'json',
                                                    'get data', 'all')):
                print(i.control_type, repr(nm[:90]), i.automation_id, el.rectangle(), flush=True)
    except Exception:
        pass

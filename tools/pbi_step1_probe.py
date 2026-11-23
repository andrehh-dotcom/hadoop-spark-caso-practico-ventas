"""Explora el cuadro Get data de Power BI Desktop."""
import sys
import time
import subprocess
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import find, main_window, write
from pbi_focus import focus_powerbi

EXE = r'C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe'
EV = r'C:\hadoop-spark-cluster\evidencias'
try:
    win = focus_powerbi()
except RuntimeError:
    subprocess.Popen([EXE])
    for _ in range(60):
        time.sleep(1)
        try:
            win = focus_powerbi()
            break
        except RuntimeError:
            continue
    else:
        raise RuntimeError('Power BI no arrancó')
win = focus_powerbi()
win.set_focus()
time.sleep(0.5)
shot = lambda n: ImageGrab.grab().save(rf'{EV}\pbi_{n}.png')

search = find(win, auto_id='TellMe-SearchBox', timeout=20)
write(search, 'Get data')
time.sleep(1.0)
print('=== sugerencias Get data ===')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type == 'Button' and 'Get data' in (i.name or '') and el.is_visible():
            print(repr(i.name), i.class_name, el.rectangle())
    except Exception:
        pass

sugg = None
for el in win.descendants():
    try:
        i = el.element_info
        if (i.control_type == 'Button' and i.name == 'Get data'
                and 'splitPrimaryMenu' in (i.class_name or '') and el.is_visible()):
            sugg = el
            break
    except Exception:
        pass
if sugg is None:
    for el in win.descendants():
        try:
            i = el.element_info
            if i.control_type == 'Button' and i.name == 'Get data' and el.is_visible():
                sugg = el
                break
        except Exception:
            pass
print('sugerencia:', sugg is not None)
if sugg:
    sugg.click_input()
    time.sleep(1.5)
shot('01_getdata_menu')

for el in win.descendants():
    try:
        i = el.element_info
        if (i.control_type == 'Button' and 'other sources' in (i.name or '').lower()
                and el.is_visible()):
            print('other sources:', repr(i.name), el.rectangle())
            el.click_input()
            time.sleep(1.5)
            break
    except Exception:
        pass
shot('02_gallery')

print('=== galería ===')
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type == 'Window' and el.is_visible():
            print('WINDOW', repr(i.name), i.class_name, i.automation_id, el.rectangle())
    except Exception:
        pass
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type in ('DataItem', 'ListItem') and el.is_visible():
            print(i.control_type, repr(i.name)[:90], i.automation_id)
    except Exception:
        pass

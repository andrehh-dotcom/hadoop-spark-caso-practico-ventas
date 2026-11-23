import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pywinauto.keyboard import send_keys
from pbi_ui import main_window, write

w = main_window(timeout=15)
w.set_focus()
send_keys('{ESC}')
time.sleep(0.5)
send_keys('{ESC}')
time.sleep(0.5)

# TellMe: "Get data"
search = None
for e in w.descendants(control_type='Edit'):
    try:
        if (e.is_visible() and e.element_info.automation_id == 'TellMe-SearchBox'):
            search = e
            break
    except Exception:
        pass
print('tellme:', search is not None, flush=True)
search.click_input()
write(search, 'Get data')
time.sleep(1.2)

# Sugerencia splitPrimaryMenu
sugg = []
for e in w.descendants(control_type='Button'):
    try:
        if (e.is_visible() and (e.element_info.name or '') == 'Get data'
                and 'splitPrimaryMenu' in (e.element_info.class_name or '')
                and e.rectangle().top < 160):
            sugg.append(e)
    except Exception:
        pass
print('sugerencias:', len(sugg), flush=True)
if sugg:
    sugg[0].click_input()
    time.sleep(3)

for x in w.descendants(control_type='Window'):
    try:
        if x.is_visible():
            i = x.element_info
            print('WIN', repr((i.name or '')[:70]), i.automation_id, flush=True)
    except Exception:
        pass

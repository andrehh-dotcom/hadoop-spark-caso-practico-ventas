import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import main_window, write

EV = r'C:\hadoop-spark-cluster\evidencias'
win = main_window(timeout=15)
send_keys('{ESC}')
time.sleep(0.3)
search = [e for e in win.descendants(control_type='Edit')
          if e.is_visible() and e.element_info.automation_id == 'TellMe-SearchBox'][0]
write(search, 'Get data')
time.sleep(1.0)
sugg = [e for e in win.descendants(control_type='Button')
        if e.is_visible() and (e.element_info.name or '') == 'Get data'
        and 'splitPrimaryMenu' in (e.element_info.class_name or '')
        and e.rectangle().top < 160]
print('sugerencias:', len(sugg), flush=True)
if sugg:
    sugg[0].click_input()
time.sleep(1.2)
ImageGrab.grab().save(EV + r'\pbi_menu_after_load.png')

print('=== TODOS LOS CONTROLES VISIBLES RECIENTES ===', flush=True)
seen = set()
for el in win.descendants():
    try:
        i = el.element_info
        if not el.is_visible():
            continue
        nm = (i.name or '').strip()
        r = el.rectangle()
        if not nm or r.top > 400:
            continue
        key = (i.control_type, nm, r.left, r.top)
        if key in seen:
            continue
        seen.add(key)
        if i.control_type in ('Button', 'MenuItem', 'ListItem', 'DataItem', 'Text'):
            print(i.control_type, repr(nm[:100]), 'aid=', i.automation_id,
                  'cls=', (i.class_name or '')[:45], 'rect=', r, flush=True)
    except Exception:
        pass

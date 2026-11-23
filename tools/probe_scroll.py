import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pywinauto import mouse
from pbi_ui import main_window
win = main_window(timeout=15)


def show(tag):
    cbs = [e for e in win.descendants(control_type='CheckBox')
           if e.is_visible() and e.rectangle().left > 1600]
    tops = [e.rectangle().top for e in cbs]
    print(tag, 'n=', len(cbs), 'min/max=', (min(tops), max(tops)) if tops else None,
          'ultimos=', [e.element_info.name for e in cbs[-3:]], flush=True)


show('ANTES')
for dist in (-5, -5, -5):
    mouse.scroll(coords=(1800, 700), wheel_dist=dist)
    time.sleep(0.5)
    show('SCROLL ' + str(dist))
# Clic en el árbol de la última tabla visible
trees = [e for e in win.descendants(control_type='TreeItem')
         if e.is_visible() and (e.element_info.name or '').startswith('Table ')
         and e.rectangle().left == 1645]
for e in trees:
    if (e.element_info.name or '').strip() == 'Table ventas_por_producto':
        print('clic en', e.element_info.name, e.rectangle(), flush=True)
        e.click_input()
        time.sleep(0.8)
        break
show('TRAS CLIC')

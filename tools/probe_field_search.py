import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window, write
win = main_window(timeout=15)

search = None
cands = []
for el in win.descendants(control_type='Edit'):
    try:
        if el.is_visible() and (el.element_info.name or '') == 'Search' \
                and el.rectangle().left > 1600:
            cands.append(el)
    except Exception:
        pass
cands.sort(key=lambda e: e.rectangle().top)
print('candidatos:', [(e.rectangle().left, e.rectangle().top) for e in cands], flush=True)
if not cands:
    raise RuntimeError('sin search box')
search = cands[1] if len(cands) > 1 else cands[0]
print('usando:', search.rectangle(), flush=True)
search.click_input()
write(search, 'Total')
time.sleep(1.2)
print('=== CAMPOS TRAS BUSCAR Total ===', flush=True)
for el in win.descendants(control_type='CheckBox'):
    try:
        if el.is_visible() and el.rectangle().left > 1500:
            print(repr((el.element_info.name or '')[:70]), 'top=', el.rectangle().top, flush=True)
    except Exception:
        pass

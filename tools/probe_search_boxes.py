import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window, write
win = main_window(timeout=15)

boxes = []
for el in win.descendants(control_type='Edit'):
    try:
        if (el.is_visible() and (el.element_info.name or '') == 'Search'
                and el.element_info.automation_id != 'TellMe-SearchBox'):
            r = el.rectangle()
            if (r.left, r.top) not in [(b.rectangle().left, b.rectangle().top) for b in boxes]:
                boxes.append(el)
    except Exception:
        pass
print('buscadores:', [(b.rectangle().left, b.rectangle().top) for b in boxes], flush=True)


def cbcount():
    return len([e for e in win.descendants(control_type='CheckBox')
                if e.is_visible() and e.rectangle().left > 1600])


base = cbcount()
print('base:', base, flush=True)
for b in boxes:
    r = b.rectangle()
    try:
        b.click_input()
        write(b, 'Total')
        time.sleep(1.0)
        n = cbcount()
        names = [e.element_info.name for e in win.descendants(control_type='CheckBox')
                 if e.is_visible() and e.rectangle().left > 1600][-4:]
        print('box', r.left, r.top, '->', n, names, flush=True)
        b.click_input()
        write(b, '')
        time.sleep(0.6)
    except Exception as e:
        print('err', r, e, flush=True)

"""Cierra todos los diálogos visibles de Power BI pulsando sus botones."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window

win = main_window(timeout=15)
for _ in range(6):
    found = False
    for el in list(win.descendants(control_type='Window')):
        try:
            i = el.element_info
            if i.automation_id == 'MainWindow' or not el.is_visible():
                continue
            print('cerrando', repr(i.name)[:50], flush=True)
            for label in ('Cancelar', 'Cancel', 'Close Dialog'):
                try:
                    btn = el.descendant(control_type='Button', title=label)
                    btn.click_input()
                    found = True
                    break
                except Exception:
                    continue
            time.sleep(0.5)
        except Exception:
            pass
    if not found:
        break
time.sleep(1)

"""Cierra cuadros modales secundarios de Power BI Desktop."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window

win = main_window(timeout=15)
for _ in range(8):
    changed = False
    for el in list(win.descendants(control_type='Window')):
        try:
            i = el.element_info
            if i.automation_id in ('MainWindow', '') or not el.is_visible():
                continue
            print('cerrando:', repr(i.name)[:70], i.class_name, i.automation_id, flush=True)
            for label in ('Cancelar', 'Cancel', 'Close', 'Cerrar'):
                try:
                    btn = el.descendant(control_type='Button', title=label)
                    btn.click_input()
                    changed = True
                    break
                except Exception:
                    continue
            if not changed:
                try:
                    el.close()
                    changed = True
                except Exception:
                    pass
            time.sleep(0.6)
        except Exception:
            pass
    if not changed:
        break
time.sleep(1)

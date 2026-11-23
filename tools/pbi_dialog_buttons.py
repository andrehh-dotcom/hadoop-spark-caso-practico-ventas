import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=10)
for el in win.descendants(control_type='Window'):
    try:
        i = el.element_info
        if not el.is_visible() or i.automation_id == 'MainWindow':
            continue
        print('=== DIALOGO', repr(i.name)[:70], i.class_name, i.automation_id, el.rectangle(), flush=True)
        for ch in el.descendants(control_type='Button'):
            try:
                if ch.is_visible():
                    print('  BTN', repr(ch.element_info.name)[:60], ch.element_info.automation_id, ch.rectangle(), flush=True)
            except Exception:
                pass
    except Exception:
        pass

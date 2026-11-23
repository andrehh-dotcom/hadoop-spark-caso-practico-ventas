import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=10)
print('titulo:', win.window_text())
for el in win.descendants():
    try:
        i = el.element_info
        if i.control_type == 'Window' and el.is_visible():
            print('WINDOW', repr(i.name)[:90], i.class_name, i.automation_id, el.rectangle())
    except Exception:
        pass

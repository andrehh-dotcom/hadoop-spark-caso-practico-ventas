import sys, time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pbi_ui import main_window
win = main_window(timeout=10)
time.sleep(3)
ImageGrab.grab().save(r'C:\hadoop-spark-cluster\evidencias\pbi_gallery_state.png')
for el in win.descendants(control_type='Window'):
    try:
        i = el.element_info
        if 'DataSource' in (i.class_name or '') or i.automation_id == 'DataSourceGalleryDialog':
            print('GAL', repr(i.name)[:60], i.class_name, i.automation_id, el.rectangle())
            for ch in el.descendants():
                try:
                    ci = ch.element_info
                    if ci.control_type in ('Edit', 'DataItem', 'Button') and ch.is_visible():
                        print(' ', ci.control_type, repr(ci.name)[:60], ci.automation_id)
                except Exception:
                    pass
    except Exception:
        pass

"""Sonda del estado actual de Power BI Desktop."""
import sys
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window, dump
from pywinauto import Desktop

print('=== Ventanas ===')
for w in Desktop(backend='uia').windows():
    try:
        if w.is_visible() and w.rectangle().width() > 200:
            print(repr(w.window_text()[:90]), w.class_name(), w.rectangle())
    except Exception:
        pass
print('=== PBI ===')
win = main_window(timeout=15)
print('titulo:', repr(win.window_text()), 'rect:', win.rectangle())
dump(win, depth=4, max_lines=120)

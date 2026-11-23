import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window
win = main_window(timeout=15)

for el in win.descendants(control_type='TreeItem'):
    try:
        if not el.is_visible():
            continue
        if (el.element_info.name or '').strip() == 'Table ventas_por_producto_mr':
            print('clic en', el.rectangle(), flush=True)
            el.click_input()
            time.sleep(1.2)
            break
    except Exception:
        pass
print('=== CAMPOS ===', flush=True)
for el in win.descendants(control_type='CheckBox'):
    try:
        if el.is_visible() and el.rectangle().left > 1600:
            nm = el.element_info.name or ''
            if 'Total' in nm or 'Ventas' in nm or 'Producto' in nm or 'count' in nm:
                print(repr(nm[:70]), 'top=', el.rectangle().top, flush=True)
    except Exception:
        pass

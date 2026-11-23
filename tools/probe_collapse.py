"""Colapsa todas las tablas salvo una y comprueba si sus campos aparecen."""
import sys
import time
sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from pbi_ui import main_window

STEM = sys.argv[1] if len(sys.argv) > 1 else 'ventas_por_producto_mr'
win = main_window(timeout=15)

# Panel activo = el que contiene los checkbox de campos (x > 1600)
cbs = [e for e in win.descendants(control_type='CheckBox')
       if e.is_visible() and e.rectangle().left > 1600
       and (e.element_info.name or '').startswith(('Numeric Field', ' '))]
print('checkboxes de campos:', len(cbs),
      'x=', sorted(set(c.rectangle().left for c in cbs)), flush=True)

trees = [e for e in win.descendants(control_type='TreeItem')
         if e.is_visible() and (e.element_info.name or '').startswith('Table ')]
# Elegir el grupo de árbol cuya x esté más cerca de los campos (1784 - 139)
cb_x = cbs[0].rectangle().left if cbs else 1784
groups = {}
for e in trees:
    groups.setdefault(e.rectangle().left, []).append(e)
print('grupos:', {k: len(v) for k, v in groups.items()}, flush=True)
pane_left = min(groups, key=lambda k: abs((cb_x - 139) - k))
print('panel elegido:', pane_left, flush=True)

for el in groups[pane_left]:
    nm = el.element_info.name or ''
    if nm.strip() == 'Table ' + STEM:
        continue
    try:
        if el.iface_expand_collapse.CurrentExpandCollapseState == 1:
            el.iface_expand_collapse.Collapse()
            time.sleep(0.2)
    except Exception:
        pass
time.sleep(1)
for el in groups[pane_left]:
    nm = el.element_info.name or ''
    try:
        if nm.strip() == 'Table ' + STEM and el.iface_expand_collapse.CurrentExpandCollapseState != 1:
            el.iface_expand_collapse.Expand()
    except Exception:
        pass
time.sleep(1)
print('=== CAMPOS TRAS COLAPSO ===', flush=True)
for el in win.descendants(control_type='CheckBox'):
    try:
        if el.is_visible() and el.rectangle().left > 1600:
            print(repr((el.element_info.name or '')[:60]), 'top=', el.rectangle().top, flush=True)
    except Exception:
        pass

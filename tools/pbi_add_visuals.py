"""Añade visuales al informe Dashboard_Ventas vía GUI de Power BI Desktop.

Uso: python tools/pbi_add_visuals.py [índice]
Cada ejecución añade un visual, guarda (Ctrl+S) y registra el progreso.
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto import mouse
from pywinauto.keyboard import send_keys
from pbi_ui import main_window

EV = r'C:\hadoop-spark-cluster\evidencias'
STATE = r'C:\hadoop-spark-cluster\tools\.visual_progress.txt'

# (etiqueta, tipo de visual, tabla, [(campo UIA, rol)], (x, y) en el canvas)
SPECS = [
    ('KPI Total vendido', 'Card', 'resumen_general',
     [('Numeric Field TotalVendido', 'value')], (340, 260)),
    ('KPI Numero de ventas', 'Card', 'resumen_general',
     [('Numeric Field NumVentas', 'value')], (570, 260)),
    ('KPI Ticket promedio', 'Card', 'resumen_general',
     [('Numeric Field TicketPromedio', 'value')], (800, 260)),
    ('KPI Porcentaje ventas altas', 'Card', 'resumen_general',
     [('Numeric Field PctVentasAltas', 'value')], (1030, 260)),
    ('Ventas por producto', 'Clustered column chart', 'ventas_por_producto',
     [('Numeric Field TotalVendido', 'value'), (' Producto', 'category')], (340, 560)),
    ('Ventas por cliente', 'Clustered column chart', 'ventas_por_cliente',
     [('Numeric Field TotalVendido', 'value'), (' Cliente', 'category')], (790, 560)),
    ('Evolucion mensual', 'Line chart', 'ventas_por_mes',
     [('Numeric Field TotalVendido', 'value'), (' Mes', 'category')], (340, 860)),
    ('Detalle ventas altas', 'Table', 'ventas_altas',
     [('Numeric Field Monto', 'value'), (' Cliente', 'category'),
      (' Producto', 'category'), (' Ciudad', 'category')], (790, 860)),
    ('Resultado MapReduce por producto', 'Clustered column chart',
     'ventas_por_producto_mr',
     [('Numeric Field Total', 'value'), (' Producto', 'category')], (340, 990)),
    ('Palabras frecuentes en comentarios', 'Clustered bar chart',
     'palabras_comentarios',
     [('Numeric Field count', 'value'), (' palabra', 'category')], (790, 990)),
]


def log(msg):
    print('[visual] ' + msg, flush=True)


def visible_by(win, **kw):
    ct = kw.pop('control_type', None)
    nm = kw.pop('name', None)
    out = []
    for el in win.descendants():
        try:
            i = el.element_info
            if not el.is_visible():
                continue
            if ct and i.control_type != ct:
                continue
            if nm and (i.name or '').strip() != nm:
                continue
            out.append(el)
        except Exception:
            pass
    return out


def expand_all_tables(win):
    """Expande todas las tablas del panel Data sin colapsar ninguna."""
    seen = set()
    for el in visible_by(win, control_type='TreeItem'):
        try:
            nm = el.element_info.name or ''
            if not nm.startswith('Table '):
                continue
            r = el.rectangle()
            key = (nm, r.left, r.top)
            if key in seen:
                continue
            seen.add(key)
            try:
                if el.iface_expand_collapse.CurrentExpandCollapseState != 1:
                    el.iface_expand_collapse.Expand()
                    time.sleep(0.3)
            except Exception:
                if r.left > 1500:
                    el.click_input()
                    time.sleep(0.2)
        except Exception:
            pass
    time.sleep(0.5)


def table_bounds(win, stem):
    """Devuelve (top, bottom) de la tabla objetivo en el panel Data."""
    toc = []
    for el in visible_by(win, control_type='TreeItem'):
        try:
            nm = el.element_info.name or ''
            if nm.startswith('Table '):
                toc.append((el.rectangle().top, nm.strip(), el.rectangle().left))
        except Exception:
            pass
    toc = sorted(set(toc))
    targets = [t for t in toc if t[1] == 'Table ' + stem]
    if not targets:
        return None
    top = targets[0][0]
    later = [t[0] for t in toc if t[0] > top]
    return (top, min(later) if later else top + 200)


def data_search_box(win):
    for el in win.descendants(control_type='Edit'):
        try:
            if (el.is_visible() and (el.element_info.name or '') == 'Search'
                    and el.element_info.automation_id != 'TellMe-SearchBox'
                    and el.rectangle().left > 1600):
                return el
        except Exception:
            pass
    return None


def field_checkbox(win, field_name, stem=None):
    """Localiza el checkbox del campo, filtrando el panel Data si hace falta."""
    def candidates():
        hits = [e for e in visible_by(win, control_type='CheckBox')
                if (e.element_info.name or '') == field_name]
        if stem and hits:
            bounds = table_bounds(win, stem)
            if bounds:
                lo, hi = bounds
                in_table = [e for e in hits if lo <= e.rectangle().top < hi]
                if in_table:
                    return in_table
        return hits

    hits = candidates()
    if hits:
        return hits[0]

    # Buscar por nombre en el cuadro de búsqueda del panel Data
    box = data_search_box(win)
    if box is None:
        raise RuntimeError('sin buscador en el panel Data')
    term = field_name.replace('Numeric Field', '').strip()
    box.click_input()
    from pbi_ui import write
    write(box, term)
    time.sleep(1.0)
    hits = candidates()
    if not hits:
        # Fallback: primer checkbox con el término en el nombre
        hits = [e for e in visible_by(win, control_type='CheckBox')
                if term.lower() in (e.element_info.name or '').lower()]
    if hits:
        log('campo encontrado filtrando por ' + repr(term))
        box.click_input()
        write(box, '')
        time.sleep(0.5)
        return hits[0]
    box.click_input()
    write(box, '')
    raise RuntimeError('campo no visible: ' + repr(field_name))


def visual_type_item(win, vtype):
    hits = [e for e in visible_by(win, control_type='ListItem')
            if (e.element_info.name or '').strip() == vtype]
    if not hits:
        raise RuntimeError('tipo de visual no visible: ' + vtype)
    return hits[0]


def add_one(win, idx):
    label, vtype, table, fields, (x, y) = SPECS[idx]
    log('%s -> %s / %s' % (label, vtype, table))
    send_keys('{ESC}')
    time.sleep(0.3)

    expand_all_tables(win)
    time.sleep(0.4)

    # Crear un visual nuevo haciendo clic en un área libre del canvas
    mouse.click(coords=(x, y))
    time.sleep(0.8)

    for pos, (field, role) in enumerate(fields):
        cb = field_checkbox(win, field, table)
        cb.click_input()
        time.sleep(1.8)
        if pos == 0:
            item = visual_type_item(win, vtype)
            item.click_input()
            time.sleep(1.5)

    # Guardar
    send_keys('{ESC}')
    time.sleep(0.3)
    send_keys('^s')
    time.sleep(3)
    ImageGrab.grab().save(os.path.join(EV, 'pbi_visual_%02d.png' % (idx + 1)))
    log('guardado: ' + label)


def main():
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    if not 0 <= idx < len(SPECS):
        raise RuntimeError('índice fuera de rango')
    done = []
    if os.path.exists(STATE):
        done = [int(x.strip()) for x in open(STATE, encoding='utf-8') if x.strip()]
    if idx in done:
        log('índice %d ya completado' % idx)
        return
    win = main_window(timeout=20)
    log('ventana: ' + win.window_text())
    add_one(win, idx)
    with open(STATE, 'a', encoding='utf-8') as h:
        h.write('%d\n' % idx)
    log('progreso: ' + str(sorted(set(done + [idx]))))


if __name__ == '__main__':
    main()

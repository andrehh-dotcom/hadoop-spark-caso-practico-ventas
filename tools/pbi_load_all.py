"""Carga todos los CSV del caso práctico en Power BI Desktop vía GUI.

Flujo por archivo:
  TellMe "Get data" -> sugerencia splitPrimaryMenu -> "Get data from other sources"
  -> galería Text/CSV -> Connect -> cuadro Abrir (ruta) -> Enter
  -> ImportFromTextDialog -> Load.

Uso: python tools/pbi_load_all.py [csv1 csv2 ...]
"""
from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, r'C:\hadoop-spark-cluster\tools')
from PIL import ImageGrab
from pywinauto.keyboard import send_keys
from pbi_ui import main_window, write

EV = r'C:\hadoop-spark-cluster\evidencias'
DATA = r'C:\hadoop-spark-cluster\powerbi'
DEFAULT = [
    'ventas_altas.csv',
    'ventas_por_producto.csv',
    'ventas_por_cliente.csv',
    'ventas_por_mes.csv',
    'palabras_comentarios.csv',
    'ventas_por_producto_mr.csv',
]


def log(msg):
    print('[load] ' + msg, flush=True)


def visible_by(win, *, name=None, name_contains=None, control_type=None,
               class_contains=None, auto_id=None, top_max=None):
    out = []
    for el in win.descendants():
        try:
            i = el.element_info
            if not el.is_visible():
                continue
            nm = i.name or ''
            if name is not None and nm.strip() != name:
                continue
            if name_contains is not None and name_contains.lower() not in nm.lower():
                continue
            if control_type is not None and i.control_type != control_type:
                continue
            if class_contains is not None and class_contains not in (i.class_name or ''):
                continue
            if auto_id is not None and i.automation_id != auto_id:
                continue
            if top_max is not None and el.rectangle().top > top_max:
                continue
            out.append(el)
        except Exception:
            pass
    return out


def wait_for(fn, timeout=12, interval=0.6, label=''):
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = fn()
        if r:
            return r
        time.sleep(interval)
    raise RuntimeError('timeout: ' + label)


def table_exists(win, stem):
    return any('Table ' + stem in (e.element_info.name or '')
               for e in visible_by(win, control_type='TreeItem'))


def close_transient_dialogs(win):
    """Cierra los cuadros #32770 y de importación que queden abiertos."""
    for el in list(win.descendants(control_type='Window')):
        try:
            if not el.is_visible():
                continue
            cls = el.element_info.class_name or ''
            aid = el.element_info.automation_id or ''
            if cls == '#32770' or aid == 'ImportFromTextDialog':
                btns = [b for b in el.descendants(control_type='Button')
                        if b.is_visible() and (b.element_info.name or '') in
                        ('Cancelar', 'Cancel', 'Close')]
                if btns:
                    btns[-1].click_input()
                    time.sleep(0.5)
                    log('cerrado diálogo: ' + (el.element_info.name or aid))
        except Exception:
            pass


def find_gallery_window(win):
    """La galería puede venir como DataSourceGalleryDialog o como diálogo 'Get Data'."""
    for el in visible_by(win, control_type='Window'):
        i = el.element_info
        if i.automation_id == 'DataSourceGalleryDialog' or (i.name or '') == 'Get Data':
            if any(c.is_visible() and (c.element_info.name or '') == 'Text/CSV'
                   and c.element_info.control_type == 'DataItem'
                   for c in el.descendants()):
                return el
    return None


def open_gallery(win):
    # Si ya está abierta (por un sondeo), reutilizarla
    existing = find_gallery_window(win)
    if existing:
        log('galería ya abierta, reutilizando')
        return existing

    send_keys('{ESC}')
    time.sleep(0.3)

    # En la página de inicio hay acceso directo a la galería
    direct = visible_by(win, name='Get data from other sources', control_type='Button')
    if direct:
        log('usando acceso directo de la página de inicio')
        direct[0].click_input()
    else:
        search = visible_by(win, auto_id='TellMe-SearchBox', control_type='Edit')
        if not search:
            raise RuntimeError('TellMe-SearchBox no visible')
        search[0].click_input()
        write(search[0], 'Get data')
        time.sleep(1.0)

        def find_suggestion():
            return visible_by(win, name='Get data', control_type='Button',
                              class_contains='splitPrimaryMenu', top_max=160)

        sugg = wait_for(find_suggestion, timeout=10, label='sugerencia Get data')
        sugg[0].click_input()

    gal = wait_for(lambda: find_gallery_window(win), timeout=20, label='galería Get Data')
    return gal


def load_one(win, filename, tag):
    path = os.path.join(DATA, filename)
    stem = os.path.splitext(filename)[0]
    if not os.path.exists(path):
        raise RuntimeError('no existe ' + path)
    if table_exists(win, stem):
        log('ya cargada: ' + stem)
        return

    log('abriendo galería para ' + filename)
    gal = open_gallery(win)
    ImageGrab.grab().save(os.path.join(EV, 'pbi_%s_01_gallery.png' % tag))

    items = [e for e in gal.descendants(control_type='DataItem')
             if e.is_visible() and (e.element_info.name or '') == 'Text/CSV']
    if not items:
        # La galería puede cargar tarde: reintentar dentro del mismo diálogo
        items = wait_for(lambda: [e for e in gal.descendants(control_type='DataItem')
                                  if e.is_visible()
                                  and (e.element_info.name or '') == 'Text/CSV'],
                         timeout=12, label='Text/CSV en galería')
    items[0].click_input()
    time.sleep(0.5)

    conn = visible_by(win, name='Connect', control_type='Button')
    if not conn:
        raise RuntimeError('botón Connect no visible')
    conn[0].click_input()
    time.sleep(1.8)

    def find_filedlg():
        return visible_by(win, control_type='Window', class_contains='#32770')

    dlg = wait_for(find_filedlg, timeout=10, label='cuadro Abrir')[0]
    edits = [e for e in dlg.descendants(control_type='Edit')
             if e.element_info.automation_id == '1148']
    if not edits:
        raise RuntimeError('campo Nombre de archivo no encontrado')
    edit = edits[0]
    edit.click_input()
    edit.set_edit_text(path)
    time.sleep(0.4)
    ImageGrab.grab().save(os.path.join(EV, 'pbi_%s_02_path.png' % tag))
    send_keys('{ENTER}')
    time.sleep(3.5)

    def find_import():
        return visible_by(win, auto_id='ImportFromTextDialog', control_type='Window')

    imp = wait_for(find_import, timeout=15, label='ImportFromTextDialog')[0]
    ImageGrab.grab().save(os.path.join(EV, 'pbi_%s_03_import.png' % tag))
    loads = [b for b in imp.descendants(control_type='Button')
             if b.is_visible() and (b.element_info.name or '') == 'Load']
    if not loads:
        raise RuntimeError('botón Load no visible')
    loads[0].click_input()
    time.sleep(9)
    ImageGrab.grab().save(os.path.join(EV, 'pbi_%s_04_loaded.png' % tag))
    if not table_exists(win, stem):
        raise RuntimeError('la tabla ' + stem + ' no apareció en el modelo')
    log('CARGADA: ' + stem)


def main():
    win = main_window(timeout=20)
    log('ventana: ' + win.window_text())
    close_transient_dialogs(win)
    files = sys.argv[1:] or DEFAULT
    for filename in files:
        tag = os.path.splitext(filename)[0]
        load_one(win, filename, tag)
    log('TODAS LAS TABLAS CARGADAS')
    log('tablas: ' + ', '.join(sorted(
        (e.element_info.name or '').replace('Table ', '')
        for e in visible_by(win, control_type='TreeItem')
        if (e.element_info.name or '').startswith('Table '))))


if __name__ == '__main__':
    main()

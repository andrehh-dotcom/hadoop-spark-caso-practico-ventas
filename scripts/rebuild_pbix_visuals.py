"""Reconstruye los 10 visuales del informe Dashboard_Ventas.pbix en formato PBIR.

La automatización GUI acumulaba campos en el mismo visual, dejando solo 3 visuales
con campos mezclados. Este script genera definiciones limpias, una por visual,
usando como plantilla el esquema real que Power BI guardó en el propio PBIX.
"""
from __future__ import annotations

import json
import os
import shutil
import uuid
import zipfile

PBIX = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'
BACKUP = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pre_rebuild.pbix'
PAGE_DIR = 'Report/definition/pages/27d1bee38f56bf51d8f3'
SCHEMA = ('https://developer.microsoft.com/json-schemas/fabric/item/report/'
          'definition/visualContainer/2.14.0/schema.json')


def col(entity, prop):
    return {
        'Column': {
            'Expression': {'SourceRef': {'Entity': entity}},
            'Property': prop,
        }
    }


def agg(entity, prop):
    return {'Aggregation': {'Expression': col(entity, prop), 'Function': 0}}


class Refs:
    """Genera nativeQueryRef únicos (Power BI agrega sufijos 1, 2, ...)."""

    def __init__(self):
        self.used = {}

    def native(self, name):
        n = self.used.get(name, 0)
        self.used[name] = n + 1
        return name if n == 0 else '%s%d' % (name, n)

    def column(self, entity, prop):
        return Refs._proj(col(entity, prop),
                          '%s.%s' % (entity, prop),
                          self.native(prop))

    def measure(self, entity, prop):
        return Refs._proj(agg(entity, prop),
                          'Sum(%s.%s)' % (entity, prop),
                          self.native('Sum of ' + prop))

    @staticmethod
    def _proj(field, qref, native):
        return {'field': field, 'queryRef': qref, 'nativeQueryRef': native}


def filt(field):
    """Filtro de visual acorde al tipo de campo."""
    kind = 'Advanced' if 'Aggregation' in field else 'Categorical'
    return {
        'name': uuid.uuid4().hex[:20],
        'field': field,
        'type': kind,
    }


def visual(name, vtype, x, y, w, h, z, roles):
    """Construye un visual.json completo a partir de roles -> proyecciones."""
    refs = Refs()
    state = {}
    all_fields = []
    for role, items in roles.items():
        projections = []
        for kind, entity, prop in items:
            p = refs.measure(entity, prop) if kind == 'm' else refs.column(entity, prop)
            projections.append(p)
            all_fields.append(p['field'])
        state[role] = {'projections': projections}

    sort_field = None
    for role in ('Y', 'Data', 'Values'):
        if state.get(role, {}).get('projections'):
            sort_field = state[role]['projections'][0]['field']
            break

    query = {'queryState': state}
    if sort_field is not None:
        query['sortDefinition'] = {
            'sort': [{'field': sort_field, 'direction': 'Descending'}],
            'isDefaultSort': True,
        }

    return {
        '$schema': SCHEMA,
        'name': name,
        'position': {
            'x': x, 'y': y, 'z': z,
            'height': h, 'width': w, 'tabOrder': z,
        },
        'visual': {
            'visualType': vtype,
            'query': query,
            'drillFilterOtherVisuals': True,
        },
        'filterConfig': {'filters': [filt(f) for f in all_fields]},
    }


# (id, tipo, x, y, ancho, alto, roles)
# roles: 'm' = medida (Sum), 'c' = columna categórica
SPECS = [
    ('kpi_total',     'cardVisual',           20,  20, 280, 180,
     {'Data': [('m', 'resumen_general', 'TotalVendido')]}),
    ('kpi_ventas',    'cardVisual',          320,  20, 280, 180,
     {'Data': [('m', 'resumen_general', 'NumVentas')]}),
    ('kpi_ticket',    'cardVisual',          620,  20, 280, 180,
     {'Data': [('m', 'resumen_general', 'TicketPromedio')]}),
    ('kpi_pct',       'cardVisual',          920,  20, 280, 180,
     {'Data': [('m', 'resumen_general', 'PctVentasAltas')]}),
    ('ventas_producto', 'clusteredColumnChart', 20, 230, 600, 390,
     {'Category': [('c', 'ventas_por_producto', 'Producto')],
      'Y': [('m', 'ventas_por_producto', 'TotalVendido')]}),
    ('ventas_cliente', 'clusteredColumnChart', 660, 230, 600, 390,
     {'Category': [('c', 'ventas_por_cliente', 'Cliente')],
      'Y': [('m', 'ventas_por_cliente', 'TotalVendido')]}),
    ('mapreduce',     'clusteredColumnChart', 1300, 230, 600, 390,
     {'Category': [('c', 'ventas_por_producto_mr', 'Producto')],
      'Y': [('m', 'ventas_por_producto_mr', 'Total')]}),
    ('evolucion',     'lineChart',             20, 650, 600, 390,
     {'Category': [('c', 'ventas_por_mes', 'Mes')],
      'Y': [('m', 'ventas_por_mes', 'TotalVendido')]}),
    ('detalle',       'tableEx',              660, 650, 600, 390,
     {'Values': [('m', 'ventas_altas', 'Monto'),
                 ('c', 'ventas_altas', 'Cliente'),
                 ('c', 'ventas_altas', 'Producto'),
                 ('c', 'ventas_altas', 'Ciudad')]}),
    ('palabras',      'clusteredBarChart',   1300, 650, 600, 390,
     {'Category': [('c', 'palabras_comentarios', 'palabra')],
      'Y': [('m', 'palabras_comentarios', 'count')]}),
]


def main():
    if not os.path.exists(PBIX):
        raise RuntimeError('No existe ' + PBIX)
    if not os.path.exists(BACKUP):
        shutil.copy2(PBIX, BACKUP)
        print('backup:', BACKUP, os.path.getsize(BACKUP), flush=True)

    tmp = PBIX + '.tmp'
    with zipfile.ZipFile(PBIX, 'r') as zin:
        items = [(i, zin.read(i.filename)) for i in zin.infolist()]

    # Sustituir todos los visuales anteriores por los nuevos
    prefix = PAGE_DIR + '/visuals/'
    kept = [(i, data) for i, data in items
            if not (i.filename.startswith(prefix)
                    and i.filename.endswith('visual.json'))]

    visuals = {}
    for z, (vid, vtype, x, y, w, h, roles) in enumerate(SPECS):
        # Power BI espera una única carpeta cuyo nombre es el GUID del visual,
        # coincidente con el campo "name" del visual.json.
        guid = uuid.uuid4().hex[:20]
        folder = prefix + guid + '/'
        obj = visual(guid, vtype, x, y, w, h, z, roles)
        visuals[folder + 'visual.json'] = json.dumps(
            obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

    names = [i.filename for i, _ in kept]
    for n in visuals:
        if n in names:
            raise RuntimeError('nombre duplicado: ' + n)

    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for info, data in kept:
            zout.writestr(info.filename, data)
        for n, data in visuals.items():
            zout.writestr(n, data)

    os.replace(tmp, PBIX)
    print('RECONSTRUIDO:', PBIX, os.path.getsize(PBIX), flush=True)
    print('VISUALES:', len(visuals), flush=True)
    for n in sorted(visuals):
        print('  ', n, flush=True)


if __name__ == '__main__':
    main()

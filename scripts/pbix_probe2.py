"""Variantes adicionales para aislar el rechazo de Power BI al añadir visuales."""
import copy
import json
import os
import uuid
import zipfile

SRC = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pre_rebuild.pbix'
OUT = r'C:\hadoop-spark-cluster\powerbi\probe'
os.makedirs(OUT, exist_ok=True)

with zipfile.ZipFile(SRC, 'r') as z:
    base = [(i.filename, z.read(i.filename)) for i in z.infolist()]

vfiles = [(n, d) for n, d in base if n.endswith('visual.json')]
name0, data0 = vfiles[0]
orig = json.loads(data0.decode('utf-8'))
old_folder = os.path.dirname(name0)


def add(name_suffix, obj, insert_after_visuals=True):
    guid = uuid.uuid4().hex[:20]
    obj = copy.deepcopy(obj)
    obj['name'] = guid
    new_folder = old_folder.rsplit('/', 1)[0] + '/' + guid
    new_name = new_folder + '/visual.json'
    items = []
    added = False
    for n, d in base:
        items.append((n, d))
        if insert_after_visuals and n == vfiles[-1][0] and not added:
            items.append((new_name, json.dumps(
                obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8')))
            added = True
    if not added:
        items.append((new_name, json.dumps(
            obj, ensure_ascii=False, separators=(',', ':')).encode('utf-8')))
    p = os.path.join(OUT, name_suffix + '.pbix')
    with zipfile.ZipFile(p, 'w', zipfile.ZIP_DEFLATED) as z:
        for n, d in items:
            z.writestr(n, d)
    print(name_suffix, os.path.getsize(p), flush=True)


# D: clon con nombres de filtro nuevos
d = copy.deepcopy(orig)
for f in d.get('filterConfig', {}).get('filters', []):
    f['name'] = uuid.uuid4().hex[:20]
add('D_clone_newfilters', d)

# E: visual mínimo (sin query ni filtros)
e = {
    '$schema': orig['$schema'],
    'name': 'placeholder',
    'position': {'x': 1300, 'y': 0, 'z': 3, 'height': 280,
                 'width': 280, 'tabOrder': 3},
    'visual': {'visualType': 'cardVisual',
               'query': {'queryState': {}},
               'drillFilterOtherVisuals': True},
    'filterConfig': {'filters': []},
}
add('E_minimal', e)

# F: clon exacto pero con posición z=3
f = copy.deepcopy(orig)
f['position'] = {'x': 1300, 'y': 0, 'z': 3, 'height': 280,
                 'width': 280, 'tabOrder': 3}
add('F_clone_pos', f)

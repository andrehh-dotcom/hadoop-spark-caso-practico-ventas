"""Genera variantes controladas del PBIX para aislar por qué Power BI lo rechaza."""
import json
import os
import shutil
import uuid
import zipfile

SRC = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pre_rebuild.pbix'
OUT = r'C:\hadoop-spark-cluster\powerbi\probe'
os.makedirs(OUT, exist_ok=True)


def read_items(path):
    with zipfile.ZipFile(path, 'r') as z:
        return [(i.filename, z.read(i.filename)) for i in z.infolist()]


def write_items(path, items):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            z.writestr(name, data)
    print('escrito:', path, os.path.getsize(path), flush=True)


base = read_items(SRC)
vfiles = [(n, d) for n, d in base if n.endswith('visual.json')]
print('visuales originales:', len(vfiles), flush=True)

# Prueba A: re-zip sin cambios
write_items(os.path.join(OUT, 'A_rezip.pbix'), base)

# Prueba B: clonar el primer visual exacto con otro GUID
name0, data0 = vfiles[0]
obj = json.loads(data0.decode('utf-8'))
new_guid = uuid.uuid4().hex[:20]
obj['name'] = new_guid
new_name = name0.replace(os.path.basename(os.path.dirname(name0)), new_guid)
items_b = base + [(new_name, json.dumps(obj, ensure_ascii=False,
                                         separators=(',', ':')).encode('utf-8'))]
write_items(os.path.join(OUT, 'B_clone.pbix'), items_b)

# Prueba C: re-zip conservando la compresión original de cada entrada
def write_items_preserve(path, src, items):
    with zipfile.ZipFile(path, 'w') as z:
        with zipfile.ZipFile(src, 'r') as zs:
            info_map = {i.filename: i for i in zs.infolist()}
        for name, data in items:
            orig = info_map.get(name)
            if orig:
                zi = zipfile.ZipInfo(name, date_time=orig.date_time)
                zi.compress_type = orig.compress_type
                zi.external_attr = orig.external_attr
            else:
                zi = zipfile.ZipInfo(name)
                zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)

write_items_preserve(os.path.join(OUT, 'C_preserve.pbix'), SRC, base)

"""Verifica el contenido del PBIX final: tablas y visuales."""
import json
import os
import zipfile

p = r'C:\hadoop-spark-cluster\powerbi\Dashboard_Ventas.pbix'
print('archivo:', p, os.path.getsize(p))
z = zipfile.ZipFile(p)
names = z.namelist()
print('entradas:', len(names))
for n in names:
    if 'definition' in n and n.endswith('.json'):
        print('---', n)
        s = z.read(n).decode('utf-8', 'replace')
        try:
            obj = json.loads(s)
            print(json.dumps(obj, indent=2, ensure_ascii=False)[:1500])
        except Exception:
            print(s[:1500])

# Contar visuales en los JSON de página
vis = 0
for n in names:
    if n.endswith('page.json'):
        s = z.read(n).decode('utf-8', 'replace')
        vis += s.count('"visualType"')
print('VISUALES ENCONTRADOS:', vis)

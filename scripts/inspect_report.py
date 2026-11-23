import zipfile, json
for p in [r'C:\Users\USUARIO\Documents\laboratorio_bigdata.pbix',
          r'C:\Users\USUARIO\.config\openchamber\chats\2026-11-22\session-ba044be6-619b-4787-9f47-a273222e81f4\entregable\laboratorio_bigdata.pbix.sin_visuales.bak']:
    print('====', p)
    z = zipfile.ZipFile(p)
    for name in z.namelist():
        if name.endswith('.json') and ('definition' in name or name == 'Settings'):
            print('---', name)
            s = z.read(name).decode('utf-8', 'replace')
            print(s[:3000])

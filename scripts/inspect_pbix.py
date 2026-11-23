import zipfile
p = r'C:\Users\USUARIO\Documents\laboratorio_bigdata.pbix'
z = zipfile.ZipFile(p)
for i in z.infolist():
    print(i.filename, i.file_size)

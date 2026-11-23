from docx import Document
p = r'C:\Users\USUARIO\Downloads\proyecto final.docx'
d = Document(p)
print('PARRAFOS:', len(d.paragraphs), 'TABLAS:', len(d.tables), 'IMAGENES:', len(d.inline_shapes))
for i, par in enumerate(d.paragraphs[:120]):
    t = par.text.strip()
    if t:
        print(i, repr(t[:180]), '| style:', par.style.name)
PY = None

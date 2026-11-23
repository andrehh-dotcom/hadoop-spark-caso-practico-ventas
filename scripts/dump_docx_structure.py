"""Vuelca párrafos e imágenes del DOCX de referencia en orden."""
from docx import Document
from docx.oxml.ns import qn

p = r'C:\Users\USUARIO\Downloads\proyecto final.docx'
d = Document(p)

para_idx = {}
for i, par in enumerate(d.paragraphs):
    para_idx[id(par._p)] = i

print('TOTAL PARRAFOS', len(d.paragraphs), 'IMAGENES', len(d.inline_shapes))
print('=' * 80)

for i, par in enumerate(d.paragraphs):
    # Buscar dibujos dentro de este párrafo
    drawings = par._p.findall('.//' + qn('w:drawing'))
    txt = par.text.strip()
    style = par.style.name if par.style else ''
    if drawings:
        for dr in drawings:
            blip = dr.find('.//' + qn('a:blip'))
            rid = blip.get(qn('r:embed')) if blip is not None else None
            print(f'[{i}] IMAGEN rid={rid}')
    if txt:
        align = str(par.alignment) if par.alignment is not None else '-'
        print(f'[{i}] TEXTO({style}, align={align}): {txt[:300]!r}')

print('=' * 80)
print('SECCIONES:', len(d.sections))
for s in d.sections:
    print('pagina:', s.page_width, s.page_height, 'margenes:',
          s.left_margin, s.right_margin, s.top_margin, s.bottom_margin)

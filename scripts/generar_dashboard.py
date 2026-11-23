# Genera un dashboard HTML autonomo con los resultados que exporta Spark.
# Uso: python scripts\generar_dashboard.py
import csv
import os
import html

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pbi = os.path.join(base, "powerbi")
salida = os.path.join(pbi, "dashboard.html")


def leer(nombre):
    ruta = os.path.join(pbi, nombre)
    if not os.path.exists(ruta):
        return []
    with open(ruta, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


productos = leer("ventas_por_producto.csv")
clientes = leer("ventas_por_cliente.csv")
meses = leer("ventas_por_mes.csv")
resumen = leer("resumen_general.csv")
mr = leer("ventas_por_producto_mr.csv")

if not resumen:
    raise SystemExit("Faltan los CSV en powerbi/. Ejecuta primero los jobs de Spark.")

r = resumen[0]
total = float(r["TotalVendido"])
nventas = int(r["NumVentas"])
ticket = float(r["TicketPromedio"])
pct = float(r["PctVentasAltas"])


def barras(filas, etiqueta, valor, titulo, color):
    if not filas:
        return ""
    maximo = max(float(f[valor]) for f in filas) or 1
    out = ['<section class="card"><h2>%s</h2><div class="bars">' % html.escape(titulo)]
    for f in sorted(filas, key=lambda x: float(x[valor]), reverse=True):
        v = float(f[valor])
        ancho = max(2, round(100 * v / maximo, 1))
        out.append(
            '<div class="bar-row"><span class="lbl">%s</span>'
            '<span class="track"><span class="fill" style="width:%s%%;background:%s"></span></span>'
            '<span class="val">$%s</span></div>'
            % (html.escape(f[etiqueta]), ancho, color, "{:,.2f}".format(v))
        )
    out.append("</div></section>")
    return "".join(out)


def linea(filas):
    if not filas:
        return ""
    vals = [float(f["TotalVendido"]) for f in filas]
    maximo = max(vals) or 1
    ancho, alto = 640, 180
    puntos = []
    for i, v in enumerate(vals):
        x = 20 + i * (ancho - 40) / max(1, len(vals) - 1)
        y = alto - 20 - (v / maximo) * (alto - 40)
        puntos.append("%.1f,%.1f" % (x, y))
    polilinea = " ".join(puntos)
    etiquetas = "".join(
        '<text x="%.1f" y="%d" font-size="11" text-anchor="middle" fill="#6b7280">%s</text>'
        % (20 + i * (ancho - 40) / max(1, len(vals) - 1), alto - 2, html.escape(f["Mes"]))
        for i, f in enumerate(filas)
    )
    circulos = "".join(
        '<circle cx="%s" cy="%s" r="4" fill="#0b6b3a"/>' % (p.split(",")[0], p.split(",")[1])
        for p in puntos
    )
    return (
        '<section class="card"><h2>Ventas por mes</h2>'
        '<svg viewBox="0 0 %d %d" width="100%%" height="200" role="img">'
        '<polyline fill="none" stroke="#0b6b3a" stroke-width="2.5" points="%s"/>%s%s</svg></section>'
        % (ancho, alto, polilinea, circulos, etiquetas)
    )


def tabla_mapreduce(filas):
    if not filas:
        return ""
    filas = sorted(filas, key=lambda f: float(f.get("Total", 0)), reverse=True)
    cuerpo = "".join(
        "<tr><td>%s</td><td class='num'>$%s</td><td class='num'>%s</td></tr>"
        % (
            html.escape(f.get("Producto", "")),
            "{:,.2f}".format(float(f.get("Total", 0))),
            html.escape(f.get("Ventas", "")),
        )
        for f in filas
    )
    return (
        '<section class="card"><h2>MapReduce: total por producto</h2>'
        "<table><thead><tr><th>Producto</th><th class='num'>Total</th><th class='num'>Ventas</th></tr></thead>"
        "<tbody>%s</tbody></table></section>" % cuerpo
    )


htmldoc = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard de Ventas - Hadoop 3 + Spark + Power BI</title>
<style>
  :root { --bg:#f6f7f9; --card:#ffffff; --ink:#111827; --muted:#6b7280; --line:#e5e7eb; --accent:#0b6b3a; }
  * { box-sizing:border-box; }
  body { margin:0; font-family:'Segoe UI',system-ui,sans-serif; background:var(--bg); color:var(--ink); }
  header { padding:24px 32px 8px; }
  header h1 { margin:0 0 4px; font-size:22px; }
  header p { margin:0; color:var(--muted); font-size:13px; }
  main { padding:16px 32px 40px; display:grid; gap:16px; grid-template-columns:repeat(2,minmax(0,1fr)); }
  .kpis { grid-column:1/-1; display:grid; gap:16px; grid-template-columns:repeat(4,minmax(0,1fr)); }
  .kpi, .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:16px 18px; }
  .kpi span { display:block; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
  .kpi strong { display:block; margin-top:6px; font-size:24px; }
  .card h2 { margin:0 0 14px; font-size:14px; font-weight:600; }
  .bars { display:grid; gap:10px; }
  .bar-row { display:grid; grid-template-columns:96px 1fr 92px; align-items:center; gap:10px; font-size:12px; }
  .lbl { color:#374151; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .track { height:10px; background:#eef0f3; border-radius:6px; overflow:hidden; }
  .fill { display:block; height:100%; border-radius:6px; }
  .val { text-align:right; font-variant-numeric:tabular-nums; }
  table { width:100%; border-collapse:collapse; font-size:12.5px; }
  th, td { padding:7px 6px; border-bottom:1px solid var(--line); text-align:left; }
  th { color:var(--muted); font-weight:600; }
  .num { text-align:right; font-variant-numeric:tabular-nums; }
  footer { grid-column:1/-1; color:var(--muted); font-size:12px; }
  @media (max-width:820px) { main { grid-template-columns:1fr; padding:12px; } .kpis { grid-template-columns:repeat(2,1fr); } }
</style>
</head>
<body>
<header>
  <h1>Dashboard de Ventas</h1>
  <p>Ingesta CSV -> HDFS (Hadoop 3.2.1) -> Spark 3.0 / MapReduce -> Power BI</p>
</header>
<main>
  <div class="kpis">
    <div class="kpi"><span>Ventas totales</span><strong>$__TOTAL__</strong></div>
    <div class="kpi"><span>Transacciones</span><strong>__NVENTAS__</strong></div>
    <div class="kpi"><span>Ticket promedio</span><strong>$__TICKET__</strong></div>
    <div class="kpi"><span>Ventas &gt; $100</span><strong>__PCT__%</strong></div>
  </div>
  __PRODUCTOS__
  __CLIENTES__
  __MESES__
  __MAPREDUCE__
  <footer>Generado desde HDFS: /data/analitica y /data/ventas_por_producto_mr. Fuente: data/ventas.csv (__FILAS__ filas).</footer>
</main>
</body>
</html>
"""

htmldoc = (
    htmldoc.replace("__TOTAL__", "{:,.2f}".format(total))
    .replace("__NVENTAS__", "{:,}".format(nventas))
    .replace("__TICKET__", "{:,.2f}".format(ticket))
    .replace("__PCT__", "{:.1f}".format(pct))
    .replace("__FILAS__", "{:,}".format(nventas))
    .replace("__PRODUCTOS__", barras(productos, "Producto", "TotalVendido", "Ventas por producto (Spark)", "#0b6b3a"))
    .replace("__CLIENTES__", barras(clientes, "Cliente", "TotalVendido", "Ventas por cliente (Spark)", "#1d4ed8"))
    .replace("__MESES__", linea(meses))
    .replace("__MAPREDUCE__", tabla_mapreduce(mr))
)

with open(salida, "w", encoding="utf-8") as f:
    f.write(htmldoc)
print("Dashboard generado:", salida)

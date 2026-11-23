import csv, random, datetime, os

random.seed(2026)
out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
carpeta = os.path.join(out, "data")
os.makedirs(carpeta, exist_ok=True)

clientes = ["Carlos", "Ana", "Beatriz", "David", "Elena"]
productos = [
    ("Laptop", 1200.00),
    ("Monitor", 300.00),
    ("Teclado", 50.00),
    ("Mouse", 25.00),
    ("Impresora", 150.00),
    ("Tablet", 220.00),
    ("Audifonos", 80.00),
]
ciudades = ["Lima", "Arequipa", "Trujillo", "Cusco"]

filas = []
# Filas base del caso del documento (el ejemplo exacto del PDF)
filas += [
    ("Carlos", "Laptop", 1, 1200.00, 2026, 1, "Lima"),
    ("Ana", "Monitor", 1, 300.00, 2026, 1, "Arequipa"),
    ("Beatriz", "Teclado", 1, 50.00, 2026, 1, "Lima"),
    ("David", "Mouse", 1, 25.00, 2026, 1, "Trujillo"),
    ("Elena", "Impresora", 1, 150.00, 2026, 1, "Cusco"),
]

for i in range(240):
    cliente = random.choice(clientes)
    producto, precio = random.choice(productos)
    cantidad = random.choice([1, 1, 1, 2, 2, 3])
    if producto in ("Laptop", "Monitor", "Impresora") and cantidad > 2:
        cantidad = 2
    mes = random.randint(1, 10)
    ciudad = random.choice(ciudades)
    filas.append((cliente, producto, cantidad, precio, 2026, mes, ciudad))

filas.sort(key=lambda f: (f[4], f[5]))

with open(os.path.join(carpeta, "ventas.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Cliente", "Producto", "Cantidad", "PrecioUnitario", "Anio", "Mes", "Ciudad", "Monto"])
    for cliente, producto, cantidad, precio, anio, mes, ciudad in filas:
        w.writerow([cliente, producto, cantidad, f"{precio:.2f}", anio, mes, ciudad, f"{cantidad * precio:.2f}"])

# Dato no estructurado: comentarios de clientes (para ELT con Spark)
comentarios = [
    "Carlos: la laptop llego rapido y funciona perfecto, excelente compra",
    "Ana: el monitor tiene muy buena resolucion, pero el envio demoro tres dias",
    "Beatriz: el teclado es comodo y barato, buena relacion calidad precio",
    "David: el mouse es basico, cumple para trabajar desde casa",
    "Elena: la impresora imprime bien aunque el toner es caro",
    "Carlos: atencion al cliente excelente, resolvieron mi garantia",
    "Ana: volvere a comprar, el monitor es ideal para disenar",
    "Beatriz: el teclado fallo a la semana, el soporte respondio rapido",
    "David: el mouse no es ergonomico, esperaba mas por el precio",
    "Elena: la impresora es lenta pero confiable para la oficina",
    "Carlos: la tablet tiene buena bateria y pantalla nitida",
    "Ana: los audifonos suenan muy bien y aislan el ruido",
]
with open(os.path.join(carpeta, "comentarios.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(comentarios * 8) + "\n")

print("ventas.csv:", len(filas), "filas")
print("comentarios.txt:", len(comentarios) * 8, "lineas")

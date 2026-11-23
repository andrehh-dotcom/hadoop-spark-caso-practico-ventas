#!/usr/bin/env python3
# Mapper de Hadoop Streaming: emite (Producto, Monto)
import sys

for linea in sys.stdin:
    linea = linea.strip()
    if not linea or linea.startswith("Cliente"):
        continue
    campos = linea.split(",")
    if len(campos) < 8:
        continue
    producto = campos[1]
    monto = campos[7]
    print("%s\t%s" % (producto, monto))

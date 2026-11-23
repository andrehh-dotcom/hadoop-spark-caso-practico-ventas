#!/usr/bin/env python3
# Reducer de Hadoop Streaming: suma el monto por producto
import sys

producto_actual = None
total = 0.0
ventas = 0

for linea in sys.stdin:
    linea = linea.strip()
    if not linea:
        continue
    producto, monto = linea.split("\t")
    monto = float(monto)
    if producto == producto_actual:
        total += monto
        ventas += 1
    else:
        if producto_actual is not None:
            print("%s\t%.2f\t%d" % (producto_actual, total, ventas))
        producto_actual = producto
        total = monto
        ventas = 1

if producto_actual is not None:
    print("%s\t%.2f\t%d" % (producto_actual, total, ventas))

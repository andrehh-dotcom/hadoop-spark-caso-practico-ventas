# Power BI: dashboard con los resultados de Hadoop + Spark

Los CSV de esta carpeta los genera el pipeline desde HDFS:

| Archivo | Origen HDFS | Uso en el dashboard |
|---|---|---|
| `ventas_altas.csv` | `/data/ventas_altas` | Detalle de compras > $100 (tabla) |
| `ventas_por_producto.csv` | `/data/analitica/ventas_por_producto` | Barras: total por producto |
| `ventas_por_cliente.csv` | `/data/analitica/ventas_por_cliente` | Barras: total por cliente |
| `ventas_por_mes.csv` | `/data/analitica/ventas_por_mes` | Linea: evolucion mensual |
| `resumen_general.csv` | `/data/analitica/resumen_general` | Tarjetas KPI |
| `ventas_por_producto_mr.csv` | `/data/ventas_por_producto_mr` | Validacion MapReduce |

## Pasos en Power BI Desktop

1. **Obtener datos -> Texto/CSV** y cargar los 5 CSV (uno por uno o **Carpeta** para cargar todos).
2. En **Transformar datos** verifica tipos: `TotalVendido`, `TicketPromedio`, `Monto` = Numero decimal; `Mes`, `NumVentas` = Numero entero.
3. Crea el modelo: `resumen_general` queda como tabla de medidas; no hace falta relacionar porque los agregados ya vienen calculados.
4. Medidas DAX sugeridas (tabla `resumen_general`):
   ```dax
   Total Ventas = SUM(resumen_general[TotalVendido])
   Transacciones = SUM(resumen_general[NumVentas])
   Ticket Promedio = AVERAGE(resumen_general[TicketPromedio])
   % Ventas Altas = AVERAGE(resumen_general[PctVentasAltas])
   ```
5. Visuales:
   - 4 **Tarjetas**: Total Ventas, Transacciones, Ticket Promedio, % Ventas Altas.
   - **Grafico de barras**: eje `Producto`, valor `TotalVendido`.
   - **Grafico de barras**: eje `Cliente`, valor `TotalVendido`.
   - **Grafico de lineas**: eje `Mes`, valor `TotalVendido`.
   - **Tabla**: `ventas_altas` con Cliente, Producto, Monto (filtro Monto > 100).
6. Guarda como `powerbi\Dashboard_Ventas.pbix`.

> Los datos ya estan limpios y agregados por Spark; Power BI solo consume.

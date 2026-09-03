def calcular_importe(cantidad, precio_unitario):
    return cantidad * precio_unitario

importe = calcular_importe(3, 1200)
assert importe == 3600, "El importe calculado no es el esperado"

importe2 = calcular_importe(5, 200)
assert importe2 == 1000, "El importe calculado no es el esperado"

importe3 = calcular_importe(2, 100)
assert importe3 == 500, "El importe calculado no es el esperado"


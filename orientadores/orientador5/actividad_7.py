def calcular_importe(cantidad, precio):
    if cantidad <= 0 or precio <= 0:
        raise ValueError("La cantidad y el precio deben ser mayores que cero")
    return cantidad * precio
try:
    cantidad = float(input("Ingrese la cantidad: "))
    precio = float(input("Ingrese el precio: "))
    importe = calcular_importe(cantidad, precio)
    print(f"El importe a pagar es: {importe}")
except ValueError as error:
    print(f"Error: {error}")
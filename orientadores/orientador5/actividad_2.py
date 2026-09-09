cantidad = 0
suma = 0

while True:
    numero = int(input("Ingrese un número entero (-1 para finalizar): "))
    
    if numero == -1:
        break
    
    cantidad += 1
    suma += numero

if cantidad == 0:
    print("No existen datos para calcular el promedio.")
else:
    promedio = suma / cantidad
    print(f"Cantidad de números ingresados: {cantidad}")
    print(f"Suma: {suma}")
    print(f"Promedio: {promedio}")
    
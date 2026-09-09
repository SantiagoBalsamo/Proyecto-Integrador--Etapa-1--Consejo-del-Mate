cantidad = 0
suma = 0

while True:
    try:
        numero = int(input("Ingrese un número entero (-1 para finalizar): "))
    except ValueError:
        print("Error: debe ingresar un número entero. Intente nuevamente.")
        continue
    
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
    
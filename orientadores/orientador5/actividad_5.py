numeros = [10, 20, 30, 40]

try:
    posicion = int(input("Posición: "))
    
    if posicion < 0:
        raise ValueError("La posición no puede ser negativa.")
    
    print(numeros[posicion])

except ValueError:
    print("Error: debe ingresar un número entero válido y no negativo.")
except IndexError:
    print("Error: la posición ingresada está fuera del rango de la lista.")
    
try:
    numero = int(input("Ingrese un número: "))
    
    if numero == 0:
        print("No se puede dividir por cero.")
    else:
        resultado = 100 / numero
        print(resultado)

except ValueError:
    print("Error: debe ingresar un número entero válido.")
    
    
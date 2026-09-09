def programa_division():
    try:
       
        num1 = float(input("Ingrese el dividendo (primer número): "))
        num2 = float(input("Ingrese el divisor (segundo número): "))
        resultado = num1 / num2

    except ValueError:
        
        print("Error: Debe ingresar valores numéricos válidos.")

    except ZeroDivisionError:
        
        print("Error: No es posible dividir por cero.")

    else:
        
        print(f"Resultado de la división: {resultado:.2f}")

    finally:
      
        print("Finalizando la ejecución del intento de división.\n")


if __name__ == "__main__":
    programa_division()

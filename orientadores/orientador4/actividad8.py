codigos = ("P101", "P205", "P330")

ventas_semanales = [
    [12, 15, 10, 18],
    [8, 11, 9, 14],
    [20, 17, 22, 19]
]

def total_por_producto(codigos, ventas):
    totales = []
    for i in range(len(codigos)):
        totales.append(sum(ventas[i]))
    return totales

def mostrar_total_por_producto(codigos, ventas):
    totales = total_por_producto(codigos, ventas)
    print("\n--- Total vendido por producto ---")
    for i in range(len(codigos)):
        print(f"{codigos[i]}: {totales[i]} unidades")

def total_semana(ventas, semana):
    indice = semana - 1
    total = 0
    for fila in ventas:
        total += fila[indice]
    return total

def mostrar_total_semana(ventas, semana):
    if validar_semana(ventas, semana):
        total = total_semana(ventas, semana)
        print(f"\nTotal vendido en la semana {semana}: {total} unidades")
    else:
        cantidad_semanas = len(ventas[0])
        print(f"\nError: la semana {semana} no existe. Debe estar entre 1 y {cantidad_semanas}.")

def producto_mayor_venta(codigos, ventas):
    totales = total_por_producto(codigos, ventas)
    indice_max = 0
    for i in range(len(totales)):
        if totales[i] > totales[indice_max]:
            indice_max = i
    return codigos[indice_max], totales[indice_max]

def mostrar_producto_mayor_venta(codigos, ventas):
    codigo, total = producto_mayor_venta(codigos, ventas)
    print(f"\nProducto con mayor venta acumulada: {codigo} ({total} unidades)")

def validar_semana(ventas, semana):
    cantidad_semanas = len(ventas[0])
    es_valida = False                              
    if semana >= 1 and semana <= cantidad_semanas:  
        es_valida = True                            
    return es_valida                                

def pedir_semana_validada(ventas):
    cantidad_semanas = len(ventas[0])
    semana_valida = False
    semana = 0
    while not semana_valida:
        entrada = input("Ingrese el número de semana a consultar: ")
        if entrada.isdigit():
            semana = int(entrada)
            if validar_semana(ventas, semana):
                semana_valida = True
            else:
                print(f"Entrada inválida: la semana debe estar entre 1 y {cantidad_semanas}.")
        else:
            print(f"Entrada inválida: '{entrada}' no es un número entero.")
    return semana

if __name__ == "__main__":
    mostrar_total_por_producto(codigos, ventas_semanales)
    mostrar_producto_mayor_venta(codigos, ventas_semanales)

    #Ejemplo semana válida
    mostrar_total_semana(ventas_semanales, 2)

    #Ejemplo semana fuera de rango
    mostrar_total_semana(ventas_semanales, 7)
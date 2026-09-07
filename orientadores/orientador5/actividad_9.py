def calcular_importe(cantidad, precio):
    importe = cantidad * precio
    assert importe > 0, "Error interno: el importe calculado no es positivo"
    return importe
 
def cargar_productos():
    productos = []
    while True:
        codigo = input("Ingrese código del producto (FIN para terminar): ").strip()
        if codigo == "FIN":
            break
        descripcion = input("Ingrese descripción: ").strip()
        try:
            cantidad = int(input("Ingrese cantidad: "))
            precio = float(input("Ingrese precio: "))
            if cantidad <= 0 or precio <= 0:
                raise ValueError("la cantidad y el precio deben ser mayores que cero")
        except ValueError as error:
            print(f"Datos inválidos ({error}). El producto no fue incorporado.\n")
            continue
 
        importe = calcular_importe(cantidad, precio)
        productos.append([codigo, descripcion, cantidad, precio, importe])
        print(f"Producto '{codigo}' agregado correctamente.\n")
    return productos
 
def informar_resultados(productos):
    cantidad_productos = len(productos)
    if cantidad_productos == 0:
        print("No se cargaron productos.")
        return
    importe_total = sum(producto[4] for producto in productos)
    precio_promedio = importe_total / cantidad_productos
 
    print("----- INFORME FINAL -----")
    print(f"Cantidad de productos cargados: {cantidad_productos}")
    print(f"Importe total: ${importe_total:.2f}")
    print(f"Precio promedio: ${precio_promedio:.2f}")
 
def main():
    productos = cargar_productos()
    informar_resultados(productos)

if __name__ == "__main__":
    main()
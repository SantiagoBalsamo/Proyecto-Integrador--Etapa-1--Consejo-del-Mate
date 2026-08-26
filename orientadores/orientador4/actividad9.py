def contiene_digito(texto):
    encontrado = False
    for caracter in texto:
        if caracter.isdigit():
            encontrado = True
    return encontrado


def es_precio_valido(texto):
    valido = True
    cantidad_puntos = 0
    if len(texto) == 0:
        valido = False
    else:
        for caracter in texto:
            if caracter == ".":
                cantidad_puntos += 1
            else:
                if caracter.isdigit() == False:
                    valido = False
        if cantidad_puntos > 1:
            valido = False
    return valido


def buscar_producto(productos, codigo):
    resultado = None
    for producto in productos:
        if producto[0] == codigo:
            resultado = producto
    return resultado


def descripcion_repetida(productos, descripcion):
    repetida = False
    for producto in productos:
        if producto[1].lower() == descripcion.lower():
            repetida = True
    return repetida


def solicitar_descripcion_valida(productos):
    descripcion_valida = ""
    continuar = True
    while continuar:
        descripcion = input("Descripcion: ")
        if contiene_digito(descripcion) == True:
            print("La descripcion no puede contener numeros")
        else:
            if descripcion_repetida(productos, descripcion) == True:
                print("Ya existe un producto con esa descripcion")
            else:
                descripcion_valida = descripcion
                continuar = False
    return descripcion_valida


def solicitar_precio_valido():
    precio = 0
    continuar = True
    while continuar:
        precio_texto = input("Precio: ")
        if es_precio_valido(precio_texto) == True:
            precio_convertido = float(precio_texto)
            if precio_convertido > 0:
                precio = precio_convertido
                continuar = False
            else:
                print("El precio debe ser mayor a cero")
        else:
            print("Ingrese un precio valido, solo numeros")
    return precio


def cargar_productos():
    productos = []
    continuar = True
    while continuar:
        codigo = input("Codigo del producto (FIN para terminar): ")
        if codigo == "FIN":
            continuar = False
        else:
            if buscar_producto(productos, codigo) == None:
                descripcion = solicitar_descripcion_valida(productos)
                precio = solicitar_precio_valido()
                producto = (codigo, descripcion, precio)
                productos.append(producto)
            else:
                print("Ese codigo ya existe, ingrese uno diferente")
    return productos


def mostrar_productos(productos):
    if len(productos) == 0:
        print("No hay productos cargados")
    else:
        print("Catalogo de productos:")
        for producto in productos:
            codigo, descripcion, precio = producto
            print(f"Codigo: {codigo} | Descripcion: {descripcion} | Precio: ${precio:.2f}")


def producto_mayor_precio(productos):
    mayor = None
    for producto in productos:
        if mayor == None:
            mayor = producto
        else:
            if producto[2] > mayor[2]:
                mayor = producto
    return mayor


def precio_promedio(productos):
    if len(productos) == 0:
        return None
    else:
        suma = 0
        for producto in productos:
            suma += producto[2]
        return suma / len(productos)


def actualizar_precio(productos, codigo, nuevo_precio):
    indice = 0
    actualizado = False
    while indice < len(productos):
        if productos[indice][0] == codigo:
            codigo_actual, descripcion, precio_actual = productos[indice]
            productos[indice] = (codigo_actual, descripcion, nuevo_precio)
            actualizado = True
        indice += 1
    return actualizado


def main():
    productos = cargar_productos()
    mostrar_productos(productos)

    codigo_buscado = input("Codigo a buscar: ")
    producto_encontrado = buscar_producto(productos, codigo_buscado)
    if producto_encontrado == None:
        print("Producto no encontrado")
    else:
        print(f"Producto encontrado: {producto_encontrado}")

    mayor = producto_mayor_precio(productos)
    if mayor == None:
        print("No hay productos para determinar el de mayor precio")
    else:
        print(f"Producto de mayor precio: {mayor[1]} (${mayor[2]:.2f})")

    promedio = precio_promedio(productos)
    if promedio == None:
        print("No hay productos para calcular el promedio")
    else:
        print(f"Precio promedio: ${promedio:.2f}")


if __name__ == "__main__":
    main()
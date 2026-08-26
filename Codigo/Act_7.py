producto = input("Producto: ")
precio = float(input("Precio unitario: "))
cantidad = int(input("Cantidad: "))
total = precio * cantidad

print(f"El importe total de {cantidad} unidades de {producto} es: ${total:.2f}")

print("El importe total de " + str(cantidad) + " unidades de " + producto + " es: $" + str(total))
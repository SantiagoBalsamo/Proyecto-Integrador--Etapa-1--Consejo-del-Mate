def contiene_digitos(texto):
    val = False
    for caracter in texto:
        if caracter.isdigit():
            val = True
    return val


def generar_sigla(texto):
    palabras = texto.split()
    sigla = ""
    for palabra in palabras:
        sigla += palabra[0].upper()
    return sigla


def normalizar_nombre(nombre):
    return nombre.title()


def solicitar_cantidad_integrantes():
    while True:
        entrada = input("Cantidad de integrantes: ")
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        else:
            print("Ingrese un numero entero mayor a cero")


def solicitar_integrantes(cantidad):
    integrantes = []
    contador = 1
    while contador <= cantidad:
        nombre = input(f"Nombre del integrante {contador}: ")
        rol = input(f"Rol inicial de {nombre}: ")
        integrante = {"nombre": normalizar_nombre(nombre), "rol": normalizar_nombre(rol)}
        integrantes.append(integrante)
        contador += 1
    return integrantes


def main():
    nombre_equipo = input("Nombre del equipo: ")
    comision = input("Comision: ")
    cantidad_integrantes = solicitar_cantidad_integrantes()
    integrantes = solicitar_integrantes(cantidad_integrantes)

    nombre_equipo_mayus = nombre_equipo.upper()
    cantidad_caracteres = len(nombre_equipo)
    sigla = generar_sigla(nombre_equipo)
    tiene_digitos = contiene_digitos(nombre_equipo)

    print(f"Equipo: {nombre_equipo_mayus}")
    print(f"Comision: {comision}")
    print(f"Cantidad de caracteres del nombre del equipo: {cantidad_caracteres}")
    print(f"Sigla del equipo: {sigla}")
    if tiene_digitos:
        print("El nombre del equipo contiene al menos un digito")
    else:
        print("El nombre del equipo no contiene digitos")

    print("Integrantes del equipo:")
    for integrante in integrantes:
        print(f"- {integrante['nombre']} | Rol: {integrante['rol']}")


if __name__ == "__main__":
    main()

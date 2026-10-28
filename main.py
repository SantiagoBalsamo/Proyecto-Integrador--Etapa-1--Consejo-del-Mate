"""
Sistema de gestión de un torneo de eSports (FIFA) - Etapa 2.
Punto de entrada: login y menú interactivo por consola.

Inicio del programa (en este orden):
1. Lee configuracion.json y valida la puntuación.
2. Lee usuarios.json a un diccionario {usuario: contraseña}.
3. Pide usuario y contraseña, con hasta 3 intentos: primero controla el
   formato con expresiones regulares y después compara con el diccionario.
4. Lee equipos.txt y valida los nombres, que no haya repetidos, que haya
   al menos 4 y que la cantidad sea par.
5. Genera el fixture y crea las tres matrices según la cantidad de equipos.
6. Muestra el menú.

Errores críticos (pasos 1 a 4): un archivo obligatorio que falta o es
inválido, o agotar los intentos de login, impiden iniciar: el programa
informa el motivo y termina sin mostrar el menú.
Errores no críticos (dentro del menú): un dato mal ingresado o un error
al exportar el fixture se informan y el programa sigue.

No hay variables globales: los datos se crean dentro de las funciones y
viajan por parámetro. No hay break, continue ni return en el medio de
una función: cada función tiene una sola entrada y una sola salida.
"""

import datos
import operaciones as ops
import validaciones
import archivos


# ---------- Utilidades de entrada/salida ----------

def pedir_entero(mensaje, minimo, maximo):
    """Pide un entero por consola hasta que el usuario ingrese uno válido.
    validar_entero lanza ValueError si el dato no sirve; acá se captura,
    se muestra el mensaje y se vuelve a pedir (error no crítico)."""
    valor_valido = False
    resultado_final = 0
    while not valor_valido:
        texto = input(mensaje)
        try:
            resultado_final = validaciones.validar_entero(texto, minimo, maximo)
            valor_valido = True
        except ValueError as error:
            print(f"  Error: {error}")
    return resultado_final


def unir_con_comas(lista):
    """Devuelve los elementos de la lista separados por coma, en un solo texto."""
    texto = ""
    for i in range(len(lista)):
        if i == 0:
            texto = lista[i]
        else:
            texto = texto + ", " + lista[i]
    return texto


# ---------- Login ----------

def iniciar_sesion(usuarios, intentos_maximos):
    """
    Pide usuario y contraseña hasta que sean correctos o se agoten los
    intentos. Devuelve el nombre del usuario que ingresó, o "" si no
    pudo ingresar. El while termina por su propia condición (sin break).
    """
    usuario_logueado = ""
    intentos = 0
    while usuario_logueado == "" and intentos < intentos_maximos:
        intentos = intentos + 1
        print(f"\nIngreso al sistema (intento {intentos} de {intentos_maximos})")
        usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ").strip()
        try:
            validaciones.validar_usuario(usuario)
            validaciones.validar_contrasena(contrasena)
        except ValueError as error:
            print(f"  Error: {error}")
        else:
            if validaciones.verificar_credenciales(usuarios, usuario, contrasena):
                usuario_logueado = usuario
                print(f"  Bienvenido/a, {usuario}.")
            else:
                print("  Error: usuario o contraseña incorrectos.")
    return usuario_logueado


# ---------- Opciones del menú ----------

def mostrar_menu():
    print("\n=== TORNEO DE ESPORTS (FIFA) - MENÚ PRINCIPAL ===")
    print("1) Información general del torneo")
    print("2) Cargar resultado de un partido")
    print("3) Ver tabla de posiciones")
    print("4) Ver resultados de una fecha")
    print("5) Buscar equipo")
    print("6) Ver indicadores (promedios, diferencia de gol, efectividad)")
    print("7) Detectar condiciones destacables (invictos / estado crítico)")
    print("8) Resumen general del torneo")
    print("9) Exportar el fixture a fixture.txt")
    print("0) Salir")


def mostrar_informacion_general(equipos, puntuacion, cantidad_equipos, cantidad_fechas, limite_estado_critico):
    print("\n--- Información general del torneo ---")
    print("  Formato: todos contra todos, a una rueda")
    print(f"  Cantidad de equipos: {cantidad_equipos}")
    print(f"  Cantidad de fechas: {cantidad_fechas}")
    print("  Puntos por resultado (configuracion.json):")
    for resultado, puntos in puntuacion.items():
        print(f"    {resultado}: {puntos}")
    print("  Criterio de desempate: puntos, diferencia de gol y goles a favor")
    print(f"  Estado crítico: 0 puntos con {limite_estado_critico} o más partidos jugados")
    print("\nEquipos participantes:")
    numero = 1
    for equipo in equipos:
        print(f"  {numero}. {equipo}")
        numero = numero + 1


def mostrar_fechas_disponibles(cantidad_fechas):
    print("\nFechas del torneo:")
    for i in range(cantidad_fechas):
        print(f"  Fecha {i + 1}")


def cargar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra, equipos, fixture,
                      cantidad_fechas, goles_maximos, sin_resultado, puntuacion):
    print("\n--- Cargar resultado de un partido ---")
    mostrar_fechas_disponibles(cantidad_fechas)
    fecha = pedir_entero("Elegí el número de fecha: ", 1, cantidad_fechas)
    fecha_idx = fecha - 1

    print(f"\nPartidos de la fecha {fecha}:")
    partidos_fecha = fixture[fecha_idx]
    numero = 1
    for local_idx, visitante_idx in partidos_fecha:
        estado = "cargado" if ops.partido_cargado(matriz_puntos, fecha_idx, local_idx, sin_resultado) else "pendiente"
        print(f"  {numero}. {equipos[local_idx]} vs {equipos[visitante_idx]} ({estado})")
        numero = numero + 1

    numero_partido = pedir_entero("Elegí el número de partido: ", 1, len(partidos_fecha))
    local_idx, visitante_idx = partidos_fecha[numero_partido - 1]

    if ops.partido_cargado(matriz_puntos, fecha_idx, local_idx, sin_resultado):
        print("  Error: ese partido ya tiene un resultado cargado (inconsistencia evitada).")
    else:
        goles_local = pedir_entero(f"Goles de {equipos[local_idx]}: ", 0, goles_maximos)
        goles_visitante = pedir_entero(f"Goles de {equipos[visitante_idx]}: ", 0, goles_maximos)

        ops.registrar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                                 fecha_idx, local_idx, visitante_idx, goles_local, goles_visitante,
                                 puntuacion)
        print("  Resultado cargado correctamente.")


def mostrar_tabla_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                              equipos, cantidad_equipos, sin_resultado):
    print("\n--- Tabla de posiciones ---")
    tabla = ops.tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                                     equipos, cantidad_equipos, sin_resultado)
    print("Pos - Equipo - Puntos - Diferencia de gol - Goles a favor")
    posicion = 1
    for equipo, pts, dif, gf in tabla:
        print(f"{posicion} - {equipo} - {pts} - {dif} - {gf}")
        posicion = posicion + 1


def mostrar_resultados_fecha(matriz_goles_favor, equipos, fixture, cantidad_fechas, sin_resultado):
    """Reporte filtrado: todos los partidos de una fecha, con el resultado
    si ya se jugó o "vs" si está pendiente."""
    mostrar_fechas_disponibles(cantidad_fechas)
    fecha = pedir_entero("¿De qué fecha querés ver los resultados?: ", 1, cantidad_fechas)
    print(f"\n--- Fecha {fecha} ---")
    for linea in ops.lineas_de_fecha(fecha - 1, fixture, equipos, matriz_goles_favor, sin_resultado):
        print(linea)


def buscar_equipo(equipos, matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                   cantidad_equipos, cantidad_fechas, sin_resultado):
    print("\n--- Buscar equipo ---")
    print("Equipos participantes:")
    numero = 1
    for equipo in equipos:
        print(f"  {numero}. {equipo}")
        numero = numero + 1

    nombre_buscado = input("\nEscribí el nombre del equipo: ")
    nombre_limpio = nombre_buscado.strip()

    if nombre_limpio == "":
        print("  Error: el nombre no puede estar vacío.")
    else:
        indice_equipo = ops.buscar_equipo_por_nombre(equipos, nombre_limpio, cantidad_equipos)
        if indice_equipo == -1:
            print("  Error: no existe ningún equipo con ese nombre.")
        else:
            informacion = ops.informacion_equipo(indice_equipo, matriz_puntos, matriz_goles_favor,
                                                  matriz_goles_contra, cantidad_equipos,
                                                  cantidad_fechas, sin_resultado)
            puntos_equipo, gf_equipo, gc_equipo, jugados_equipo, restantes_equipo = informacion
            print(f"\n--- {equipos[indice_equipo]} ---")
            print(f"  Puntos: {puntos_equipo}")
            print(f"  Goles a favor: {gf_equipo}")
            print(f"  Goles en contra: {gc_equipo}")
            print(f"  Partidos jugados: {jugados_equipo}")
            print(f"  Partidos restantes por jugar: {restantes_equipo}")


def mostrar_indicadores(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                         equipos, cantidad_equipos, sin_resultado, puntuacion):
    print("\n--- Indicadores ---")
    promedios = ops.promedio_goles_favor(matriz_goles_favor, matriz_puntos, cantidad_equipos, sin_resultado)
    diferencias = ops.diferencia_de_gol(matriz_goles_favor, matriz_goles_contra, cantidad_equipos, sin_resultado)
    porcentajes = ops.porcentaje_efectividad(matriz_puntos, cantidad_equipos, sin_resultado, puntuacion)
    print("Equipo - Promedio goles a favor - Diferencia de gol - Efectividad")
    for i in range(len(equipos)):
        print(f"{equipos[i]} - {promedios[i]:.2f} - {diferencias[i]} - {porcentajes[i]:.1f}%")


def mostrar_condiciones_destacables(matriz_puntos, equipos, cantidad_equipos, sin_resultado,
                                     puntuacion, limite_estado_critico):
    """Reporte de alertas: equipos en estado crítico (más los invictos)."""
    print("\n--- Condiciones destacables ---")
    invictos = ops.equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntuacion)
    criticos = ops.equipos_en_estado_critico(matriz_puntos, equipos, cantidad_equipos, sin_resultado,
                                              limite_estado_critico)
    print("  Equipos invictos:", unir_con_comas(invictos) if invictos else "ninguno por el momento")
    print(f"  Equipos en estado crítico (0 puntos con {limite_estado_critico} o más partidos jugados):",
          unir_con_comas(criticos) if criticos else "ninguno por el momento")


def mostrar_resumen_general(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                             equipos, cantidad_equipos, cantidad_fechas, sin_resultado, puntuacion):
    """Reporte general: totales e indicadores sobre todos los resultados."""
    print("\n=== RESUMEN GENERAL DEL TORNEO ===")
    total_partidos_posibles = cantidad_fechas * (cantidad_equipos // 2)
    partidos_jugados = ops.partidos_jugados_del_torneo(matriz_puntos, cantidad_equipos, sin_resultado)
    print(f"1) Partidos jugados: {partidos_jugados} de {total_partidos_posibles}")

    tabla = ops.tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                                     equipos, cantidad_equipos, sin_resultado)
    if partidos_jugados == 0:
        print("2) Líder del torneo: todavía no hay partidos cargados")
        print("3) Mejor ataque: todavía no hay partidos cargados")
    else:
        puntos_del_lider = tabla[0][1]
        lideres = []
        for equipo, pts, dif, gf in tabla:
            if pts == puntos_del_lider:
                lideres.append(equipo)
        print(f"2) Líder del torneo: {unir_con_comas(lideres)} ({puntos_del_lider} puntos)")
        equipo_ataque, goles_ataque = ops.equipo_con_mas_goles_favor(matriz_goles_favor, equipos,
                                                                      cantidad_equipos, sin_resultado)
        print(f"3) Mejor ataque: {equipo_ataque} ({goles_ataque} goles a favor)")

    invictos = ops.equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntuacion)
    print(f"4) Equipos invictos: {unir_con_comas(invictos) if invictos else 'ninguno'}")

    print("5) Top 3 del torneo:")
    # Slicing: las primeras 3 posiciones de la tabla ya ordenada.
    top_3 = tabla[:3]
    posicion = 1
    for equipo, pts, dif, gf in top_3:
        print(f"   {posicion}. {equipo} - {pts} pts (dif. {dif})")
        posicion = posicion + 1

    # Diccionario acumulador {numero_de_fecha: goles_totales}, recorrido con items().
    goles_fecha = ops.goles_por_fecha(matriz_goles_favor, cantidad_equipos, cantidad_fechas, sin_resultado)
    print("6) Goles por fecha:")
    for fecha, goles in goles_fecha.items():
        print(f"   Fecha {fecha}: {goles} goles")

    maximo, fechas_maximas = ops.fecha_con_mas_goles(goles_fecha)
    if maximo == 0:
        print("7) Fecha con más goles: todavía no hay goles cargados")
    else:
        nombres_fechas = []
        for fecha in fechas_maximas:
            nombres_fechas.append(f"Fecha {fecha}")
        print(f"7) Fecha con más goles: {unir_con_comas(nombres_fechas)} ({maximo} goles)")


def exportar_fixture(fixture, equipos, matriz_goles_favor, cantidad_equipos, cantidad_fechas, sin_resultado):
    """Archivo de texto generado: escribe el fixture completo en fixture.txt,
    con el resultado de los partidos ya jugados. Si no se puede escribir,
    es un error no crítico: se informa y se vuelve al menú."""
    lineas = ops.lineas_del_fixture(fixture, equipos, matriz_goles_favor, cantidad_equipos,
                                     cantidad_fechas, sin_resultado)
    try:
        archivos.escribir_lineas("fixture.txt", lineas)
    except OSError as error:
        print(f"  Error: {error}")
    else:
        print("\n  Fixture exportado en fixture.txt (los partidos jugados incluyen el resultado).")


# ---------- Menú principal ----------

def ejecutar_menu(equipos, puntuacion):
    """Arma las estructuras del torneo a partir de la lista de equipos ya
    validada y atiende el menú hasta que el usuario elige salir."""
    goles_maximos = datos.obtener_goles_maximos()
    limite_estado_critico = datos.obtener_limite_estado_critico()
    sin_resultado = datos.obtener_sin_resultado()
    cantidad_equipos = datos.obtener_cantidad_equipos(equipos)
    cantidad_fechas = datos.obtener_cantidad_fechas(equipos)
    fixture = datos.generar_fixture(equipos)
    matriz_puntos = datos.crear_matriz_puntos(cantidad_equipos, cantidad_fechas, sin_resultado)
    matriz_goles_favor = datos.crear_matriz_goles_favor(cantidad_equipos, cantidad_fechas, sin_resultado)
    matriz_goles_contra = datos.crear_matriz_goles_contra(cantidad_equipos, cantidad_fechas, sin_resultado)

    opcion = -1
    while opcion != 0:
        mostrar_menu()
        texto_opcion = input("Elegí una opción: ")
        try:
            opcion = validaciones.validar_entero(texto_opcion, 0, 9)
        except ValueError as error:
            print(f"  Error: {error}")
            opcion = -1

        if opcion == 1:
            mostrar_informacion_general(equipos, puntuacion, cantidad_equipos, cantidad_fechas,
                                        limite_estado_critico)
        elif opcion == 2:
            cargar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra, equipos, fixture,
                              cantidad_fechas, goles_maximos, sin_resultado, puntuacion)
        elif opcion == 3:
            mostrar_tabla_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                                      equipos, cantidad_equipos, sin_resultado)
        elif opcion == 4:
            mostrar_resultados_fecha(matriz_goles_favor, equipos, fixture, cantidad_fechas, sin_resultado)
        elif opcion == 5:
            buscar_equipo(equipos, matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                          cantidad_equipos, cantidad_fechas, sin_resultado)
        elif opcion == 6:
            mostrar_indicadores(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                                 equipos, cantidad_equipos, sin_resultado, puntuacion)
        elif opcion == 7:
            mostrar_condiciones_destacables(matriz_puntos, equipos, cantidad_equipos, sin_resultado,
                                             puntuacion, limite_estado_critico)
        elif opcion == 8:
            mostrar_resumen_general(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                                     equipos, cantidad_equipos, cantidad_fechas, sin_resultado, puntuacion)
        elif opcion == 9:
            exportar_fixture(fixture, equipos, matriz_goles_favor, cantidad_equipos, cantidad_fechas,
                             sin_resultado)
        elif opcion == 0:
            print("\n¡Gracias por usar el sistema! Hasta la próxima.")


def main():
    print("=== TORNEO DE ESPORTS (FIFA) ===")
    puede_seguir = True
    puntuacion = {}
    usuarios = {}
    equipos = []

    # Paso 1: puntuación desde configuracion.json (archivo obligatorio:
    # si falta o es inválido, no se reemplaza por valores inventados).
    try:
        puntuacion = validaciones.validar_configuracion(archivos.leer_json("configuracion.json"))
    except (OSError, ValueError) as error:
        print(f"Error: {error}")
        puede_seguir = False

    # Paso 2: usuarios desde usuarios.json
    if puede_seguir:
        try:
            usuarios = validaciones.validar_usuarios(archivos.leer_json("usuarios.json"))
        except (OSError, ValueError) as error:
            print(f"Error: {error}")
            puede_seguir = False

    # Paso 3: login con hasta 3 intentos
    if puede_seguir:
        usuario = iniciar_sesion(usuarios, 3)
        if usuario == "":
            print("\nSe superó la cantidad máxima de intentos. El programa termina.")
            puede_seguir = False

    # Paso 4: equipos desde equipos.txt, validados
    if puede_seguir:
        try:
            equipos = archivos.leer_lineas("equipos.txt")
            validaciones.validar_equipos(equipos, datos.obtener_minimo_equipos())
        except (OSError, ValueError) as error:
            print(f"\nError: {error}")
            print("El programa no puede seguir sin una lista de equipos válida.")
            puede_seguir = False

    # Pasos 5 y 6: fixture, matrices y menú
    if puede_seguir:
        ejecutar_menu(equipos, puntuacion)


if __name__ == "__main__":
    main()

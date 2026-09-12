
import datos
import operaciones as ops


#Funciones del menu

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
    print("0) Salir")


def pedir_entero(mensaje, minimo, maximo): #pide numero entero hasata que sea valido
    valor_valido = False
    resultado_final = 0
    while not valor_valido:
        texto = input(mensaje)
        valido, resultado = ops.validar_entero(texto, minimo, maximo)
        if valido:
            valor_valido = True
            resultado_final = resultado
        else:
            print(f"  Error: {resultado}")
    return resultado_final


def unir_con_comas(lista):
    texto = ""
    for i in range(len(lista)):
        if i == 0:
            texto = lista[i]
        else:
            texto = texto + ", " + lista[i]
    return texto


def mostrar_informacion_general(equipos, reglas_torneo):
    print("\nInformación general del torneo")
    for regla in reglas_torneo:
        print(f"  - {regla}")
    print("\nEquipos participantes:")
    numero = 1
    for equipo in equipos:
        print(f"  {numero}. {equipo}")
        numero = numero + 1


def mostrar_fechas_disponibles(cantidad_fechas):
    print("\nFechas del torneo:")
    for i in range(cantidad_fechas):
        print(f"  Fecha {i + 1}")


def cargar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, fixture, cantidad_fechas, goles_maximos, sin_resultado,puntos_victoria, puntos_empate, puntos_derrota):
    print("\nCargar resultado de un partido")
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
                                 puntos_victoria, puntos_empate, puntos_derrota)
        print("  Resultado cargado correctamente.")


def buscar_equipo(equipos, matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                   cantidad_equipos, cantidad_fechas, sin_resultado):
    print("\n Buscar equipo ")
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
            informacion = ops.informacion_equipo(indice_equipo, matriz_puntos, matriz_goles_favor,matriz_goles_contra, cantidad_equipos,cantidad_fechas, sin_resultado)
            puntos_equipo, gf_equipo, gc_equipo, jugados_equipo, restantes_equipo = informacion
            print(f"\n--- {equipos[indice_equipo]} ---")
            print(f"  Puntos: {puntos_equipo}")
            print(f"  Goles a favor: {gf_equipo}")
            print(f"  Goles en contra: {gc_equipo}")
            print(f"  Partidos jugados: {jugados_equipo}")
            print(f"  Partidos restantes por jugar: {restantes_equipo}")


def mostrar_tabla_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado):
    print("\nTabla de posiciones ")
    tabla = ops.tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado)
    print("Pos - Equipo - Puntos - Diferencia de gol - Goles a favor")
    posicion = 1
    for equipo, pts, dif, gf in tabla:
        print(f"{posicion} - {equipo} - {pts} - {dif} - {gf}")
        posicion = posicion + 1


def mostrar_resultados_fecha(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, fixture, cantidad_fechas, sin_resultado):
    mostrar_fechas_disponibles(cantidad_fechas)
    fecha = pedir_entero("¿De qué fecha querés ver los resultados?: ", 1, cantidad_fechas)
    resultados = ops.resultados_de_fecha(fecha - 1, matriz_puntos, matriz_goles_favor,matriz_goles_contra, equipos, fixture, sin_resultado)
    print(f"\n Resultados de la fecha: {fecha}")
    if not resultados:
        print("  Todavía no hay resultados cargados para esta fecha.")
    else:
        for local, gf, gc, visitante in resultados:
            print(f"  {local} {gf} - {gc} {visitante}")


def mostrar_indicadores(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado, puntos_victoria):
    print("\n Indicadores ")
    promedios = ops.promedio_goles_favor(matriz_goles_favor, matriz_puntos, cantidad_equipos, sin_resultado)
    diferencias = ops.diferencia_de_gol(matriz_goles_favor, matriz_goles_contra, cantidad_equipos, sin_resultado)
    porcentajes = ops.porcentaje_efectividad(matriz_puntos, cantidad_equipos, sin_resultado, puntos_victoria)
    print("Equipo - Promedio goles a favor - Diferencia de gol - Efectividad")
    for i in range(len(equipos)):
        print(f"{equipos[i]} - {promedios[i]:.2f} - {diferencias[i]} - {porcentajes[i]:.1f}%")


def mostrar_condiciones_destacables(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntos_derrota):
    print("\nCondiciones destacables")
    invictos = ops.equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntos_derrota)
    criticos = ops.equipos_en_estado_critico(matriz_puntos, equipos, cantidad_equipos, sin_resultado, 3)
    print("  Equipos invictos:", unir_con_comas(invictos) if invictos else "ninguno por el momento")
    print("  Equipos en estado crítico (0 puntos con 3+ partidos jugados):",
          unir_con_comas(criticos) if criticos else "ninguno por el momento")


def mostrar_resumen_general(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, cantidad_fechas, sin_resultado, puntos_derrota):
    print("\n RESUMEN GENERAL DEL TORNEO ")
    total_partidos_posibles = cantidad_fechas * (len(equipos) // 2)

    celdas_jugadas = 0
    for i in range(len(equipos)):
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                celdas_jugadas = celdas_jugadas + 1
    partidos_jugados = celdas_jugadas // 2
    print(f"1) Partidos jugados: {partidos_jugados} de {total_partidos_posibles}")

    tabla = ops.tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado)
    puntos_del_lider = tabla[0][1]
    lideres = []
    for equipo, pts, dif, gf in tabla:
        if pts == puntos_del_lider:
            lideres.append(equipo)
    print(f"2) Líder del torneo: {unir_con_comas(lideres)} ({puntos_del_lider} puntos)")

    equipo_ataque, goles_ataque = ops.equipo_con_mas_goles_favor(matriz_goles_favor, equipos, cantidad_equipos, sin_resultado)
    print(f"3) Mejor ataque: {equipo_ataque} ({goles_ataque} goles a favor)")

    invictos = ops.equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntos_derrota)
    print(f"4) Equipos invictos: {unir_con_comas(invictos) if invictos else 'ninguno'}")

    print("5) Top 3 del torneo:")#slincing para tomar el top 3 
    top_3 = tabla[:3]
    posicion = 1
    for equipo, pts, dif, gf in top_3:
        print(f"   {posicion}. {equipo} - {pts} pts (dif. {dif})")
        posicion = posicion + 1


def main():
    equipos = datos.obtener_equipos()
    puntos_victoria = datos.obtener_puntos_victoria()
    puntos_empate = datos.obtener_puntos_empate()
    puntos_derrota = datos.obtener_puntos_derrota()
    goles_maximos = datos.obtener_goles_maximos()
    sin_resultado = datos.obtener_sin_resultado()
    cantidad_equipos = datos.obtener_cantidad_equipos(equipos)
    cantidad_fechas = datos.obtener_cantidad_fechas(equipos)
    reglas_torneo = datos.obtener_reglas_torneo(cantidad_equipos, cantidad_fechas,puntos_victoria, puntos_empate, puntos_derrota)
    fixture = datos.generar_fixture(equipos)
    matriz_puntos = datos.crear_matriz_puntos(cantidad_equipos, cantidad_fechas, sin_resultado)
    matriz_goles_favor = datos.crear_matriz_goles_favor(cantidad_equipos, cantidad_fechas, sin_resultado)
    matriz_goles_contra = datos.crear_matriz_goles_contra(cantidad_equipos, cantidad_fechas, sin_resultado)

    opcion = -1
    while opcion != 0:
        mostrar_menu()
        texto_opcion = input("Elegí una opción: ")
        valido, opcion = ops.validar_entero(texto_opcion, 0, 8)
        if not valido:
            print(f"  Error: {opcion}")
            opcion = -1
        elif opcion == 1:
            mostrar_informacion_general(equipos, reglas_torneo)
        elif opcion == 2:
            cargar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, fixture, cantidad_fechas, goles_maximos, sin_resultado,puntos_victoria, puntos_empate, puntos_derrota)
        elif opcion == 3:
            mostrar_tabla_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado)
        elif opcion == 4:
            mostrar_resultados_fecha(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, fixture, cantidad_fechas, sin_resultado)
        elif opcion == 5:
            buscar_equipo(equipos, matriz_puntos, matriz_goles_favor, matriz_goles_contra,cantidad_equipos, cantidad_fechas, sin_resultado)
        elif opcion == 6:
            mostrar_indicadores(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado, puntos_victoria)
        elif opcion == 7:
            mostrar_condiciones_destacables(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntos_derrota)
        elif opcion == 8:
            mostrar_resumen_general(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, cantidad_fechas, sin_resultado, puntos_derrota)
        elif opcion == 0:
            print("\n¡Gracias por usar el sistema! Hasta la próxima.")


if __name__ == "__main__":
    main()
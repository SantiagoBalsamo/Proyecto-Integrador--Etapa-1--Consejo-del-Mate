"""
Sistema principal
"""

from datos import (
    EQUIPOS, FIXTURE, CANTIDAD_FECHAS, GOLES_MAXIMOS, REGLAS_TORNEO,
    crear_matriz_puntos, crear_registro_partidos,
)
import operaciones as ops


def mostrar_menu(): #menu interactuivo
    print("\nTORNEO DE ESPORTS (FIFA) - MENÚ PRINCIPAL")
    print("1) Información general del torneo")
    print("2) Cargar resultado de un partido")
    print("3) Ver tabla de posiciones")
    print("4) Ver resultados de una fecha")
    print("5) Ver indicadores (promedios, diferencia de gol, efectividad)")
    print("6) Detectar condiciones destacables (invictos / estado crítico)")
    print("7) Resumen general del torneo")
    print("0) Salir")


def pedir_entero(mensaje, minimo, maximo): #valida que sea numero entero
    while True:
        texto = input(mensaje)
        valido, resultado = ops.validar_entero(texto, minimo, maximo)
        if valido:
            return resultado
        print(f"  Error: {resultado}")


def unir_con_comas(lista): #Devuelve los elementos de la lista separados por coma, en un solo texto
    texto = ""
    for i in range(len(lista)):
        if i == 0:
            texto = lista[i]
        else:
            texto = texto + ", " + lista[i]
    return texto


def mostrar_informacion_general():
    print("\n--- Información general del torneo ---")
    for regla in REGLAS_TORNEO:
        print(f"  - {regla}")
    print("\nEquipos participantes:")
    numero = 1
    for equipo in EQUIPOS:
        print(f"  {numero}. {equipo}")
        numero = numero + 1


def mostrar_fechas_disponibles():
    print("\nFechas del torneo:")
    for i in range(CANTIDAD_FECHAS):
        print(f"  Fecha {i + 1}")


def cargar_resultado(puntos, partidos):
    print("\n--- Cargar resultado de un partido ---")
    mostrar_fechas_disponibles()
    fecha = pedir_entero("Elegí el número de fecha: ", 1, CANTIDAD_FECHAS)
    fecha_idx = fecha - 1

    print(f"\nPartidos de la fecha {fecha}:")
    partidos_fecha = FIXTURE[fecha_idx]
    numero = 1
    for local_idx, visitante_idx in partidos_fecha:
        estado = "cargado" if ops.partido_cargado(partidos, fecha_idx, local_idx, visitante_idx) else "pendiente"
        print(f"  {numero}. {EQUIPOS[local_idx]} vs {EQUIPOS[visitante_idx]} ({estado})")
        numero = numero + 1

    numero_partido = pedir_entero("Elegí el número de partido: ", 1, len(partidos_fecha))
    local_idx, visitante_idx = partidos_fecha[numero_partido - 1]

    if ops.partido_cargado(partidos, fecha_idx, local_idx, visitante_idx):
        print("  Error: ese partido ya tiene un resultado cargado.")
        return

    goles_local = pedir_entero(f"Goles de {EQUIPOS[local_idx]}: ", 0, GOLES_MAXIMOS)
    goles_visitante = pedir_entero(f"Goles de {EQUIPOS[visitante_idx]}: ", 0, GOLES_MAXIMOS)

    ops.registrar_resultado(puntos, partidos, fecha_idx, local_idx, visitante_idx,
                             goles_local, goles_visitante)
    print("  Resultado cargado correctamente.")


def mostrar_tabla_posiciones(puntos, partidos):
    print("\n--- Tabla de posiciones ---")
    tabla = ops.tabla_de_posiciones(puntos, partidos)
    print("Pos - Equipo - Puntos - Diferencia de gol")
    posicion = 1
    for equipo, pts, dif in tabla:
        print(f"{posicion} - {equipo} - {pts} - {dif}")
        posicion = posicion + 1


def mostrar_resultados_fecha(partidos):
    mostrar_fechas_disponibles()
    fecha = pedir_entero("¿De qué fecha querés ver los resultados?: ", 1, CANTIDAD_FECHAS)
    resultados = ops.resultados_de_fecha(fecha - 1, partidos)
    print(f"\n--- Resultados de la fecha {fecha} ---")
    if not resultados:
        print("  Todavía no hay resultados cargados para esta fecha.")
        return
    for local, gf, gc, visitante in resultados:
        print(f"  {local} {gf} - {gc} {visitante}")


def mostrar_indicadores(puntos, partidos):
    print("\n--- Indicadores ---")
    promedios = ops.promedio_goles_favor(partidos)
    diferencias = ops.diferencia_de_gol(partidos)
    porcentajes = ops.porcentaje_efectividad(puntos, partidos)
    print("Equipo - Promedio goles a favor - Diferencia de gol - Efectividad")
    for i in range(len(EQUIPOS)):
        print(f"{EQUIPOS[i]} - {promedios[i]:.2f} - {diferencias[i]} - {porcentajes[i]:.1f}%")


def mostrar_condiciones_destacables(puntos, partidos):
    print("\n--- Condiciones destacables ---")
    invictos = ops.equipos_invictos(puntos, partidos)
    criticos = ops.equipos_en_estado_critico(puntos, partidos, 3)
    print("  Equipos invictos:", unir_con_comas(invictos) if invictos else "ninguno por el momento")
    print("  Equipos en estado crítico (0 puntos con 3+ partidos jugados):",
          unir_con_comas(criticos) if criticos else "ninguno por el momento")


def mostrar_resumen_general(puntos, partidos):
    print("\n=== RESUMEN GENERAL DEL TORNEO ===")
    total_partidos_posibles = CANTIDAD_FECHAS * (len(EQUIPOS) // 2)
    partidos_jugados = len(partidos)
    print(f"1) Partidos jugados: {partidos_jugados} de {total_partidos_posibles}")

    tabla = ops.tabla_de_posiciones(puntos, partidos)
    puntos_del_lider = tabla[0][1]
    lideres = []
    for equipo, pts, dif in tabla:
        if pts == puntos_del_lider:
            lideres.append(equipo)
    print(f"2) Líder del torneo: {unir_con_comas(lideres)} ({puntos_del_lider} puntos)")

    equipo_ataque, goles_ataque = ops.equipo_con_mas_goles_favor(partidos)
    print(f"3) Mejor ataque: {equipo_ataque} ({goles_ataque} goles a favor)")

    invictos = ops.equipos_invictos(puntos, partidos)
    print(f"4) Equipos invictos: {unir_con_comas(invictos) if invictos else 'ninguno'}")

    print("5) Top 3 del torneo:") #se toma el top 3 del torneo
    top_3 = tabla[:3]
    posicion = 1
    for equipo, pts, dif in top_3:
        print(f"   {posicion}. {equipo} - {pts} pts (dif. {dif})")
        posicion = posicion + 1


def main():
    puntos = crear_matriz_puntos()
    partidos = crear_registro_partidos()

    opcion = -1
    while opcion != 0:
        mostrar_menu()
        texto_opcion = input("Elegí una opción: ")
        valido, opcion = ops.validar_entero(texto_opcion, 0, 7)
        if not valido:
            print(f"  Error: {opcion}")
            opcion = -1
            continue

        if opcion == 1:
            mostrar_informacion_general()
        elif opcion == 2:
            cargar_resultado(puntos, partidos)
        elif opcion == 3:
            mostrar_tabla_posiciones(puntos, partidos)
        elif opcion == 4:
            mostrar_resultados_fecha(partidos)
        elif opcion == 5:
            mostrar_indicadores(puntos, partidos)
        elif opcion == 6:
            mostrar_condiciones_destacables(puntos, partidos)
        elif opcion == 7:
            mostrar_resumen_general(puntos, partidos)
        elif opcion == 0:
            print("\n¡Gracias por usar el sistema! Hasta la próxima.")


if __name__ == "__main__":
    main()
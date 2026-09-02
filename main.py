"""
Sistema de gestión de un torneo de eSports (FIFA) - Etapa 1.
Prototipo funcional en memoria: los datos se pierden al cerrar el programa.
Punto de entrada: menú interactivo por consola.
"""

from datos import (
    EQUIPOS, FIXTURE, CANTIDAD_FECHAS, REGLAS_TORNEO,
    crear_matriz_puntos, crear_registro_partidos,
)
import operaciones as ops


# ---------- Funciones de presentación (entrada/salida por consola) ----------

def mostrar_menu():
    print("\n=== TORNEO DE ESPORTS (FIFA) - MENÚ PRINCIPAL ===")
    print("1) Información general del torneo")
    print("2) Cargar resultado de un partido")
    print("3) Ver tabla de posiciones")
    print("4) Ver resultados de una fecha")
    print("5) Ver indicadores (promedios, diferencia de gol, efectividad)")
    print("6) Detectar condiciones destacables (invictos / estado crítico)")
    print("7) Resumen general del torneo")
    print("0) Salir")


def pedir_entero(mensaje, minimo=None, maximo=None):
    """Pide un entero por consola hasta que el usuario ingrese uno válido."""
    while True:
        texto = input(mensaje)
        valido, resultado = ops.validar_entero(texto, minimo, maximo)
        if valido:
            return resultado
        print(f"  Error: {resultado}")


def mostrar_informacion_general():
    print("\n--- Información general del torneo ---")
    for regla in REGLAS_TORNEO:
        print(f"  - {regla}")
    print("\nEquipos participantes:")
    for indice, equipo in enumerate(EQUIPOS, start=1):
        print(f"  {indice}. {equipo}")


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
    for numero, (local_idx, visitante_idx) in enumerate(partidos_fecha, start=1):
        estado = "cargado" if ops.partido_cargado(partidos, fecha_idx, local_idx, visitante_idx) else "pendiente"
        print(f"  {numero}. {EQUIPOS[local_idx]} vs {EQUIPOS[visitante_idx]} ({estado})")

    numero_partido = pedir_entero("Elegí el número de partido: ", 1, len(partidos_fecha))
    local_idx, visitante_idx = partidos_fecha[numero_partido - 1]

    if ops.partido_cargado(partidos, fecha_idx, local_idx, visitante_idx):
        print("  Error: ese partido ya tiene un resultado cargado (inconsistencia evitada).")
        return

    goles_local = pedir_entero(f"Goles de {EQUIPOS[local_idx]}: ", 0)
    goles_visitante = pedir_entero(f"Goles de {EQUIPOS[visitante_idx]}: ", 0)

    ops.registrar_resultado(puntos, partidos, fecha_idx, local_idx, visitante_idx,
                             goles_local, goles_visitante)
    print("  Resultado cargado correctamente.")


def mostrar_tabla_posiciones(puntos, partidos):
    print("\n--- Tabla de posiciones ---")
    tabla = ops.tabla_de_posiciones(puntos, partidos)
    print(f"{'Pos':<4}{'Equipo':<25}{'Pts':<6}{'Dif. Gol':<10}")
    for posicion, (equipo, pts, dif) in enumerate(tabla, start=1):
        print(f"{posicion:<4}{equipo:<25}{pts:<6}{dif:<10}")


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
    print(f"{'Equipo':<25}{'Prom. GF':<12}{'Dif. Gol':<12}{'Efectividad %':<15}")
    for equipo, prom, dif, efect in zip(EQUIPOS, promedios, diferencias, porcentajes):
        print(f"{equipo:<25}{prom:<12}{dif:<12}{efect:<15}")


def mostrar_condiciones_destacables(puntos, partidos):
    print("\n--- Condiciones destacables ---")
    invictos = ops.equipos_invictos(puntos, partidos)
    criticos = ops.equipos_en_estado_critico(puntos, partidos)
    print("  Equipos invictos:", ", ".join(invictos) if invictos else "ninguno por el momento")
    print("  Equipos en estado crítico (0 puntos tras 3+ fechas):",
          ", ".join(criticos) if criticos else "ninguno por el momento")


def mostrar_resumen_general(puntos, partidos):
    print("\n=== RESUMEN GENERAL DEL TORNEO ===")
    total_partidos = CANTIDAD_FECHAS * (len(EQUIPOS) // 2)
    jugados = len(partidos)
    print(f"1) Partidos jugados: {jugados} de {total_partidos}")

    tabla = ops.tabla_de_posiciones(puntos, partidos)
    lider_puntos = tabla[0][1]
    lideres = [equipo for equipo, pts, dif in tabla if pts == lider_puntos]
    print(f"2) Líder del torneo: {', '.join(lideres)} ({lider_puntos} puntos)")

    equipo_ataque, goles_ataque = ops.equipo_con_mas_goles_favor(partidos)
    print(f"3) Mejor ataque: {equipo_ataque} ({goles_ataque} goles a favor)")

    invictos = ops.equipos_invictos(puntos, partidos)
    print(f"4) Equipos invictos: {', '.join(invictos) if invictos else 'ninguno'}")

    print("5) Top 3 del torneo:")
    for posicion, (equipo, pts, dif) in enumerate(tabla[:3], start=1):
        print(f"   {posicion}. {equipo} - {pts} pts (dif. {dif})")


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

def obtener_equipos(): #lista de los equipos
    return [
        "Real Norte",
        "Atlético Sur",
        "Deportivo Central",
        "Unión FC",
        "Estudiantes del Oeste",
        "Talleres Andino",
        "Rayo Dorado",
        "Halcones FC",
        "Cóndor United",
        "Pumas del Litoral",
    ]


def obtener_puntos_victoria():
    return 3


def obtener_puntos_empate():
    return 1


def obtener_puntos_derrota():
    return 0


def obtener_goles_maximos(): #maximo de goles 
    return 20


def obtener_sin_resultado(): #valor centinela (es el valor en la tabla de partidos no cargados)
    return -1


def obtener_cantidad_equipos(equipos):
    return len(equipos)


def obtener_cantidad_fechas(equipos):
    return len(equipos) - 1


def obtener_reglas_torneo(cantidad_equipos, cantidad_fechas, puntos_victoria, puntos_empate, puntos_derrota): #tupla para mostrar datos en pantallas
    return (
        "Formato: Round Robin (todos contra todos, una rueda)",
        f"Cantidad de equipos: {cantidad_equipos}",
        f"Cantidad de fechas: {cantidad_fechas}",
        f"Puntos por victoria: {puntos_victoria}",
        f"Puntos por empate: {puntos_empate}",
        f"Puntos por derrota: {puntos_derrota}",
        "Criterio de desempate: diferencia de gol, luego goles a favor",
    )


def generar_fixture(equipos):
    indices = []
    for i in range(len(equipos)):
        indices.append(i)

    fixture = []
    for numero_fecha in range(len(equipos) - 1):
        partidos_de_la_fecha = []
        for i in range(len(equipos) // 2):
            local = indices[i]
            visitante = indices[len(equipos) - 1 - i]
            partidos_de_la_fecha.append((local, visitante))
        fixture.append(tuple(partidos_de_la_fecha))

        nuevos_indices = []
        nuevos_indices.append(indices[0])
        nuevos_indices.append(indices[len(indices) - 1])
        for i in range(1, len(indices) - 1):
            nuevos_indices.append(indices[i])
        indices = nuevos_indices

    return tuple(fixture)


def crear_matriz_puntos(cantidad_equipos, cantidad_fechas, sin_resultado): #matriz de puntos(fechas y partidos)
    matriz = []
    for indice_equipo in range(cantidad_equipos):
        fila = []
        for indice_fecha in range(cantidad_fechas):
            fila.append(sin_resultado)
        matriz.append(fila)
    return matriz


def crear_matriz_goles_favor(cantidad_equipos, cantidad_fechas, sin_resultado): #matriz goles a favor 
    matriz = []
    for indice_equipo in range(cantidad_equipos):
        fila = []
        for indice_fecha in range(cantidad_fechas):
            fila.append(sin_resultado)
        matriz.append(fila)
    return matriz


def crear_matriz_goles_contra(cantidad_equipos, cantidad_fechas, sin_resultado):#matriz goles en contra
    matriz = []
    for indice_equipo in range(cantidad_equipos):
        fila = []
        for indice_fecha in range(cantidad_fechas):
            fila.append(sin_resultado)
        matriz.append(fila)
    return matriz
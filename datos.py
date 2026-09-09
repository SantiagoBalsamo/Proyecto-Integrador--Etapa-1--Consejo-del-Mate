
#Datos de configuración

EQUIPOS = [
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
PUNTOS_VICTORIA = 3
PUNTOS_EMPATE = 1
PUNTOS_DERROTA = 0

CANTIDAD_EQUIPOS = len(EQUIPOS)
CANTIDAD_FECHAS = CANTIDAD_EQUIPOS - 1  # round robin a una rueda -> 9 fechas

REGLAS_TORNEO = (
    "Formato: Round Robin (todos contra todos, una rueda)",
    f"Cantidad de equipos: {CANTIDAD_EQUIPOS}",
    f"Cantidad de fechas: {CANTIDAD_FECHAS}",
    f"Puntos por victoria: {PUNTOS_VICTORIA}",
    f"Puntos por empate: {PUNTOS_EMPATE}",
    f"Puntos por derrota: {PUNTOS_DERROTA}",
    "Criterio de desempate: diferencia de gol",
) 


def generar_fixture(equipos):
    indices = list(range(len(equipos)))
    fixture = []
    for _ in range(len(equipos) - 1):
        partidos = []
        for i in range(len(equipos) // 2):
            local = indices[i]
            visitante = indices[len(equipos) - 1 - i]
            partidos.append((local, visitante))
        fixture.append(tuple(partidos))
        indices = [indices[0]] + [indices[-1]] + indices[1:-1]
    return tuple(fixture)


FIXTURE = generar_fixture(EQUIPOS)


def crear_matriz_puntos():
    return [[0 for _ in range(CANTIDAD_FECHAS)] for _ in range(CANTIDAD_EQUIPOS)]


def crear_registro_partidos():
    return []
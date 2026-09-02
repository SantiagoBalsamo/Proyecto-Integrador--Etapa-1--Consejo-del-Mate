"""
Módulo de datos.
Contiene las constantes del dominio (datos fijos, no se modifican durante
la ejecución) y las funciones que inicializan las estructuras de datos
que sí se actualizan en memoria mientras corre el programa.
"""

# --- Datos de configuración (tuplas: no deben modificarse) ---

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
]  # lista homogénea de nombres (cadenas)

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
)  # tupla: datos de configuración fijos


def generar_fixture(equipos):
    """
    Genera el fixture de un torneo round robin con el método del círculo.
    Devuelve una tupla de fechas (dato fijo, una vez generado no cambia);
    cada fecha es a su vez una tupla de partidos, y cada partido es una
    tupla (indice_local, indice_visitante) que referencia la lista EQUIPOS.
    """
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


# --- Estructuras que se actualizan durante la ejecución (solo en memoria) ---

def crear_matriz_puntos():
    """Única matriz del sistema: enteros homogéneos con los puntos obtenidos
    por cada equipo en cada fecha."""
    return [[0 for _ in range(CANTIDAD_FECHAS)] for _ in range(CANTIDAD_EQUIPOS)]


def crear_registro_partidos():
    """
    Lista (crece durante la ejecución) de partidos jugados. Cada partido
    se guarda como una tupla inmutable:
        (fecha_idx, local_idx, visitante_idx, goles_local, goles_visitante)
    Se usa tupla porque, una vez cargado un resultado, esos datos puntuales
    no deben modificarse.
    """
    return []
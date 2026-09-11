
EQUIPOS = [
    "Grupo 9",
    "Los Autores",
    "eXperience",
    "BlueSquad",
    "Consejo del Mate",
    "Grupo 6",
    "Juan de los Palotes",
    "Overflow",
    "Panini",
    "Grupo 10",
]  

PUNTOS_VICTORIA = 3
PUNTOS_EMPATE = 1
PUNTOS_DERROTA = 0
GOLES_MAXIMOS = 20  

CANTIDAD_EQUIPOS = len(EQUIPOS)
CANTIDAD_FECHAS = CANTIDAD_EQUIPOS - 1  

REGLAS_TORNEO = (
    "Formato: Round Robin (todos contra todos, una rueda)",
    f"Cantidad de equipos: {CANTIDAD_EQUIPOS}",
    f"Cantidad de fechas: {CANTIDAD_FECHAS}",
    f"Puntos por victoria: {PUNTOS_VICTORIA}",
    f"Puntos por empate: {PUNTOS_EMPATE}",
    f"Puntos por derrota: {PUNTOS_DERROTA}",
    "Criterio de desempate: diferencia de gol",
)  


def generar_fixture(equipos): #genera el fixture, devuelve tuplas
   
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


FIXTURE = generar_fixture(EQUIPOS)



def crear_matriz_puntos(): #matriz general, puntos obtenidos por cada fecha
    matriz = []
    for indice_equipo in range(CANTIDAD_EQUIPOS):
        fila = []
        for indice_fecha in range(CANTIDAD_FECHAS):
            fila.append(0)
        matriz.append(fila)
    return matriz


def crear_registro_partidos(): #lista vacia de partidos y crece mediante se cargan los resultados

    return []
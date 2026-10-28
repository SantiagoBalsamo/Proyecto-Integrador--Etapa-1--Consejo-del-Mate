"""
Módulo de datos.
No define variables globales: todo son funciones. Cada función devuelve
un dato de configuración o arma una estructura vacía; quien la llama
(main.py) guarda el resultado en una variable local y se lo pasa como
parámetro a las demás funciones que lo necesiten.

Cambios respecto de la Etapa 1:
- Los nombres de los equipos ya no están escritos acá: se leen de
  equipos.txt.
- La puntuación tampoco: se lee de configuracion.json, así se puede
  cambiar sin tocar el código (ver archivos.py).
- Acá quedan las reglas fijas del dominio (goles máximos, límite de
  estado crítico y mínimo de equipos), el valor centinela y las
  funciones que arman el fixture y las matrices.
"""


def obtener_goles_maximos():
    """Tope razonable para validar los goles de un partido."""
    return 20


def obtener_limite_estado_critico():
    """
    Regla del estado crítico: un equipo está en estado crítico cuando
    jugó al menos esta cantidad de partidos y tiene 0 puntos.
    """
    return 3


def obtener_minimo_equipos():
    """
    Mínimo de equipos del torneo. Con 4 equipos cada uno juega 3
    partidos, lo justo para que pueda darse el estado crítico.
    """
    return 4


def obtener_sin_resultado():
    """
    Valor centinela que marca, en las tres matrices, que un partido
    todavía no se jugó. Nunca es un resultado válido porque los goles
    y los puntos siempre se validan como mayores o iguales a 0.
    """
    return -1


def obtener_cantidad_equipos(equipos):
    return len(equipos)


def obtener_cantidad_fechas(equipos):
    """Round robin a una rueda: cada equipo juega una vez contra cada rival."""
    return len(equipos) - 1


def generar_fixture(equipos):
    """
    Genera el fixture de un torneo round robin con el método del círculo.
    Devuelve una tupla de fechas (dato fijo, una vez generado no cambia);
    cada fecha es una tupla de partidos, y cada partido es una tupla
    (indice_local, indice_visitante) que referencia la lista de equipos.
    Funciona con cualquier cantidad par de equipos, por eso la lista
    leída de equipos.txt se valida antes de llamar a esta función.
    """
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


def crear_matriz_puntos(cantidad_equipos, cantidad_fechas, sin_resultado):
    """
    Matriz homogénea de enteros: puntos obtenidos por cada equipo en cada
    fecha. Armada con comprensión de listas anidada: la lista de afuera
    recorre los equipos (filas) y la de adentro las fechas (columnas).
    """
    matriz = [[sin_resultado for indice_fecha in range(cantidad_fechas)] for indice_equipo in range(cantidad_equipos)]
    return matriz


def crear_matriz_goles_favor(cantidad_equipos, cantidad_fechas, sin_resultado):
    """Matriz homogénea de enteros: goles a favor de cada equipo en cada fecha."""
    matriz = [[sin_resultado for indice_fecha in range(cantidad_fechas)] for indice_equipo in range(cantidad_equipos)]
    return matriz


def crear_matriz_goles_contra(cantidad_equipos, cantidad_fechas, sin_resultado):
    """Matriz homogénea de enteros: goles en contra de cada equipo en cada fecha."""
    matriz = [[sin_resultado for indice_fecha in range(cantidad_fechas)] for indice_equipo in range(cantidad_equipos)]
    return matriz

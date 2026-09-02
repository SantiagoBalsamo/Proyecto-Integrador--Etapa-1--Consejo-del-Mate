"""
Módulo de operaciones.
Contiene validaciones, búsquedas, cálculos e informes sobre las
estructuras de datos del torneo. No debe depender de input(); solo
calcula y devuelve resultados para que main.py los presente.
"""

from datos import (
    EQUIPOS, FIXTURE, CANTIDAD_EQUIPOS,
    PUNTOS_VICTORIA, PUNTOS_EMPATE, PUNTOS_DERROTA,
)


# ---------- Validaciones ----------

def validar_entero(texto, minimo=None, maximo=None):
    """
    Convierte un texto a entero y valida rango opcional.
    Devuelve (True, valor) si es válido, o (False, mensaje_error) si no.
    """
    texto = texto.strip()
    if texto == "":
        return False, "el valor no puede estar vacío."
    try:
        valor = int(texto)
    except ValueError:
        return False, "el valor ingresado no es un número entero válido."
    if minimo is not None and valor < minimo:
        return False, f"el valor debe ser mayor o igual a {minimo}."
    if maximo is not None and valor > maximo:
        return False, f"el valor debe ser menor o igual a {maximo}."
    return True, valor


# ---------- Registro de resultados ----------

def calcular_puntos(goles_local, goles_visitante):
    """Devuelve (puntos_local, puntos_visitante) según el resultado del partido."""
    if goles_local > goles_visitante:
        return PUNTOS_VICTORIA, PUNTOS_DERROTA
    if goles_local < goles_visitante:
        return PUNTOS_DERROTA, PUNTOS_VICTORIA
    return PUNTOS_EMPATE, PUNTOS_EMPATE


def partido_cargado(partidos, fecha_idx, local_idx, visitante_idx):
    """Inconsistencia interna a evitar: indica si ese partido de esa fecha
    ya tiene un resultado registrado en la lista de partidos."""
    for f, local, visitante, _gl, _gv in partidos:
        if f == fecha_idx and local == local_idx and visitante == visitante_idx:
            return True
    return False


def registrar_resultado(puntos, partidos, fecha_idx, local_idx, visitante_idx,
                         goles_local, goles_visitante):
    """
    Actualiza la matriz de puntos para ambos equipos y agrega el partido
    (como tupla inmutable) a la lista de partidos jugados.
    """
    puntos_local, puntos_visitante = calcular_puntos(goles_local, goles_visitante)
    puntos[local_idx][fecha_idx] = puntos_local
    puntos[visitante_idx][fecha_idx] = puntos_visitante

    partidos.append((fecha_idx, local_idx, visitante_idx, goles_local, goles_visitante))


# ---------- Cálculos e indicadores ----------

def total_puntos_por_equipo(puntos):
    """Acumulación: total de puntos de cada equipo (comprensión de listas)."""
    return [sum(fila) for fila in puntos]


def total_goles_favor_por_equipo(partidos):
    """Acumulación: total de goles a favor de cada equipo, recorriendo la
    lista de partidos jugados (tuplas)."""
    totales = [0 for _ in range(CANTIDAD_EQUIPOS)]
    for _f, local, visitante, gl, gv in partidos:
        totales[local] += gl
        totales[visitante] += gv
    return totales


def total_goles_contra_por_equipo(partidos):
    """Total de goles en contra de cada equipo."""
    totales = [0 for _ in range(CANTIDAD_EQUIPOS)]
    for _f, local, visitante, gl, gv in partidos:
        totales[local] += gv
        totales[visitante] += gl
    return totales


def partidos_jugados_por_equipo(partidos):
    """Conteo: cantidad de partidos jugados por cada equipo."""
    conteo = [0 for _ in range(CANTIDAD_EQUIPOS)]
    for _f, local, visitante, _gl, _gv in partidos:
        conteo[local] += 1
        conteo[visitante] += 1
    return conteo


def fechas_jugadas_por_equipo(partidos):
    """Para cada equipo, lista de índices de fecha en los que jugó."""
    fechas = [[] for _ in range(CANTIDAD_EQUIPOS)]
    for f, local, visitante, _gl, _gv in partidos:
        fechas[local].append(f)
        fechas[visitante].append(f)
    return fechas


def promedio_goles_favor(partidos):
    """Cálculo: promedio de goles a favor por partido jugado, por equipo."""
    totales_gf = total_goles_favor_por_equipo(partidos)
    jugados = partidos_jugados_por_equipo(partidos)
    promedios = []
    for gf, pj in zip(totales_gf, jugados):
        promedios.append(round(gf / pj, 2) if pj > 0 else 0.0)
    return promedios


def diferencia_de_gol(partidos):
    """Cálculo: diferencia de gol (goles a favor - goles en contra) por equipo."""
    gf = total_goles_favor_por_equipo(partidos)
    gc = total_goles_contra_por_equipo(partidos)
    return [f - c for f, c in zip(gf, gc)]


def porcentaje_efectividad(puntos, partidos):
    """Cálculo: porcentaje de puntos obtenidos sobre los puntos posibles."""
    totales = total_puntos_por_equipo(puntos)
    jugados = partidos_jugados_por_equipo(partidos)
    porcentajes = []
    for total, pj in zip(totales, jugados):
        posibles = pj * PUNTOS_VICTORIA
        porcentajes.append(round((total / posibles) * 100, 1) if posibles > 0 else 0.0)
    return porcentajes


def tabla_de_posiciones(puntos, partidos):
    """
    Ordenamiento/ranking: arma la tabla de posiciones ordenada de mayor a
    menor por puntos y, como desempate, por diferencia de gol.
    Usa lambda como criterio de orden (sorted).
    """
    totales_puntos = total_puntos_por_equipo(puntos)
    dif_gol = diferencia_de_gol(partidos)
    tabla = list(zip(EQUIPOS, totales_puntos, dif_gol))
    return sorted(tabla, key=lambda fila: (fila[1], fila[2]), reverse=True)


def equipo_con_mas_goles_favor(partidos):
    """Máximo: equipo con más goles a favor en el torneo."""
    totales_gf = total_goles_favor_por_equipo(partidos)
    indice_max = totales_gf.index(max(totales_gf))
    return EQUIPOS[indice_max], totales_gf[indice_max]


def equipos_invictos(puntos, partidos):
    """
    Detección de condición destacable: equipos que jugaron al menos un
    partido y nunca perdieron (ningún resultado con 0 puntos en las
    fechas que efectivamente jugaron).
    """
    fechas_por_equipo = fechas_jugadas_por_equipo(partidos)
    invictos = []
    for indice, equipo in enumerate(EQUIPOS):
        resultados = [puntos[indice][f] for f in fechas_por_equipo[indice]]
        if resultados and PUNTOS_DERROTA not in resultados:
            invictos.append(equipo)
    return invictos


def equipos_en_estado_critico(puntos, partidos, limite_fechas=3):
    """
    Detección de condición destacable: equipos que, tras jugar al menos
    `limite_fechas` partidos, todavía no sumaron ningún punto.
    """
    fechas_por_equipo = fechas_jugadas_por_equipo(partidos)
    criticos = []
    for indice, equipo in enumerate(EQUIPOS):
        resultados = [puntos[indice][f] for f in fechas_por_equipo[indice]]
        if len(resultados) >= limite_fechas and sum(resultados) == 0:
            criticos.append(equipo)
    return criticos


def resultados_de_fecha(fecha_idx, partidos):
    """Consulta: resultados ya cargados de una fecha específica."""
    resultados = []
    for f, local_idx, visitante_idx, gl, gv in partidos:
        if f == fecha_idx:
            resultados.append((EQUIPOS[local_idx], gl, gv, EQUIPOS[visitante_idx]))
    return resultados
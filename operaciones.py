

from datos import (
    EQUIPOS, FIXTURE, CANTIDAD_EQUIPOS,
    PUNTOS_VICTORIA, PUNTOS_EMPATE, PUNTOS_DERROTA,
)


#Validaciones

def validar_entero(texto, minimo=None, maximo=None):
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


#Registro de resultados

def calcular_puntos(goles_local, goles_visitante):
    if goles_local > goles_visitante:
        return PUNTOS_VICTORIA, PUNTOS_DERROTA
    if goles_local < goles_visitante:
        return PUNTOS_DERROTA, PUNTOS_VICTORIA
    return PUNTOS_EMPATE, PUNTOS_EMPATE


def partido_cargado(partidos, fecha_idx, local_idx, visitante_idx):
    for f, local, visitante, _gl, _gv in partidos:
        if f == fecha_idx and local == local_idx and visitante == visitante_idx:
            return True
    return False


def registrar_resultado(puntos, partidos, fecha_idx, local_idx, visitante_idx,
                         goles_local, goles_visitante):
    puntos_local, puntos_visitante = calcular_puntos(goles_local, goles_visitante)
    puntos[local_idx][fecha_idx] = puntos_local
    puntos[visitante_idx][fecha_idx] = puntos_visitante

    partidos.append((fecha_idx, local_idx, visitante_idx, goles_local, goles_visitante))


#Cálculos e indicadores

def total_puntos_por_equipo(puntos):
    return [sum(fila) for fila in puntos]


def total_goles_favor_por_equipo(partidos):
    totales = [0 for _ in range(CANTIDAD_EQUIPOS)]
    for _f, local, visitante, gl, gv in partidos:
        totales[local] += gl
        totales[visitante] += gv
    return totales


def total_goles_contra_por_equipo(partidos):
    totales = [0 for _ in range(CANTIDAD_EQUIPOS)]
    for _f, local, visitante, gl, gv in partidos:
        totales[local] += gv
        totales[visitante] += gl
    return totales


def partidos_jugados_por_equipo(partidos):
    conteo = [0 for _ in range(CANTIDAD_EQUIPOS)]
    for _f, local, visitante, _gl, _gv in partidos:
        conteo[local] += 1
        conteo[visitante] += 1
    return conteo


def fechas_jugadas_por_equipo(partidos):
    fechas = [[] for _ in range(CANTIDAD_EQUIPOS)]
    for f, local, visitante, _gl, _gv in partidos:
        fechas[local].append(f)
        fechas[visitante].append(f)
    return fechas


def promedio_goles_favor(partidos):
    totales_gf = total_goles_favor_por_equipo(partidos)
    jugados = partidos_jugados_por_equipo(partidos)
    promedios = []
    for gf, pj in zip(totales_gf, jugados):
        promedios.append(round(gf / pj, 2) if pj > 0 else 0.0)
    return promedios


def diferencia_de_gol(partidos):
    gf = total_goles_favor_por_equipo(partidos)
    gc = total_goles_contra_por_equipo(partidos)
    return [f - c for f, c in zip(gf, gc)]


def porcentaje_efectividad(puntos, partidos):
    totales = total_puntos_por_equipo(puntos)
    jugados = partidos_jugados_por_equipo(partidos)
    porcentajes = []
    for total, pj in zip(totales, jugados):
        posibles = pj * PUNTOS_VICTORIA
        porcentajes.append(round((total / posibles) * 100, 1) if posibles > 0 else 0.0)
    return porcentajes


def tabla_de_posiciones(puntos, partidos):
    totales_puntos = total_puntos_por_equipo(puntos)
    dif_gol = diferencia_de_gol(partidos)
    tabla = list(zip(EQUIPOS, totales_puntos, dif_gol))
    return sorted(tabla, key=lambda fila: (fila[1], fila[2]), reverse=True)


def equipo_con_mas_goles_favor(partidos):
    totales_gf = total_goles_favor_por_equipo(partidos)
    indice_max = totales_gf.index(max(totales_gf))
    return EQUIPOS[indice_max], totales_gf[indice_max]


def equipos_invictos(puntos, partidos):
    fechas_por_equipo = fechas_jugadas_por_equipo(partidos)
    invictos = []
    for indice, equipo in enumerate(EQUIPOS):
        resultados = [puntos[indice][f] for f in fechas_por_equipo[indice]]
        if resultados and PUNTOS_DERROTA not in resultados:
            invictos.append(equipo)
    return invictos


def equipos_en_estado_critico(puntos, partidos, limite_fechas=3):
    fechas_por_equipo = fechas_jugadas_por_equipo(partidos)
    criticos = []
    for indice, equipo in enumerate(EQUIPOS):
        resultados = [puntos[indice][f] for f in fechas_por_equipo[indice]]
        if len(resultados) >= limite_fechas and sum(resultados) == 0:
            criticos.append(equipo)
    return criticos


def resultados_de_fecha(fecha_idx, partidos):
    resultados = []
    for f, local_idx, visitante_idx, gl, gv in partidos:
        if f == fecha_idx:
            resultados.append((EQUIPOS[local_idx], gl, gv, EQUIPOS[visitante_idx]))
    return resultados

from datos import (
    EQUIPOS, CANTIDAD_EQUIPOS,
    PUNTOS_VICTORIA, PUNTOS_EMPATE, PUNTOS_DERROTA,
)


# Validaciones

def validar_entero(texto, minimo, maximo): #convierte texto a entero y valida q este en maximo y minimo
    texto = texto.strip()
    if texto == "":
        return False, "el valor no puede estar vacío."
    try:
        valor = int(texto)
    except ValueError:
        return False, "el valor ingresado no es un número entero válido."
    if valor < minimo:
        return False, f"el valor debe ser mayor o igual a {minimo}."
    if valor > maximo:
        return False, f"el valor debe ser menor o igual a {maximo}."
    return True, valor


# Registro de resultados 

def calcular_puntos(goles_local, goles_visitante): #Devuelve (puntos_local, puntos_visitante) según el resultado del partido
    if goles_local > goles_visitante:
        return PUNTOS_VICTORIA, PUNTOS_DERROTA
    if goles_local < goles_visitante:
        return PUNTOS_DERROTA, PUNTOS_VICTORIA
    return PUNTOS_EMPATE, PUNTOS_EMPATE


def partido_cargado(partidos, fecha_idx, local_idx, visitante_idx): #indica si ese partido de esa fecha ya tiene resultado
    for fecha, local, visitante, goles_local, goles_visitante in partidos:
        if fecha == fecha_idx and local == local_idx and visitante == visitante_idx:
            return True
    return False


def registrar_resultado(puntos, partidos, fecha_idx, local_idx, visitante_idx,
 goles_local, goles_visitante):
    puntos_local, puntos_visitante = calcular_puntos(goles_local, goles_visitante)
    puntos[local_idx][fecha_idx] = puntos_local
    puntos[visitante_idx][fecha_idx] = puntos_visitante

    partidos.append((fecha_idx, local_idx, visitante_idx, goles_local, goles_visitante))


# ---------- Cálculos e indicadores ----------

def total_puntos_por_equipo(puntos): #suma total de puntos de cada equipo
    totales = []
    for i in range(CANTIDAD_EQUIPOS):
        totales.append(sum(puntos[i]))
    return totales


def total_goles_favor_por_equipo(partidos): #goles totales
    totales = []
    for i in range(CANTIDAD_EQUIPOS):
        totales.append(0)

    for fecha, local, visitante, goles_local, goles_visitante in partidos:
        totales[local] = totales[local] + goles_local
        totales[visitante] = totales[visitante] + goles_visitante
    return totales


def total_goles_contra_por_equipo(partidos): #goles en contra
    
    totales = []
    for i in range(CANTIDAD_EQUIPOS):
        totales.append(0)

    for fecha, local, visitante, goles_local, goles_visitante in partidos:
        totales[local] = totales[local] + goles_visitante
        totales[visitante] = totales[visitante] + goles_local
    return totales


def partidos_jugados_por_equipo(partidos): #conteo de cantidad partidos jugados x equipo
    conteo = []
    for i in range(CANTIDAD_EQUIPOS):
        conteo.append(0)

    for fecha, local, visitante, goles_local, goles_visitante in partidos:
        conteo[local] = conteo[local] + 1
        conteo[visitante] = conteo[visitante] + 1
    return conteo


def fechas_jugadas_por_equipo(partidos):
    fechas = []
    for i in range(CANTIDAD_EQUIPOS):
        fechas.append([])

    for fecha, local, visitante, goles_local, goles_visitante in partidos:
        fechas[local].append(fecha)
        fechas[visitante].append(fecha)
    return fechas


def promedio_goles_favor(partidos): #promedio de gf
    totales_gf = total_goles_favor_por_equipo(partidos)
    jugados = partidos_jugados_por_equipo(partidos)

    promedios = []
    for i in range(CANTIDAD_EQUIPOS):
        if jugados[i] > 0:
            promedios.append(totales_gf[i] / jugados[i])
        else:
            promedios.append(0.0)
    return promedios


def diferencia_de_gol(partidos): #goles a favor - goles en contra
    goles_favor = total_goles_favor_por_equipo(partidos)
    goles_contra = total_goles_contra_por_equipo(partidos)

    diferencias = []
    for i in range(CANTIDAD_EQUIPOS):
        diferencias.append(goles_favor[i] - goles_contra[i])
    return diferencias


def porcentaje_efectividad(puntos, partidos): #efectividad (porcentaje de partidos jugados y puntos)
    totales = total_puntos_por_equipo(puntos)
    jugados = partidos_jugados_por_equipo(partidos)

    porcentajes = []
    for i in range(CANTIDAD_EQUIPOS):
        puntos_posibles = jugados[i] * PUNTOS_VICTORIA
        if puntos_posibles > 0:
            porcentajes.append((totales[i] / puntos_posibles) * 100)
        else:
            porcentajes.append(0.0)
    return porcentajes


def tabla_de_posiciones(puntos, partidos): #arma la tabla de posiciones ordenada de mayor a menor por puntos y, como desempate, por diferencia de gol
    totales_puntos = total_puntos_por_equipo(puntos)
    diferencias = diferencia_de_gol(partidos)

    claves_de_orden = []
    for i in range(CANTIDAD_EQUIPOS):
        claves_de_orden.append((-totales_puntos[i], -diferencias[i], EQUIPOS[i]))

    claves_de_orden.sort()

    tabla_ordenada = []
    for puntos_negativos, diferencia_negativa, equipo in claves_de_orden:
        tabla_ordenada.append((equipo, -puntos_negativos, -diferencia_negativa))
    return tabla_ordenada


def equipo_con_mas_goles_favor(partidos): #equipo con mas goles a favor 
    totales_gf = total_goles_favor_por_equipo(partidos)

    indice_max = 0
    for i in range(CANTIDAD_EQUIPOS):
        if totales_gf[i] > totales_gf[indice_max]:
            indice_max = i
    return EQUIPOS[indice_max], totales_gf[indice_max]


def equipos_invictos(puntos, partidos): #equipos sin perder partido
    fechas_por_equipo = fechas_jugadas_por_equipo(partidos)

    invictos = []
    for i in range(CANTIDAD_EQUIPOS):
        jugo_algun_partido = len(fechas_por_equipo[i]) > 0
        perdio_algun_partido = False
        for fecha in fechas_por_equipo[i]:
            if puntos[i][fecha] == PUNTOS_DERROTA:
                perdio_algun_partido = True
        if jugo_algun_partido and not perdio_algun_partido:
            invictos.append(EQUIPOS[i])
    return invictos


def equipos_en_estado_critico(puntos, partidos, limite_partidos): #critico, jugaron al menos partidos y no obtuvieron puntos
    fechas_por_equipo = fechas_jugadas_por_equipo(partidos)

    criticos = []
    for i in range(CANTIDAD_EQUIPOS):
        cantidad_jugados = len(fechas_por_equipo[i])
        puntos_del_equipo = 0
        for fecha in fechas_por_equipo[i]:
            puntos_del_equipo = puntos_del_equipo + puntos[i][fecha]
        if cantidad_jugados >= limite_partidos and puntos_del_equipo == 0:
            criticos.append(EQUIPOS[i])
    return criticos


def resultados_de_fecha(fecha_idx, partidos): #consutal de fecha especifica
    resultados = []
    for fecha, local_idx, visitante_idx, goles_local, goles_visitante in partidos:
        if fecha == fecha_idx:
            resultados.append((EQUIPOS[local_idx], goles_local, goles_visitante, EQUIPOS[visitante_idx]))
    return resultados
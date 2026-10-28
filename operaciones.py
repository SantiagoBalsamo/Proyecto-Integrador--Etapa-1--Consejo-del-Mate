"""
Módulo de operaciones: la lógica del dominio.
No usa variables globales: todo lo que necesita cada función le llega
por parámetro. No hace input() ni print(): calcula y devuelve, y
main.py se encarga de mostrar. Cada función tiene un único punto de
salida (un solo return al final), sin break ni continue.

Cambios respecto de la Etapa 1:
- validar_entero pasó a validaciones.py.
- Las funciones que usaban puntos_victoria, puntos_empate y
  puntos_derrota ahora reciben un solo diccionario: puntuacion, que se
  lee de configuracion.json.
- Nuevo: goles_por_fecha, fecha_con_mas_goles y las líneas del
  fixture (para la opción 4 y para exportar a fixture.txt).
"""


# ---------- Registro de resultados ----------

def calcular_puntos(goles_local, goles_visitante, puntuacion):
    """Devuelve (puntos_local, puntos_visitante) según el marcador,
    consultando el diccionario de puntuación por clave."""
    if goles_local > goles_visitante:
        puntos_local = puntuacion["victoria"]
        puntos_visitante = puntuacion["derrota"]
    elif goles_local < goles_visitante:
        puntos_local = puntuacion["derrota"]
        puntos_visitante = puntuacion["victoria"]
    else:
        puntos_local = puntuacion["empate"]
        puntos_visitante = puntuacion["empate"]

    return puntos_local, puntos_visitante


def partido_cargado(matriz_puntos, fecha_idx, equipo_idx, sin_resultado):
    """Inconsistencia interna a evitar: indica si ese equipo ya tiene
    resultado cargado en esa fecha (la celda dejó de ser SIN_RESULTADO)."""
    return matriz_puntos[equipo_idx][fecha_idx] != sin_resultado


def registrar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                         fecha_idx, local_idx, visitante_idx,
                         goles_local, goles_visitante, puntuacion):
    """Actualiza las tres matrices, en las celdas de ambos equipos, para esa
    fecha. No devuelve nada: las matrices son listas (mutables), así que
    el cambio queda en las originales."""
    puntos_local, puntos_visitante = calcular_puntos(goles_local, goles_visitante, puntuacion)

    matriz_puntos[local_idx][fecha_idx] = puntos_local
    matriz_puntos[visitante_idx][fecha_idx] = puntos_visitante

    matriz_goles_favor[local_idx][fecha_idx] = goles_local
    matriz_goles_favor[visitante_idx][fecha_idx] = goles_visitante

    matriz_goles_contra[local_idx][fecha_idx] = goles_visitante
    matriz_goles_contra[visitante_idx][fecha_idx] = goles_local


# ---------- Cálculos e indicadores ----------

def total_por_equipo(matriz, cantidad_equipos, sin_resultado):
    """Acumulación: total de una matriz (puntos, goles a favor o en contra)
    por cada equipo, ignorando las celdas sin resultado todavía."""
    totales = []
    for i in range(cantidad_equipos):
        total = 0
        for valor in matriz[i]:
            if valor != sin_resultado:
                total = total + valor
        totales.append(total)
    return totales


def partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado):
    """Conteo: cantidad de celdas con resultado cargado, por equipo."""
    conteo = []
    for i in range(cantidad_equipos):
        cantidad = 0
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                cantidad = cantidad + 1
        conteo.append(cantidad)
    return conteo


def promedio_goles_favor(matriz_goles_favor, matriz_puntos, cantidad_equipos, sin_resultado):
    """Cálculo: promedio de goles a favor por partido jugado, por equipo."""
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)

    promedios = []
    for i in range(cantidad_equipos):
        if jugados[i] > 0:
            promedios.append(totales_gf[i] / jugados[i])
        else:
            promedios.append(0.0)
    return promedios


def diferencia_de_gol(matriz_goles_favor, matriz_goles_contra, cantidad_equipos, sin_resultado):
    """Cálculo: diferencia de gol (goles a favor - goles en contra) por equipo."""
    goles_favor = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    goles_contra = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)

    diferencias = []
    for i in range(cantidad_equipos):
        diferencias.append(goles_favor[i] - goles_contra[i])
    return diferencias


def porcentaje_efectividad(matriz_puntos, cantidad_equipos, sin_resultado, puntuacion):
    """Cálculo: porcentaje de puntos obtenidos sobre los puntos posibles
    (partidos jugados x puntos por victoria)."""
    totales = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)

    porcentajes = []
    for i in range(cantidad_equipos):
        puntos_posibles = jugados[i] * puntuacion["victoria"]
        if puntos_posibles > 0:
            porcentajes.append((totales[i] / puntos_posibles) * 100)
        else:
            porcentajes.append(0.0)
    return porcentajes


def tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                         equipos, cantidad_equipos, sin_resultado):
    """
    Ordenamiento/ranking: arma la tabla de posiciones ordenada por puntos,
    luego diferencia de gol, y luego goles a favor. Usa lambda como
    criterio de orden dentro de sorted().
    """
    totales_puntos = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    totales_gc = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)

    tabla = []
    for i in range(cantidad_equipos):
        diferencia = totales_gf[i] - totales_gc[i]
        tabla.append((equipos[i], totales_puntos[i], diferencia, totales_gf[i]))

    tabla_ordenada = sorted(tabla, key=lambda fila: (fila[1], fila[2], fila[3]), reverse=True)
    return tabla_ordenada


def equipo_con_mas_goles_favor(matriz_goles_favor, equipos, cantidad_equipos, sin_resultado):
    """Máximo: equipo con más goles a favor en el torneo."""
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)

    indice_max = 0
    for i in range(cantidad_equipos):
        if totales_gf[i] > totales_gf[indice_max]:
            indice_max = i
    return equipos[indice_max], totales_gf[indice_max]


def equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntuacion):
    """Detección de condición destacable: equipos que jugaron al menos un
    partido y nunca perdieron."""
    invictos = []
    for i in range(cantidad_equipos):
        jugo_algun_partido = False
        perdio_algun_partido = False
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                jugo_algun_partido = True
                if valor == puntuacion["derrota"]:
                    perdio_algun_partido = True
        if jugo_algun_partido and not perdio_algun_partido:
            invictos.append(equipos[i])
    return invictos


def equipos_en_estado_critico(matriz_puntos, equipos, cantidad_equipos, sin_resultado, limite_partidos):
    """Detección de condición crítica: equipos que jugaron al menos
    `limite_partidos` partidos y todavía no sumaron ningún punto."""
    criticos = []
    for i in range(cantidad_equipos):
        cantidad_jugados = 0
        puntos_del_equipo = 0
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                cantidad_jugados = cantidad_jugados + 1
                puntos_del_equipo = puntos_del_equipo + valor
        if cantidad_jugados >= limite_partidos and puntos_del_equipo == 0:
            criticos.append(equipos[i])
    return criticos


def partidos_jugados_del_torneo(matriz_puntos, cantidad_equipos, sin_resultado):
    """Conteo: partidos jugados en todo el torneo. Cada partido ocupa dos
    celdas (una por equipo), por eso se divide por 2."""
    celdas_jugadas = 0
    for i in range(cantidad_equipos):
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                celdas_jugadas = celdas_jugadas + 1
    return celdas_jugadas // 2


# ---------- Goles por fecha (diccionario acumulador) ----------

def goles_por_fecha(matriz_goles_favor, cantidad_equipos, cantidad_fechas, sin_resultado):
    """
    Diccionario acumulador {numero_de_fecha: goles_totales}.
    Para cada fecha suma su columna en matriz_goles_favor, salteando las
    celdas en SIN_RESULTADO. Alcanza con los goles a favor: cada gol del
    partido es gol a favor de uno de los dos equipos, así que no se
    cuenta dos veces. Las fechas se numeran desde 1.
    """
    goles = {}
    for fecha_idx in range(cantidad_fechas):
        total = 0
        for equipo_idx in range(cantidad_equipos):
            valor = matriz_goles_favor[equipo_idx][fecha_idx]
            if valor != sin_resultado:
                total = total + valor
        goles[fecha_idx + 1] = total
    return goles


def fecha_con_mas_goles(goles_fecha):
    """
    Devuelve (maximo, fechas): la mayor cantidad de goles en una fecha y
    la lista de fechas que la alcanzan (puede haber empate).
    Usa max() sobre los valores del diccionario y items() para recorrerlo.
    """
    maximo = max(goles_fecha.values())
    fechas = []
    for fecha, goles in goles_fecha.items():
        if goles == maximo:
            fechas.append(fecha)
    return maximo, fechas


# ---------- Consulta por fecha y fixture ----------

def lineas_de_fecha(fecha_idx, fixture, equipos, matriz_goles_favor, sin_resultado):
    """
    Consulta filtrada por fecha: arma una línea de texto por partido de
    esa fecha. Los partidos jugados muestran el resultado; los
    pendientes, "vs". La usan la opción 4 y la exportación del fixture.
    """
    lineas = []
    for local_idx, visitante_idx in fixture[fecha_idx]:
        goles_local = matriz_goles_favor[local_idx][fecha_idx]
        goles_visitante = matriz_goles_favor[visitante_idx][fecha_idx]
        if goles_local != sin_resultado:
            lineas.append(f"  {equipos[local_idx]} {goles_local} - {goles_visitante} {equipos[visitante_idx]}")
        else:
            lineas.append(f"  {equipos[local_idx]} vs {equipos[visitante_idx]}")
    return lineas


def lineas_del_fixture(fixture, equipos, matriz_goles_favor, cantidad_equipos,
                        cantidad_fechas, sin_resultado):
    """Arma todo el texto del fixture, fecha por fecha, para escribirlo en
    fixture.txt. Devuelve una lista de líneas (sin el salto de línea)."""
    lineas = []
    lineas.append(f"FIXTURE - {cantidad_equipos} equipos, {cantidad_fechas} fechas")
    for fecha_idx in range(cantidad_fechas):
        lineas.append("")
        lineas.append(f"Fecha {fecha_idx + 1}")
        for linea in lineas_de_fecha(fecha_idx, fixture, equipos, matriz_goles_favor, sin_resultado):
            lineas.append(linea)
    return lineas


# ---------- Búsqueda de equipo ----------

def buscar_equipo_por_nombre(equipos, nombre_buscado, cantidad_equipos):
    """
    Búsqueda: recorre la lista de equipos y devuelve el índice del que
    coincide con el nombre buscado (sin importar mayúsculas/minúsculas).
    Devuelve -1 si no se encontró ninguno (identificador no registrado).
    """
    nombre_normalizado = nombre_buscado.upper()
    indice_encontrado = -1
    for i in range(cantidad_equipos):
        if equipos[i].upper() == nombre_normalizado:
            indice_encontrado = i
    return indice_encontrado


def informacion_equipo(indice_equipo, matriz_puntos, matriz_goles_favor, matriz_goles_contra,
                        cantidad_equipos, cantidad_fechas, sin_resultado):
    """
    Arma la información de un equipo puntual: puntos, goles a favor,
    goles en contra, partidos jugados y partidos que le quedan por jugar.
    """
    totales_puntos = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    totales_gc = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)

    puntos_equipo = totales_puntos[indice_equipo]
    goles_favor_equipo = totales_gf[indice_equipo]
    goles_contra_equipo = totales_gc[indice_equipo]
    partidos_jugados_equipo = jugados[indice_equipo]
    partidos_restantes_equipo = cantidad_fechas - partidos_jugados_equipo

    return (puntos_equipo, goles_favor_equipo, goles_contra_equipo,
            partidos_jugados_equipo, partidos_restantes_equipo)

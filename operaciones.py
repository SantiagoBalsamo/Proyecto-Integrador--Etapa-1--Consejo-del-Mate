
# Validaciones

def validar_entero(texto, minimo, maximo):# convierte el texto en entero(sin espacio) y valida max y min
    texto = texto.strip()
    es_valido = True
    resultado = None

    if texto == "":
        es_valido = False
        resultado = "el valor no puede estar vacío."
    else:
        try:
            valor = int(texto)
            if valor < minimo:
                es_valido = False
                resultado = f"el valor debe ser mayor o igual a {minimo}."
            elif valor > maximo:
                es_valido = False
                resultado = f"el valor debe ser menor o igual a {maximo}."
            else:
                resultado = valor
        except ValueError:
            es_valido = False
            resultado = "el valor ingresado no es un número entero válido."

    return es_valido, resultado


# Registro de resultados

def calcular_puntos(goles_local, goles_visitante, puntos_victoria, puntos_empate, puntos_derrota):
    if goles_local > goles_visitante:
        puntos_local = puntos_victoria
        puntos_visitante = puntos_derrota
    elif goles_local < goles_visitante:
        puntos_local = puntos_derrota
        puntos_visitante = puntos_victoria
    else:
        puntos_local = puntos_empate
        puntos_visitante = puntos_empate

    return puntos_local, puntos_visitante


def partido_cargado(matriz_puntos, fecha_idx, equipo_idx, sin_resultado): # cambia la celda a sin resultado(-1) a celda con resultado
    return matriz_puntos[equipo_idx][fecha_idx] != sin_resultado


def registrar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra,fecha_idx, local_idx, visitante_idx,goles_local, goles_visitante,puntos_victoria, puntos_empate, puntos_derrota):
    puntos_local, puntos_visitante = calcular_puntos(
        goles_local, goles_visitante, puntos_victoria, puntos_empate, puntos_derrota)

    matriz_puntos[local_idx][fecha_idx] = puntos_local
    matriz_puntos[visitante_idx][fecha_idx] = puntos_visitante

    matriz_goles_favor[local_idx][fecha_idx] = goles_local
    matriz_goles_favor[visitante_idx][fecha_idx] = goles_visitante

    matriz_goles_contra[local_idx][fecha_idx] = goles_visitante
    matriz_goles_contra[visitante_idx][fecha_idx] = goles_local


# Cálculos e indicadores 

def total_por_equipo(matriz, cantidad_equipos, sin_resultado): #totales
    totales = []
    for i in range(cantidad_equipos):
        total = 0
        for valor in matriz[i]:
            if valor != sin_resultado:
                total = total + valor
        totales.append(total)
    return totales


def partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado): #cantidad de celdas con resultado cargado, por equipo
    conteo = []
    for i in range(cantidad_equipos):
        cantidad = 0
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                cantidad = cantidad + 1
        conteo.append(cantidad)
    return conteo


def promedio_goles_favor(matriz_goles_favor, matriz_puntos, cantidad_equipos, sin_resultado): #promedio de goles a vor por partido jugado
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)

    promedios = []
    for i in range(cantidad_equipos):
        if jugados[i] > 0:
            promedios.append(totales_gf[i] / jugados[i])
        else:
            promedios.append(0.0)
    return promedios


def diferencia_de_gol(matriz_goles_favor, matriz_goles_contra, cantidad_equipos, sin_resultado): #goles a favor - goles en contra
    goles_favor = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    goles_contra = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)

    diferencias = []
    for i in range(cantidad_equipos):
        diferencias.append(goles_favor[i] - goles_contra[i])
    return diferencias


def porcentaje_efectividad(matriz_puntos, cantidad_equipos, sin_resultado, puntos_victoria): #porcentaje de puntos obtenidos sobre los puntos posibles
    totales = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)

    porcentajes = []
    for i in range(cantidad_equipos):
        puntos_posibles = jugados[i] * puntos_victoria
        if puntos_posibles > 0:
            porcentajes.append((totales[i] / puntos_posibles) * 100)
        else:
            porcentajes.append(0.0)
    return porcentajes


def tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, cantidad_equipos, sin_resultado): #arma la tabla de posiciones ordenada por puntos,luego diferencia de gol, y luego goles a favor. Usa lambda comocriterio de orden dentro de sorted()
  
    totales_puntos = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    totales_gc = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)

    tabla = []
    for i in range(cantidad_equipos):
        diferencia = totales_gf[i] - totales_gc[i]
        tabla.append((equipos[i], totales_puntos[i], diferencia, totales_gf[i]))

    tabla_ordenada = sorted(tabla, key=lambda fila: (fila[1], fila[2], fila[3]), reverse=True)
    return tabla_ordenada


def equipo_con_mas_goles_favor(matriz_goles_favor, equipos, cantidad_equipos, sin_resultado): #equipo con mas goles a favor
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)

    indice_max = 0
    for i in range(cantidad_equipos):
        if totales_gf[i] > totales_gf[indice_max]:
            indice_max = i
    return equipos[indice_max], totales_gf[indice_max]


def equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntos_derrota): #invicto 
    invictos = []
    for i in range(cantidad_equipos):
        jugo_algun_partido = False
        perdio_algun_partido = False
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                jugo_algun_partido = True
                if valor == puntos_derrota:
                    perdio_algun_partido = True
        if jugo_algun_partido and not perdio_algun_partido:
            invictos.append(equipos[i])
    return invictos


def equipos_en_estado_critico(matriz_puntos, equipos, cantidad_equipos, sin_resultado, limite_partidos): #estado critico (0 putos en +3 partidos)
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


def resultados_de_fecha(fecha_idx, matriz_puntos, matriz_goles_favor, matriz_goles_contra,equipos, fixture, sin_resultado): #recorre el fixture
    resultados = []
    for local_idx, visitante_idx in fixture[fecha_idx]:
        if matriz_puntos[local_idx][fecha_idx] != sin_resultado:
            gf_local = matriz_goles_favor[local_idx][fecha_idx]
            gc_local = matriz_goles_contra[local_idx][fecha_idx]
            resultados.append((equipos[local_idx], gf_local, gc_local, equipos[visitante_idx]))
    return resultados
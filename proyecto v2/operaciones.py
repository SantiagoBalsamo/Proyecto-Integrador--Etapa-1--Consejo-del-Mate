def validar_entero(texto, minimo, maximo):
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

#Registro de resultados

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


def partido_cargado(matriz_puntos, fecha_idx, equipo_idx, sin_resultado):
    return matriz_puntos[equipo_idx][fecha_idx] != sin_resultado

def registrar_resultado(matriz_puntos, matriz_goles_favor, matriz_goles_contra,fecha_idx, local_idx, visitante_idx,goles_local, goles_visitante,puntos_victoria, puntos_empate, puntos_derrota):
    puntos_local, puntos_visitante = calcular_puntos(goles_local, goles_visitante, puntos_victoria, puntos_empate, puntos_derrota)

    matriz_puntos[local_idx][fecha_idx] = puntos_local
    matriz_puntos[visitante_idx][fecha_idx] = puntos_visitante

    matriz_goles_favor[local_idx][fecha_idx] = goles_local
    matriz_goles_favor[visitante_idx][fecha_idx] = goles_visitante

    matriz_goles_contra[local_idx][fecha_idx] = goles_visitante
    matriz_goles_contra[visitante_idx][fecha_idx] = goles_local


#Cálculos e indicadores 

def total_por_equipo(matriz, cantidad_equipos, sin_resultado):
    totales = []
    for i in range(cantidad_equipos):
        total = 0
        for valor in matriz[i]:
            if valor != sin_resultado:
                total = total + valor
        totales.append(total)
    return totales


def partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado): #cuenta las celdas con resultado por equipo
    conteo = []
    for i in range(cantidad_equipos):
        cantidad = 0
        for valor in matriz_puntos[i]:
            if valor != sin_resultado:
                cantidad = cantidad + 1
        conteo.append(cantidad)
    return conteo


def resultados_por_equipo(matriz_puntos, cantidad_equipos, puntos_victoria, puntos_empate, puntos_derrota):
    ganados = []
    empatados = []
    perdidos = []
    for i in range(cantidad_equipos):
        pg = 0
        pe = 0
        pp = 0
        for valor in matriz_puntos[i]:
            if valor == puntos_victoria:
                pg = pg + 1
            elif valor == puntos_empate:
                pe = pe + 1
            elif valor == puntos_derrota:
                pp = pp + 1
        ganados.append(pg)
        empatados.append(pe)
        perdidos.append(pp)
    return ganados, empatados, perdidos


def promedio_goles_favor(matriz_goles_favor, matriz_puntos, cantidad_equipos, sin_resultado):
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
    goles_favor = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    goles_contra = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)

    diferencias = []
    for i in range(cantidad_equipos):
        diferencias.append(goles_favor[i] - goles_contra[i])
    return diferencias


def porcentaje_efectividad(matriz_puntos, cantidad_equipos, sin_resultado, puntos_victoria):
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


def tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra, equipos,
                         cantidad_equipos, sin_resultado, puntos_victoria, puntos_empate, puntos_derrota):

    totales_puntos = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    totales_gc = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    ganados, empatados, perdidos = resultados_por_equipo(matriz_puntos, cantidad_equipos, puntos_victoria, puntos_empate, puntos_derrota)

    tabla = []
    for i in range(cantidad_equipos):
        diferencia = totales_gf[i] - totales_gc[i]
        fila = (
            equipos[i],        
            jugados[i],        
            ganados[i],        
            empatados[i],      
            perdidos[i],       
            totales_gf[i],     
            totales_gc[i],     
            diferencia,        
            totales_puntos[i], 
        )
        tabla.append(fila)

    tabla_alfabetica = sorted(tabla, key=lambda fila: fila[0])
    tabla_ordenada = sorted(tabla_alfabetica, key=lambda fila: (fila[8], fila[7], fila[5]), reverse=True)
    return tabla_ordenada


def equipos_con_mejor_ataque(matriz_goles_favor, equipos, cantidad_equipos, sin_resultado):
    
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    maximo = max(totales_gf)

    mejores = []
    for i in range(cantidad_equipos):
        if totales_gf[i] == maximo:
            mejores.append(equipos[i])
    return mejores, maximo


def equipos_con_mejor_defensa(matriz_goles_contra, matriz_puntos, equipos, cantidad_equipos, sin_resultado):
    
    totales_gc = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)

    indices_validos = []
    for i in range(cantidad_equipos):
        if jugados[i] > 0:
            indices_validos.append(i)

    if len(indices_validos) == 0:
        return [], None

    minimo = totales_gc[indices_validos[0]]
    for i in indices_validos:
        if totales_gc[i] < minimo:
            minimo = totales_gc[i]

    mejores = []
    for i in indices_validos:
        if totales_gc[i] == minimo:
            mejores.append(equipos[i])
    return mejores, minimo


def equipos_invictos(matriz_puntos, equipos, cantidad_equipos, sin_resultado, puntos_derrota):
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


def equipos_en_estado_critico(matriz_puntos, equipos, cantidad_equipos, sin_resultado, limite_partidos):
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


def contar_empates_torneo(matriz_puntos, cantidad_equipos, puntos_empate):
    celdas_en_empate = 0
    for i in range(cantidad_equipos):
        for valor in matriz_puntos[i]:
            if valor == puntos_empate:
                celdas_en_empate = celdas_en_empate + 1
    return celdas_en_empate // 2


def partidos_jugados_torneo(matriz_puntos, cantidad_equipos, sin_resultado):
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    total = 0
    for valor in jugados:
        total = total + valor
    return total // 2


def goles_totales_torneo(matriz_goles_favor, cantidad_equipos, sin_resultado):
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    total = 0
    for valor in totales_gf:
        total = total + valor
    return total


def promedio_goles_torneo(matriz_goles_favor, matriz_puntos, cantidad_equipos, sin_resultado):
    goles_totales = goles_totales_torneo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    partidos = partidos_jugados_torneo(matriz_puntos, cantidad_equipos, sin_resultado)
    if partidos > 0:
        return goles_totales / partidos
    return 0.0


def resultados_de_fecha(fecha_idx, matriz_puntos, matriz_goles_favor, matriz_goles_contra, equipos, fixture, sin_resultado):
    jugados = []
    pendientes = []
    for local_idx, visitante_idx in fixture[fecha_idx]:
        if matriz_puntos[local_idx][fecha_idx] != sin_resultado:
            gf_local = matriz_goles_favor[local_idx][fecha_idx]
            gc_local = matriz_goles_contra[local_idx][fecha_idx]
            jugados.append((equipos[local_idx], gf_local, gc_local, equipos[visitante_idx]))
        else:
            pendientes.append((equipos[local_idx], equipos[visitante_idx]))
    return jugados, pendientes


def buscar_equipo_por_nombre(equipos, nombre_buscado, cantidad_equipos):
    nombre_normalizado = nombre_buscado.upper()
    indice_encontrado = -1
    for i in range(cantidad_equipos):
        if equipos[i].upper() == nombre_normalizado:
            indice_encontrado = i
    return indice_encontrado


def informacion_equipo(indice_equipo, matriz_puntos, matriz_goles_favor, matriz_goles_contra, equipos,
                        cantidad_equipos, cantidad_fechas, sin_resultado,
                        puntos_victoria, puntos_empate, puntos_derrota): 
    tabla = tabla_de_posiciones(matriz_puntos, matriz_goles_favor, matriz_goles_contra, equipos,
                                 cantidad_equipos, sin_resultado, puntos_victoria, puntos_empate, puntos_derrota)
    nombre_equipo = equipos[indice_equipo]
    posicion_equipo = 0
    for i in range(len(tabla)):
        if tabla[i][0] == nombre_equipo:
            posicion_equipo = i + 1

    totales_puntos = total_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    totales_gf = total_por_equipo(matriz_goles_favor, cantidad_equipos, sin_resultado)
    totales_gc = total_por_equipo(matriz_goles_contra, cantidad_equipos, sin_resultado)
    jugados = partidos_jugados_por_equipo(matriz_puntos, cantidad_equipos, sin_resultado)
    ganados, empatados, perdidos = resultados_por_equipo(matriz_puntos, cantidad_equipos, puntos_victoria, puntos_empate, puntos_derrota)
    porcentajes = porcentaje_efectividad(matriz_puntos, cantidad_equipos, sin_resultado, puntos_victoria)

    puntos_equipo = totales_puntos[indice_equipo]
    goles_favor_equipo = totales_gf[indice_equipo]
    goles_contra_equipo = totales_gc[indice_equipo]
    diferencia_equipo = goles_favor_equipo - goles_contra_equipo
    partidos_jugados_equipo = jugados[indice_equipo]
    partidos_restantes_equipo = cantidad_fechas - partidos_jugados_equipo
    ganados_equipo = ganados[indice_equipo]
    empatados_equipo = empatados[indice_equipo]
    perdidos_equipo = perdidos[indice_equipo]
    efectividad_equipo = porcentajes[indice_equipo]

    return (posicion_equipo, puntos_equipo, goles_favor_equipo, goles_contra_equipo, diferencia_equipo,
            partidos_jugados_equipo, partidos_restantes_equipo, ganados_equipo, empatados_equipo,
            perdidos_equipo, efectividad_equipo)
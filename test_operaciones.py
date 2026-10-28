"""
Pruebas unitarias de operaciones.py (pruebas 3, 4 y 5 del alcance).
No usan input, no leen archivos y no dependen de lo que se muestra por
pantalla: cada prueba arma sus propios datos y comprueba el resultado
con assert. El valor -1 representa SIN_RESULTADO (partido no jugado).
"""

import operaciones as ops


def test_3_calculo_de_puntos_de_un_partido():
    """Cálculo simple: un 2 a 1 da 3 puntos al local y 0 al visitante."""
    puntuacion = {"victoria": 3, "empate": 1, "derrota": 0}
    assert ops.calcular_puntos(2, 1, puntuacion) == (3, 0)


def test_4_goles_por_fecha():
    """Acumulación por clave: suma la columna de cada fecha y saltea los -1."""
    matriz_goles_favor = [
        [2, 1, -1],
        [1, 3, -1],
        [0, 0, -1],
        [0, 0, -1],
    ]
    assert ops.goles_por_fecha(matriz_goles_favor, 4, 3, -1) == {1: 3, 2: 4, 3: 0}


def test_5_equipo_con_tres_derrotas_en_estado_critico():
    """Condición crítica: con 3 derrotas está en estado crítico; con 2, todavía no."""
    equipos = ["Real Norte", "Atlético Sur", "Deportivo Central", "Unión FC"]
    matriz_puntos = [
        [0, 0, 0],
        [0, 0, -1],
        [3, 3, 3],
        [3, 3, -1],
    ]
    assert ops.equipos_en_estado_critico(matriz_puntos, equipos, 4, -1, 3) == ["Real Norte"]

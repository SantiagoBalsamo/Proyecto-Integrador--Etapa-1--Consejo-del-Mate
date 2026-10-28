"""
Pruebas unitarias de validaciones.py (pruebas 1, 2, 6 y 7 del alcance).
No usan input, no leen archivos y no dependen de lo que se muestra por
pantalla: cada prueba arma sus propios datos y comprueba el resultado
con assert.
"""

import validaciones


def test_1_usuario_con_formato_correcto():
    """Validación correcta: "admin" cumple el formato y se devuelve igual."""
    assert validaciones.validar_usuario("admin") == "admin"


def test_2_contrasena_corta_lanza_excepcion():
    """Validación incorrecta: "ab" tiene menos de 6 caracteres y debe lanzar ValueError."""
    lanzo_error = False
    try:
        validaciones.validar_contrasena("ab")
    except ValueError:
        lanzo_error = True
    assert lanzo_error


def test_6_cantidad_impar_de_equipos_lanza_excepcion():
    """Regla del negocio: con 5 equipos no se puede armar el fixture (cantidad impar)."""
    equipos = ["Real Norte", "Atlético Sur", "Deportivo Central", "Unión FC", "Rayo Dorado"]
    lanzo_error = False
    try:
        validaciones.validar_equipos(equipos, 4)
    except ValueError:
        lanzo_error = True
    assert lanzo_error


def test_7_cuatro_equipos_justo_el_minimo_se_aceptan():
    """Caso límite: exactamente 4 equipos, el mínimo permitido, se aceptan."""
    equipos = ["Real Norte", "Atlético Sur", "Deportivo Central", "Unión FC"]
    assert validaciones.validar_equipos(equipos, 4) == equipos

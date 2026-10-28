"""
Módulo de archivos: todo el acceso a disco pasa por acá.
Cada archivo se abre indicando el modo ("r" lectura, "w" escritura) y
la codificación utf-8, y se cierra siempre (finally), aunque haya un
error en el medio.

Si algo falla, las funciones lanzan una excepción con un mensaje claro:
- OSError: el archivo no existe o no se pudo leer/escribir.
- ValueError: el archivo existe pero su contenido no es JSON válido.
Que el contenido tenga sentido para el torneo lo revisa validaciones.py.
main.py captura esas excepciones; ningún error cierra el programa sin
explicar qué pasó.

Archivos que maneja:
- configuracion.json (lectura): la puntuación.
- usuarios.json (lectura): los usuarios y sus contraseñas.
- equipos.txt (lectura): un nombre de equipo por línea.
- fixture.txt (escritura): el fixture exportado desde el menú.
"""

import json


def leer_json(ruta):
    """
    Lee un archivo JSON y lo devuelve como estructura de Python
    (diccionario). Proceso (como en clase): abrir, leer todo con read(),
    cerrar y convertir el texto con json.loads().
    """
    contenido = ""
    try:
        arch = open(ruta, "r", encoding="utf-8")
        try:
            contenido = arch.read()
        finally:
            arch.close()
    except OSError:
        raise OSError(f"No se pudo leer {ruta}. Verificá que el archivo exista y que el programa se ejecute desde la carpeta del proyecto.")

    try:
        datos_json = json.loads(contenido)
    except ValueError:
        raise ValueError(f"{ruta} no tiene un formato JSON válido.")
    return datos_json


def leer_lineas(ruta):
    """
    Lee un archivo de texto y devuelve sus líneas, sin el salto de línea
    ni espacios en los extremos, salteando las líneas vacías. Recorre el
    archivo con for ... in (no hace falta controlar el fin de archivo a
    mano). Se usa para equipos.txt.
    """
    lineas = []
    try:
        arch = open(ruta, "r", encoding="utf-8")
        try:
            for linea in arch:
                texto = linea.strip()
                if texto != "":
                    lineas.append(texto)
        finally:
            arch.close()
    except OSError:
        raise OSError(f"No se pudo leer {ruta}. Verificá que el archivo exista y que el programa se ejecute desde la carpeta del proyecto.")
    return lineas


def escribir_lineas(ruta, lineas):
    """
    Escribe una lista de líneas en un archivo de texto (fixture.txt). Abre en modo "w":
    si el archivo existe, lo reemplaza. write() no agrega el salto de
    línea, por eso se suma "\\n" a cada una.
    """
    try:
        arch = open(ruta, "w", encoding="utf-8")
        try:
            for linea in lineas:
                arch.write(linea + "\n")
        finally:
            arch.close()
    except OSError:
        raise OSError(f"No se pudo escribir {ruta}.")


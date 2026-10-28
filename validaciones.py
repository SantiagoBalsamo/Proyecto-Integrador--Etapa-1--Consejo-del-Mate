"""
Módulo de validaciones.
Todas las validaciones siguen el mismo patrón: arman un mensaje de error
si algo falla y, al final, si hay mensaje, lanzan ValueError con ese
mensaje; si no, devuelven el dato validado. Quien llama (main.py)
captura la excepción con try/except, muestra el mensaje y sigue.

Cambio respecto de la Etapa 1: antes validar_entero devolvía una tupla
(es_valido, resultado); ahora lanza ValueError, como cualquier error de
Python, y el mensaje explica qué formato se espera.

Las expresiones regulares solo controlan la FORMA del dato. Después se
verifica que el dato tenga sentido (que el usuario exista, que la
contraseña coincida, que no haya equipos repetidos, etc.).
"""

import re


def es_entero_desde(valor, minimo):
    """Indica si un valor leído de un JSON es un entero mayor o igual a minimo."""
    return type(valor) == int and valor >= minimo


def validar_entero(texto, minimo, maximo):
    """Convierte un texto a entero y valida que esté entre minimo y maximo.
    Devuelve el entero o lanza ValueError."""
    texto = texto.strip()
    mensaje_error = ""
    valor = 0

    if texto == "":
        mensaje_error = "el valor no puede estar vacío."
    else:
        try:
            valor = int(texto)
        except ValueError:
            mensaje_error = "el valor ingresado no es un número entero válido."

    if mensaje_error == "" and valor < minimo:
        mensaje_error = f"el valor debe ser mayor o igual a {minimo}."
    elif mensaje_error == "" and valor > maximo:
        mensaje_error = f"el valor debe ser menor o igual a {maximo}."

    if mensaje_error != "":
        raise ValueError(mensaje_error)
    return valor


# ---------- Archivos de configuración ----------

def validar_configuracion(configuracion):
    """
    Valida el diccionario leído de configuracion.json y devuelve el
    diccionario de puntuación que contiene. La puntuación debe tener
    victoria, empate y derrota, enteros >= 0, con victoria > empate >
    derrota: si el empate valiera lo mismo que la derrota, un empate se
    confundiría con una derrota al detectar invictos.
    """
    mensaje_error = ""
    puntuacion = {}

    if type(configuracion) != dict or "puntuacion" not in configuracion or type(configuracion["puntuacion"]) != dict:
        mensaje_error = "configuracion.json debe tener la clave puntuacion, con victoria, empate y derrota."
    else:
        puntuacion = configuracion["puntuacion"]
        for clave in ("victoria", "empate", "derrota"):
            if mensaje_error == "" and not es_entero_desde(puntuacion.get(clave), 0):
                mensaje_error = f"En configuracion.json, puntuacion debe tener '{clave}' con un entero mayor o igual a 0."
        if mensaje_error == "" and not (puntuacion["victoria"] > puntuacion["empate"] > puntuacion["derrota"]):
            mensaje_error = "En configuracion.json, la puntuación debe cumplir victoria > empate > derrota."

    if mensaje_error != "":
        raise ValueError(mensaje_error)
    return puntuacion


def validar_usuarios(usuarios):
    """El JSON de usuarios debe ser un diccionario {usuario: contraseña} con al menos uno."""
    if type(usuarios) != dict or len(usuarios) == 0:
        raise ValueError("usuarios.json debe tener al menos un usuario con su contraseña, con el formato {\"usuario\": \"contraseña\"}.")
    return usuarios


# ---------- Login (expresiones regulares) ----------

def validar_usuario(usuario):
    """Formato de usuario: entre 4 y 15 minúsculas, números o guion bajo."""
    if re.match(r"^[a-z0-9_]{4,15}$", usuario) == None:
        raise ValueError("Usuario inválido. Formato esperado: entre 4 y 15 minúsculas, números o guion bajo.")
    return usuario


def validar_contrasena(contrasena):
    """Formato de contraseña: entre 6 y 12 letras o números."""
    if re.match(r"^[A-Za-z0-9]{6,12}$", contrasena) == None:
        raise ValueError("Contraseña inválida. Formato esperado: entre 6 y 12 letras o números.")
    return contrasena


def verificar_credenciales(usuarios, usuario, contrasena):
    """Después de validar el formato: verifica que el usuario exista en el
    diccionario (se busca la clave con in) y que la contraseña coincida."""
    return usuario in usuarios and usuarios[usuario] == contrasena


# ---------- Equipos ----------

def validar_nombre_equipo(nombre):
    """Formato de nombre de equipo: entre 3 y 30 letras (con tildes o ñ) o espacios."""
    if re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{3,30}$", nombre) == None:
        raise ValueError(f"Nombre de equipo inválido: '{nombre}'. Formato esperado: entre 3 y 30 letras o espacios.")
    return nombre


def validar_equipos(equipos, minimo_equipos):
    """
    Valida la lista leída de equipos.txt:
    - cada nombre cumple el formato (expresión regular);
    - no hay nombres repetidos: se usa un conjunto, que no admite
      duplicados; si su tamaño es distinto al de la lista, hay repetidos;
    - hay al menos minimo_equipos equipos (regla fija: 4);
    - la cantidad es par (el fixture todos contra todos necesita que
      cada fecha tenga parejas completas).
    Lanza ValueError con el primer problema encontrado.
    """
    mensaje_error = ""

    for nombre in equipos:
        if mensaje_error == "":
            try:
                validar_nombre_equipo(nombre)
            except ValueError as error:
                mensaje_error = str(error)

    if mensaje_error == "" and len(set(equipos)) != len(equipos):
        mensaje_error = "Hay nombres de equipos repetidos en equipos.txt."
    elif mensaje_error == "" and len(equipos) < minimo_equipos:
        mensaje_error = f"equipos.txt debe tener al menos {minimo_equipos} equipos y tiene {len(equipos)}."
    elif mensaje_error == "" and len(equipos) % 2 != 0:
        mensaje_error = f"La cantidad de equipos debe ser par y equipos.txt tiene {len(equipos)}."

    if mensaje_error != "":
        raise ValueError(mensaje_error)
    return equipos


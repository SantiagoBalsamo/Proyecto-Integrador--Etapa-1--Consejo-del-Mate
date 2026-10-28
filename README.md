# Torneo de eSports (FIFA) — Etapa 2

Proyecto Integrador de Programación I — 2º cuatrimestre 2026
Cátedra: Ing. María Eugenia Varando
Equipo: Consejo del Mate F.C.

## Integrantes

- (Completar con los nombres del equipo)

## Qué es

Es un sistema por consola para administrar un torneo de FIFA todos contra todos, a una rueda.

En la Etapa 2, el prototipo de la Etapa 1 suma:
- ingreso con usuario y contraseña,
- la puntuación leída de `configuracion.json`,
- los equipos leídos de `equipos.txt`,
- la exportación del fixture a `fixture.txt`.

Los resultados se cargan durante la ejecución y no se guardan entre ejecuciones.

## Cómo ejecutar

Requiere Python 3. El programa busca sus archivos en la carpeta desde donde se ejecuta, así que hay que pararse en la carpeta del proyecto:

```
cd proyecto_etapa2
python main.py
```

Usuarios de prueba (están en `usuarios.json`):

| Usuario | Contraseña |
| --- | --- |
| admin | Admin2026 |
| organizador | Torneo123 |
| invitado | Mate2026 |

## Estructura

```
proyecto_etapa2/
├── main.py              menú, login e interacción con el usuario
├── datos.py             reglas fijas, fixture y matrices
├── operaciones.py       cálculos, tabla, reportes y goles por fecha
├── validaciones.py      expresiones regulares y validaciones (lanzan ValueError)
├── archivos.py          lectura de .json y .txt, escritura de .txt
├── configuracion.json   solo la puntuación
├── usuarios.json        los tres usuarios con su contraseña
├── equipos.txt          un nombre de equipo por línea
├── fixture.txt          se genera desde la opción 9 del menú
├── pytest.ini           le indica a pytest dónde están los módulos y las pruebas
├── tests/
│   ├── test_validaciones.py   pruebas 1, 2, 6 y 7
│   └── test_operaciones.py    pruebas 3, 4 y 5
└── README.md
```

## Inicio del programa

1. Lee `configuracion.json` y valida la puntuación: tiene que tener las claves `victoria`, `empate` y `derrota`, con enteros que cumplan victoria > empate > derrota.
2. Lee `usuarios.json` a un diccionario `{usuario: contraseña}`.
3. Pide usuario y contraseña, con hasta 3 intentos. Primero controla el formato con expresiones regulares y después compara con el diccionario.
4. Lee `equipos.txt` y valida que:
   - cada nombre tenga un formato válido,
   - no haya nombres repetidos,
   - haya al menos 4 equipos,
   - la cantidad sea par.
5. Genera el fixture, crea las tres matrices según la cantidad de equipos y muestra el menú.

## Menú

1. Información general del torneo. La puntuación se recorre con `items()`.
2. Cargar resultado. Se ingresan solo los goles, y los puntos se calculan con la puntuación del diccionario.
3. Tabla de posiciones.
4. Resultados de una fecha. Los partidos jugados muestran el resultado y los pendientes, "vs".
5. Buscar equipo.
6. Indicadores.
7. Condiciones destacables: invictos y estado crítico.
8. Resumen general, con los goles por fecha y la fecha con más goles.
9. Exportar el fixture a `fixture.txt`. Los partidos jugados muestran el resultado y los pendientes, "vs".
0. Salir.

## Reglas del dominio

- **Puntos:** victoria, empate y derrota, según `configuracion.json` (3/1/0).
- **Desempate:** primero los puntos, después la diferencia de gol y después los goles a favor.
- **Estado crítico:** un equipo que jugó al menos 3 partidos y tiene 0 puntos.
- **Invicto:** un equipo que jugó al menos un partido y nunca perdió.
- **Cantidad de equipos:** par y como mínimo 4. Con 4 equipos, cada uno juega 3 partidos, lo justo para que pueda darse el estado crítico.
- **Goles por partido:** de 0 a 20.

El máximo de goles (20), el límite de estado crítico (3) y el mínimo de equipos (4) son reglas fijas del sistema. Están en funciones de `datos.py` y no en la configuración externa.

## Cambios respecto de la Etapa 1

| Cambio | Limitación de la Etapa 1 | Cómo se resuelve |
| --- | --- | --- |
| Login de ingreso | Cualquiera podía usar el sistema | Tres usuarios en `usuarios.json`; el formato se controla con expresiones regulares |
| Puntuación externa | La puntuación estaba escrita en el código | `configuracion.json`, leído a un diccionario y validado al iniciar |
| Equipos desde archivo | Los nombres estaban escritos en el código | Se leen de `equipos.txt`; cantidad par y mínimo de 4 |
| Exportar el fixture | El fixture solo se veía en pantalla | La opción 9 genera `fixture.txt` |
| Puntuación como diccionario | Las reglas eran una tupla de textos y cada función recibía tres parámetros sueltos | `puntuacion` es un diccionario que se consulta por clave |
| Goles por fecha | No se podía ver qué fecha tuvo más goles | Diccionario `{numero_de_fecha: goles_totales}` en el resumen general |
| Validaciones con excepciones | `validar_entero` devolvía una tupla `(es_valido, resultado)` | Las validaciones lanzan `ValueError` con un mensaje que explica el formato esperado |
| Módulos nuevos | Las validaciones y el manejo de archivos estaban mezclados con la lógica | `validaciones.py` y `archivos.py` separan esas responsabilidades |
| Pruebas unitarias | No había pruebas automáticas | 7 pruebas con pytest en `tests/` |

Se mantiene de la Etapa 1:
- el fixture con el método del círculo,
- las tres matrices homogéneas con `SIN_RESULTADO = -1`,
- la tabla de posiciones con `lambda`,
- el Top 3 con slicing,
- las reglas de código: sin variables globales, un solo `return` por función, sin `break` ni `continue`.

## Diccionarios, conjuntos y expresiones regulares

| Estructura | Dónde | Para qué |
| --- | --- | --- |
| Diccionario de configuración | `configuracion.json` | Contiene solo la puntuación |
| Diccionario de puntuación | Dentro de la configuración | Se consulta con `puntuacion["victoria"]` al calcular los puntos |
| Diccionario de usuarios | `usuarios.json` | Login: se busca la clave con `in` y se compara la contraseña |
| Diccionario de goles por fecha | Resumen general | Se recorre con `items()`; `max()` sobre los valores da la fecha con más goles |
| Conjunto | Validación de `equipos.txt` | Si `len(set(equipos))` es distinto de `len(equipos)`, hay nombres repetidos |

| Dato | Patrón | Formato esperado |
| --- | --- | --- |
| Usuario | `^[a-z0-9_]{4,15}$` | Entre 4 y 15 minúsculas, números o guion bajo |
| Contraseña | `^[A-Za-z0-9]{6,12}$` | Entre 6 y 12 letras o números |
| Nombre de equipo | `^[A-Za-zÁÉÍÓÚáéíóúÑñ ]{3,30}$` | Entre 3 y 30 letras o espacios |

## Excepciones

**Errores no críticos (el programa informa y sigue):**
- Datos ingresados en el menú: una opción inexistente, texto en vez de número, goles negativos o mayores a 20, o un partido ya cargado. Se informa el error y se vuelve a pedir el dato.
- Un intento de login fallido cuando todavía quedan intentos.
- Un error de escritura (`OSError`) al exportar `fixture.txt`. Se informa y el menú sigue.

**Errores críticos (impiden iniciar el sistema):**
- `configuracion.json`, `usuarios.json` o `equipos.txt` no existen o no se pueden leer.
- Un archivo obligatorio con contenido inválido:
  - JSON mal formado,
  - puntuación incompleta o que no cumple victoria > empate > derrota,
  - un nombre de equipo inválido,
  - nombres de equipo repetidos,
  - menos de 4 equipos,
  - una cantidad impar de equipos.
- Se agotan los 3 intentos de login.

En estos casos el programa muestra un mensaje claro y termina sin entrar al menú.

## Pruebas unitarias

Requiere pytest (`pip install pytest`). Desde la carpeta del proyecto:

```
pytest
```

Resultado esperado: `7 passed`. El archivo `pytest.ini` le indica a pytest que los módulos están en esta carpeta y las pruebas en `tests/`.

| N° | Prueba | Tipo |
| --- | --- | --- |
| 1 | `validar_usuario("admin")` devuelve `"admin"` | Validación correcta |
| 2 | `validar_contrasena("ab")` lanza `ValueError` | Validación incorrecta |
| 3 | `calcular_puntos(2, 1, puntuacion)` devuelve `(3, 0)` | Cálculo simple |
| 4 | `goles_por_fecha` suma cada columna y saltea los -1 | Acumulación por clave |
| 5 | Un equipo con 3 derrotas está en estado crítico y uno con 2 no | Condición crítica |
| 6 | 5 equipos lanza `ValueError` (cantidad impar) | Regla del negocio |
| 7 | Exactamente 4 equipos se aceptan | Caso límite |

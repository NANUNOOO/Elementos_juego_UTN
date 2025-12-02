from constantes import *
# en constantes creamos un mapa de los bloques para definir los niveles.

CONFIGURACION_NIVELES = [
    {
        # Nivel 1: Cuadrado simple de colores
        "mapa": [
            ["rojo", "verde", "azul", "gris", "rojo", "verde", "azul"],
            ["gris", "azul", "rojo", "azul", "gris", "verde", "rojo"],
            ["verde", "azul", "gris", "rojo", "rojo", "gris", "verde"],
            ["rojo", "verde", "verde", "azul", "gris", "verde", "azul"],
            ["gris", "azul", "rojo", "gris", "azul", "verde", "rojo"],
            ["verde", "rojo", "gris", "azul", "azul", "gris", "verde"]
        ],
        "velocidad_base": VELOCIDAD_PELOTA_BASE,
    },
    {
        # Nivel 2: Diseño en forma de V
        "mapa": [
            ["azul", "rojo", "gris", "verde", "gris", "rojo", "verde", "azul"],
            ["verde", "azul", "rojo", "gris", "verde", "azul", "rojo", "gris"],
            ["vacio", "gris", "verde", "rojo", "azul", "verde", "gris", "vacio"],
            ["vacio", "verde", "azul", "azul", "rojo", "gris", "verde", "vacio"],
            ["vacio", "vacio", "gris", "rojo", "azul", "verde", "vacio", "vacio"],
            ["vacio", "vacio", "verde", "azul", "rojo", "gris", "vacio", "vacio"],
            ["vacio", "vacio", "vacio", "gris", "verde", "vacio", "vacio", "vacio"],
            ["vacio", "vacio", "vacio", "rojo", "azul", "vacio", "vacio", "vacio"]
        ], "velocidad_base": VELOCIDAD_PELOTA_BASE * 1.2,
    },
    {
        # Nivel 3: Cuadro con vacio
        "mapa": [
            ["azul", "rojo", "gris", "verde", "gris", "rojo", "verde", "azul"],
            ["verde", "azul", "rojo", "gris", "verde", "azul", "rojo", "gris"],
            ["rojo", "vacio", "vacio", "rojo", "azul", "verde", "gris", "verde"],
            ["gris", "vacio", "vacio", "azul", "rojo", "gris", "verde", "rojo"],
            ["verde", "rojo", "gris", "rojo", "azul", "vacio", "vacio", "azul"],
            ["azul", "gris", "verde", "azul", "rojo", "vacio", "vacio", "verde"],
            ["verde", "rojo", "azul", "gris", "verde", "azul", "verde", "gris"],
            ["azul", "gris", "verde", "rojo", "azul", "gris", "rojo", "verde"]
        ], "velocidad_base": VELOCIDAD_PELOTA_BASE * 1.4,
    },
]

LISTA_TIPOS_BLOQUES = ["rojo", "verde", "azul", "gris", "vacio"]

nivel_actual_indice = 0

# Valores de Bloques
VALORES_PUNTOS_BLOQUES = {"rojo": 100, "verde": 80, "azul": 60, "gris": 40}
LISTA_TIPOS_BLOQUES = ["rojo", "verde", "azul", "gris"]
LISTA_TIPOS_POWER_UP = ["hoja", "fuego", "viento", "gota"]
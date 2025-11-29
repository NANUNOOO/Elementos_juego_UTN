import pygame
import random

from settings import *

def crear_bloques():
    """
    Genera la matriz de bloques del nivel y devuelve una lista con todos ellos.

    Esta función crea una cuadrícula de bloques usando filas y columnas.
    Cada bloque se representa como un diccionario con:
        - "rect" : pygame.Rect con la posición y tamaño del bloque
        - "color": color asignado aleatoriamente desde colores_posibles

    Los bloques se distribuyen dejando un espacio uniforme entre ellos,
    y desplazados desde la izquierda y arriba para que no queden pegados
    a los bordes de la ventana.

    La función se ejecuta una vez al iniciar el juego y los bloques son
    utilizados posteriormente por colision_pelota_bloques() para detección
    de impacto y eliminación.

    Returns
    -------
    list[dict]
        Lista de bloques, cada uno con:
            - "rect": pygame.Rect
            - "color": tuple (R, G, B)
    """
    # Configuración de la grilla de bloques
    filas = 8
    columnas = 8
    ancho_bloque = 60
    alto_bloque = 20
    espacio = 10  # separación entre bloques

    bloques = []

    for fila in range(filas):
        for columnas in range(columnas + 1):
            x = columnas * (ancho_bloque + espacio) + 90
            y = fila * (alto_bloque + espacio) + 30
            bloque = pygame.Rect(x, y, ancho_bloque, alto_bloque)
            color = random.choice(colores_posibles)# Se carga un color aleatorio
            bloques.append({"rect":bloque, "color":color})
    return bloques
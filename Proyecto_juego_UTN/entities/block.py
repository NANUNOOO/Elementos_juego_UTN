import pygame
import random

from settings import *

def create_blocks():
    # bloques
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
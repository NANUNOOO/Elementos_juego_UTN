import pygame
import random

from settings import *
from utils import state

def iniciar_nueva_partida():

    # === VARIABLES SIMPLES ===
    state.vidas_jugador = 3
    state.puntuacion_actual = 0
    state.nombre_usuario_entrada = ""
    state.juego_esta_activo = False

    # === LISTAS ===
    state.lista_efectos_activos = []
    state.lista_power_ups_cayendo = []
    state.lista_bloques.clear()

    # === PALETA ===
    state.imagen_paleta_actual = pygame.transform.scale(
        state.imagen_paleta_base.copy(),
        (ANCHO_PALETA_ORIGINAL, 30)
    )

    state.rectangulo_paleta = state.imagen_paleta_actual.get_rect()
    state.rectangulo_paleta.centerx = ANCHO // 2
    state.rectangulo_paleta.y = ALTO - 80

    # === PELOTA ===
    state.posicion_pelota_x = ANCHO // 2
    state.posicion_pelota_y = ALTO - 170
    state.velocidad_pelota_x = VELOCIDAD_PELOTA_BASE
    state.velocidad_pelota_y = -VELOCIDAD_PELOTA_BASE

    # === BLOQUES ===
    cantidad_filas = random.choice([7, 8])
    cantidad_columnas = cantidad_filas
    ancho_bloque_individual = 65
    alto_bloque_individual = 23
    espacio_entre_bloques = 10 

    for fila in range(cantidad_filas):
        for col in range(cantidad_columnas):
            ancho_total = cantidad_columnas * ancho_bloque_individual + (cantidad_columnas - 1) * espacio_entre_bloques
            margen_x = (ANCHO - ancho_total) // 2
            
            pos_x = col * (ancho_bloque_individual + espacio_entre_bloques) + margen_x
            pos_y = fila * (alto_bloque_individual + espacio_entre_bloques) + 30 
            
            rect = pygame.Rect(pos_x, pos_y, ancho_bloque_individual, alto_bloque_individual)
            tipo = random.choice(LISTA_TIPOS_BLOQUES)

            state.lista_bloques.append({
                "rectangulo": rect, 
                "tipo": tipo, 
                "imagen": state.diccionario_imagenes_bloques[tipo]
            })
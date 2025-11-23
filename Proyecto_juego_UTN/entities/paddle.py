import pygame

from settings import *

def create_paddle():

    paleta = pygame.image.load ("Proyecto_juego_UTN/assets/images/barraroja2.png")
    paleta = pygame.transform.scale(paleta, (170, 30))

    paleta_rect = paleta.get_rect()
    paleta_rect.x = ANCHO // 2 - paleta_rect.width // 2
    paleta_rect.y = ALTO - 80
    
    velocidad_paleta = 15

    return paleta, paleta_rect, velocidad_paleta
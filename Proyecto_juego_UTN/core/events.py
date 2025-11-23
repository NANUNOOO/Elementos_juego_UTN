import pygame

from settings import *
from entities.paddle import *

def pallet_movement(paleta_rect, velocidad_paleta):

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LEFT] and paleta_rect.x> 0:
        paleta_rect.x -= velocidad_paleta

    if keys[pygame.K_RIGHT] and paleta_rect.x + paleta_rect.width < ANCHO:
        paleta_rect.x += velocidad_paleta

    return velocidad_paleta
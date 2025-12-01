import pygame

from settings import *
from utils import resources

def dibujar_texto_centrado(superficie_destino, texto_a_mostrar, fuente_texto, color_texto, posicion_y):
    superficie_texto = fuente_texto.render(texto_a_mostrar, True, color_texto)
    rectangulo_texto = superficie_texto.get_rect(center=(ANCHO // 2, posicion_y))
    superficie_destino.blit(superficie_texto, rectangulo_texto)

def dibujar_boton_interactivo(superficie_destino, rectangulo_boton, texto_boton):
    posicion_mouse = pygame.mouse.get_pos()
    
    if rectangulo_boton.collidepoint(posicion_mouse):
        color_actual_boton = COLOR_AZUL_HOVER
    else:
        color_actual_boton = COLOR_AZUL_BOTON
    
    pygame.draw.rect(superficie_destino, color_actual_boton, rectangulo_boton, border_radius=12)
    pygame.draw.rect(superficie_destino, COLOR_GRIS_CLARO, rectangulo_boton, 2, border_radius=12)
    
    superficie_texto = resources.fuente_botones.render(texto_boton, True, COLOR_BLANCO)
    rectangulo_texto = superficie_texto.get_rect(center=rectangulo_boton.center)
    superficie_destino.blit(superficie_texto, rectangulo_texto)
    
    if rectangulo_boton.collidepoint(posicion_mouse) and pygame.mouse.get_pressed()[0]:
        return True
    return False
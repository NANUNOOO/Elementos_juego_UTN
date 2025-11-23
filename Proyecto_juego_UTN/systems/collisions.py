import pygame
from settings import *

def obtener_coordenadas_pelota(pelota):
    pelota_top_cords = (pelota.centerx, pelota.centery - (pelota.height / 2))
    pelota_bottom_cords = (pelota.centerx, pelota.centery + (pelota.height / 2))
    pelota_left_cords = (pelota.centerx - (pelota.width / 2), pelota.centery)
    pelota_right_cords = (pelota.centerx + (pelota.width / 2), pelota.centery)

    return pelota_top_cords, pelota_bottom_cords, pelota_left_cords, pelota_right_cords

def colision_pelota_bloques(bloques, ventana, pelota_top_cords, pelota_bottom_cords, pelota_left_cords, pelota_right_cords, velocidad_pelota_x, velocidad_pelota_y):
    bloques_a_borrar = []

    for bloque in bloques:
        bloque_rect = pygame.draw.rect(ventana, bloque["color"], bloque["rect"], border_radius=5)
        if bloque_rect.collidepoint(pelota_top_cords):
            velocidad_pelota_y *= -1
            bloques_a_borrar.append(bloque)
        elif bloque_rect.collidepoint(pelota_bottom_cords):
            velocidad_pelota_y *= -1
            bloques_a_borrar.append(bloque)
        elif bloque_rect.collidepoint(pelota_left_cords):
            velocidad_pelota_x *= -1
            bloques_a_borrar.append(bloque)
        elif bloque_rect.collidepoint(pelota_right_cords):
            velocidad_pelota_x *= -1
            bloques_a_borrar.append(bloque)
    for bloque_rect in bloques_a_borrar:
        bloques.remove(bloque_rect)

    return velocidad_pelota_x, velocidad_pelota_y

def colision_pelota_paredes_y_paleta(posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y, paleta_rect, pelota_bottom_cords):
    # Rebote contra las paredes
    if posicion_pelota_x - radio_pelota <= 0 or posicion_pelota_x + radio_pelota >= ANCHO:
        velocidad_pelota_x *= -1
    if posicion_pelota_y - radio_pelota <= 0:
        velocidad_pelota_y *= -1
    # Rebote en la paleta
    if paleta_rect.collidepoint(pelota_bottom_cords):
        velocidad_pelota_y *= -1

    return velocidad_pelota_x, velocidad_pelota_y
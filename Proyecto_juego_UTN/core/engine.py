import pygame

from settings import *
from entities import paddle
from core.events import pallet_movement
from entities.block import create_blocks
from entities.ball import create_ball
from systems.movement import move_ball
from systems.collisions import *

def elementos_juego():
    pygame.init ()
    
    ICONO = pygame.image.load("Proyecto_juego_UTN/assets/images/arkanoide.png")
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    clock = pygame.time.Clock()
    corriendo = True

    pygame.display.set_icon(ICONO)
    background_image = pygame.image.load("Proyecto_juego_UTN/assets/images/fondoazul.jpg")
    paleta, paleta_rect, velocidad_paleta = paddle.create_paddle()
    bloques = create_blocks()
    posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y = create_ball()

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        pallet_movement(paleta_rect, velocidad_paleta)

        ventana.blit(background_image, (0,0))
        ventana.blit(paleta, paleta_rect)

        posicion_pelota_x, posicion_pelota_y = move_ball(posicion_pelota_x,posicion_pelota_y,velocidad_pelota_x,velocidad_pelota_y)
        pelota = pygame.draw.circle(ventana, (255, 255, 255), (posicion_pelota_x, posicion_pelota_y), radio_pelota)

        pelota_top_cords, pelota_bottom_cords, pelota_left_cords, pelota_right_cords = obtener_coordenadas_pelota(pelota)
        velocidad_pelota_x, velocidad_pelota_y = colision_pelota_bloques(bloques,ventana,pelota_top_cords,pelota_bottom_cords,pelota_left_cords,pelota_right_cords,velocidad_pelota_x,velocidad_pelota_y)
        velocidad_pelota_x, velocidad_pelota_y = colision_pelota_paredes_y_paleta(posicion_pelota_x,posicion_pelota_y,radio_pelota,velocidad_pelota_x,velocidad_pelota_y,paleta_rect,pelota_bottom_cords)
        
        for bloque in bloques:
            bloque_rect = pygame.draw.rect(ventana, bloque["color"], bloque["rect"], border_radius=5)
        pygame.display.flip()
        clock.tick(50)

    pygame.quit()
import pygame

from settings import *
from entities import paddle
from core.events import controles_paleta
from entities.block import crear_bloques
from entities.ball import crear_bola
from systems.movement import mover_pelota
from systems.collisions import *

def elementos_juego():
    pygame.init () # Inicializa todos los módulos de Pygame
    
    ICONO = pygame.image.load("Proyecto_juego_UTN/assets/images/arkanoide.png") # Carga el ícono de la ventana
    ventana = pygame.display.set_mode((ANCHO, ALTO)) # Crea la ventana principal del juego
    clock = pygame.time.Clock() # Reloj para controlar los FPS
    corriendo = True # Variable para mantener el juego en ejecución

    pygame.display.set_icon(ICONO) # Configura el ícono de la ventana
    background_image = pygame.image.load("Proyecto_juego_UTN/assets/images/fondoazul.jpg") # Carga la imagen de fondo
    paleta, paleta_rect, velocidad_paleta = paddle.crear_paleta() # Crea la paleta del jugador
    bloques = crear_bloques() # Crea los bloques del nivel
    posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y = crear_bola() # Crea la pelota: posición, radio y velocidades iniciales


    while corriendo: # Bucle principal del juego
        for evento in pygame.event.get(): # Manejo de eventos
            if evento.type == pygame.QUIT: # El jugador cerró la ventana
                corriendo = False
        controles_paleta(paleta_rect, velocidad_paleta) # Control de movimiento de la paleta (izquierda/derecha)

        ventana.blit(background_image, (0,0))  # Dibuja el fondo
        ventana.blit(paleta, paleta_rect) # Dibuja la paleta en su posición

        posicion_pelota_x, posicion_pelota_y = mover_pelota(posicion_pelota_x,posicion_pelota_y,velocidad_pelota_x,velocidad_pelota_y) # Actualiza la posición de la pelota según su velocidad
        pelota = pygame.draw.circle(ventana, (255, 255, 255), (posicion_pelota_x, posicion_pelota_y), radio_pelota)  # Dibuja la pelota en pantalla

        pelota_top_cords, pelota_bottom_cords, pelota_left_cords, pelota_right_cords = obtener_coordenadas_pelota(pelota)  # Obtiene las coordenadas de cada lado de la pelota (para colisiones)
        velocidad_pelota_x, velocidad_pelota_y = colision_pelota_bloques(bloques,ventana,pelota_top_cords,pelota_bottom_cords,pelota_left_cords,pelota_right_cords,velocidad_pelota_x,velocidad_pelota_y) # Detecta colisión entre pelota y bloques, y cambia la velocidad si es necesario
        velocidad_pelota_x, velocidad_pelota_y = colision_pelota_paredes_y_paleta(posicion_pelota_x,posicion_pelota_y,radio_pelota,velocidad_pelota_x,velocidad_pelota_y,paleta_rect,pelota_bottom_cords) # Detecta colisión con paredes y paleta
        
        for bloque in bloques: # Dibuja todos los bloques restantes
            bloque_rect = pygame.draw.rect(ventana, bloque["color"], bloque["rect"], border_radius=5)
        pygame.display.flip() # Actualiza la pantalla completa
        clock.tick(50) # Limita el juego a 50 FPS

    pygame.quit() # Sale correctamente de Pygame cuando termina el juego
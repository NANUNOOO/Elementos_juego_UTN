import pygame
import sys

from settings import *
from entities import paddle
from core.events import controles_paleta
from entities.block import crear_bloques
from entities.ball import crear_bola
from systems.movement import mover_pelota
from systems.collisions import *

from utils import resources
from events import *
from utils import state
def elementos_juego():
    pygame.init ()
    
    # Configuración de ventana
    ventana_principal = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(NOMBRE_DEL_JUEGO)
    reloj_control = pygame.time.Clock()

    # Cargar imágenes y fuentes (desde funciones.py)
    resources.inicializar_recursos()

    # --- VARIABLES LOCALES DEL BUCLE PRINCIPAL ---
    ESTADO_ACTUAL = "MENU"
    se_hizo_clic_previamente = False
    juego_corriendo = True

    # --- DEFINICIÓN DE BOTONES (Posición y Tamaño) ---
    coord_centro_x = ANCHO // 2

    rect_jugar = pygame.Rect(0, 0, 250, 50)
    rect_jugar.center = (coord_centro_x, 200)

    rect_ranking = pygame.Rect(0, 0, 250, 50)
    rect_ranking.center = (coord_centro_x, 270)

    rect_creditos = pygame.Rect(0, 0, 250, 50)
    rect_creditos.center = (coord_centro_x, 340)

    rect_salir = pygame.Rect(0, 0, 250, 50)
    rect_salir.center = (coord_centro_x, 410)

    rect_volver = pygame.Rect(20, ALTO - 70, 150, 50)

    while juego_corriendo: # Bucle principal del juego
        # 1. Control de Tiempo
        tiempo_actual = pygame.time.get_ticks()
        reloj_control.tick(CUADROS_POR_SEGUNDO)

        mouse_esta_presionado = pygame.mouse.get_pressed()[0]

        juego_corriendo, ESTADO_ACTUAL = procesar_eventos(ESTADO_ACTUAL) # Manejo de eventos
        # Dibujar fondo (común a todas las pantallas)
        ventana_principal.blit(state.IMAGEN_FONDO, (0, 0))













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
        pygame.display.flip() 
        clock.tick(50) 

    pygame.quit()
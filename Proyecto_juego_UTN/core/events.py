import pygame

from settings import *
from entities.paddle import *

def controles_paleta(paleta_rect, velocidad_paleta):
    """
    Controla el movimiento horizontal de la paleta según las teclas presionadas.

    Esta función:
        - Detecta si el jugador está presionando las teclas LEFT o RIGHT.
        - Mueve la paleta dentro de los límites de la pantalla.
        - Ajusta la posición directamente modificando paleta_rect.x.
        - No devuelve el rect (porque se modifica por referencia), pero retorna 
        la velocidad por consistencia con el resto del código.

    Se llama una vez por frame dentro del loop principal del juego para permitir
    el movimiento fluido de la paleta.

    Parámetros
    ----------
    paleta_rect : pygame.Rect
        Rectángulo que representa la paleta y contiene su posición en pantalla.
    velocidad_paleta : int
        Cantidad de píxeles que la paleta debe moverse por frame.

    Returns
    -------
    int
        velocidad_paleta (sin modificar). Se devuelve por consistencia,
        aunque su valor no cambia dentro de esta función.
    """
    keys = pygame.key.get_pressed()
        
    # Movimiento hacia la izquierda
    if keys[pygame.K_LEFT] and paleta_rect.x> 0:
        paleta_rect.x -= velocidad_paleta
    # Movimiento hacia la derecha
    if keys[pygame.K_RIGHT] and paleta_rect.x + paleta_rect.width < ANCHO:
        paleta_rect.x += velocidad_paleta

    return velocidad_paleta
import pygame

from settings import *

def crear_paleta():
    """
    Crea la paleta del jugador, asigna su posición inicial y define su velocidad.

    Esta función:
        - Carga la imagen de la paleta desde los assets.
        - Escala la imagen al tamaño deseado.
        - Obtiene el rectángulo (paleta_rect) que permite manejar posición y colisiones.
        - Ubica la paleta centrada horizontalmente y cerca del borde inferior.
        - Define la velocidad de movimiento lateral.

    Se utiliza una sola vez al iniciar el juego dentro de elementos_juego().

    Returns
    -------
    tuple
        (paleta, paleta_rect, velocidad_paleta)
        paleta : pygame.Surface
            Imagen ya cargada y escalada.
        paleta_rect : pygame.Rect
            Rect con posición inicial de la paleta en pantalla.
        velocidad_paleta : int
            Cantidad de píxeles que la paleta se mueve por frame.
    """
    paleta = pygame.image.load ("Proyecto_juego_UTN/assets/images/barraroja2.png")
    paleta = pygame.transform.scale(paleta, (170, 30))

    paleta_rect = paleta.get_rect()
    paleta_rect.x = ANCHO // 2 - paleta_rect.width // 2
    paleta_rect.y = ALTO - 80
    
    velocidad_paleta = 15

    return paleta, paleta_rect, velocidad_paleta
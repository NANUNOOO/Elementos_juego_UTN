import pygame
from settings import *

def obtener_coordenadas_pelota(pelota):
    """
    Calcula puntos estratégicos alrededor de la pelota para detectar colisiones
    de forma más precisa.

    Esta función se llama una vez por frame dentro del loop principal luego de
    dibujar la pelota, y permite que otras funciones de colisión trabajen con 
    coordenadas exactas en vez de usar el rectángulo completo.

    Se calculan cuatro puntos:
        - Superior: para detectar choques con bloques o el techo.
        - Inferior: para detectar colisiones con la paleta o bloques.
        - Izquierdo y derecho: para detectar rebotes laterales contra bloques.

    Parámetros
    ----------
    pelota : pygame.Rect
        El rectángulo devuelto por pygame.draw.circle que representa el área
        ocupada por la pelota en ese frame.

    Returns
    -------
    tuple of tuples
        (top, bottom, left, right) => cada uno es una coordenada (x, y)
    """
    pelota_top_cords = (pelota.centerx, pelota.centery - (pelota.height / 2))
    pelota_bottom_cords = (pelota.centerx, pelota.centery + (pelota.height / 2))
    pelota_left_cords = (pelota.centerx - (pelota.width / 2), pelota.centery)
    pelota_right_cords = (pelota.centerx + (pelota.width / 2), pelota.centery)

    return pelota_top_cords, pelota_bottom_cords, pelota_left_cords, pelota_right_cords

def colision_pelota_bloques(bloques, ventana, pelota_top_cords, pelota_bottom_cords, pelota_left_cords, pelota_right_cords, velocidad_pelota_x, velocidad_pelota_y):
    """
    Detecta colisiones entre la pelota y los bloques del nivel y elimina los 
    bloques que son golpeados.

    Esta función se llama en cada frame con las coordenadas críticas de la pelota,
    lo que permite determinar desde qué lado golpea un bloque. Cuando ocurre una 
    colisión:
        - Se invierte la velocidad correspondiente (X o Y)
        - Se elimina el bloque impactado

    Importante:
    La función también dibuja los bloques en pantalla porque utiliza pygame.draw.rect
    para obtener un rect actualizado. Esto garantiza que la detección de colisiones
    sea exacta respecto a lo que realmente se ve en la pantalla.

    Parámetros
    ----------
    bloques : list[dict]
        Lista de bloques, cada uno con:
            - "rect": pygame.Rect
            - "color": tuple (R,G,B)
    ventana : pygame.Surface
        Superficie donde se dibujan los bloques.
    pelota_*_cords : tuple
        Coordenadas del top, bottom, left y right de la pelota.
    velocidad_pelota_x : int or float
        Velocidad horizontal actual.
    velocidad_pelota_y : int or float
        Velocidad vertical actual.

    Returns
    -------
    tuple
        Velocidades actualizadas (velocidad_pelota_x, velocidad_pelota_y)
    """
    bloques_a_borrar = []

    for bloque in bloques:
        bloque_rect = pygame.draw.rect(ventana, bloque["color"], bloque["rect"], border_radius=5)
        # Colisiones por arriba
        if bloque_rect.collidepoint(pelota_top_cords):
            velocidad_pelota_y *= -1
            bloques_a_borrar.append(bloque)
        # Colisiones por abajo
        elif bloque_rect.collidepoint(pelota_bottom_cords):
            velocidad_pelota_y *= -1
            bloques_a_borrar.append(bloque)
        # Colisiones por izquierda
        elif bloque_rect.collidepoint(pelota_left_cords):
            velocidad_pelota_x *= -1
            bloques_a_borrar.append(bloque)
        #Colisiones por derecha
        elif bloque_rect.collidepoint(pelota_right_cords):
            velocidad_pelota_x *= -1
            bloques_a_borrar.append(bloque)
    # Borrar bloques destruidos
    for bloque_rect in bloques_a_borrar:
        bloques.remove(bloque_rect)

    return velocidad_pelota_x, velocidad_pelota_y

def colision_pelota_paredes_y_paleta(posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y, paleta_rect, pelota_bottom_cords):
    """
    Maneja las colisiones de la pelota con:
        - Paredes laterales (rebote horizontal)
        - Techo (rebote vertical)
        - Paleta del jugador (rebote vertical)

    Esta función se llama después de mover la pelota en cada frame. Ajusta las 
    velocidades según las colisiones detectadas.

    Parámetros
    ----------
    posicion_pelota_x : int or float
        X actual del centro de la pelota.
    posicion_pelota_y : int or float
        Y actual del centro de la pelota.
    radio_pelota : int
        Tamaño de la pelota.
    velocidad_pelota_x : int or float
        Velocidad horizontal actual.
    velocidad_pelota_y : int or float
        Velocidad vertical actual.
    paleta_rect : pygame.Rect
        Rectángulo de la paleta.
    pelota_bottom_cords : tuple
        Coordenada inferior de la pelota, usada para detectar colisión con la paleta.

    Returns
    -------
    tuple
        Velocidades ajustadas (velocidad_pelota_x, velocidad_pelota_y)
    """
    # Rebote contra paredes laterales
    if posicion_pelota_x - radio_pelota <= 0 or posicion_pelota_x + radio_pelota >= ANCHO:
        velocidad_pelota_x *= -1
    # Rebote contra el techo
    if posicion_pelota_y - radio_pelota <= 0:
        velocidad_pelota_y *= -1
    # Rebote contra la paleta
    if paleta_rect.collidepoint(pelota_bottom_cords):
        velocidad_pelota_y *= -1

    return velocidad_pelota_x, velocidad_pelota_y
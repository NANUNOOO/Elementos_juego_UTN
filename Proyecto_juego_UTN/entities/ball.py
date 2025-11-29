

from settings import *

def crear_bola():
    """
    Inicializa la pelota del juego, estableciendo su posición, tamaño y velocidad.

    Esta función define los valores iniciales de la pelota:
        - Posición centrada horizontalmente.
        - Ubicada por encima de la paleta (a 170 px del borde inferior).
        - Radio fijo (tamaño de la pelota).
        - Velocidades iniciales en X y Y para comenzar el movimiento.

    Se llama una única vez al iniciar la partida dentro del loop principal, 
    y su información luego se usa en:
        - move_ball() para mover la pelota.
        - colision_pelota_bloques() y colision_pelota_paredes_y_paleta() 
        para manejar colisiones.

    Returns
    -------
    tuple
        (posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y)
    """
    posicion_pelota_x = ANCHO // 2  # Centrada horizontalmente
    posicion_pelota_y = ALTO - 170  # Ubicada por encima de la paleta
    radio_pelota = 12               # Tamaño de la pelota
    velocidad_pelota_x = 4          # Velocidad horizontal inicial
    velocidad_pelota_y = -4         # Velocidad vertical inicial 
    
    return posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y
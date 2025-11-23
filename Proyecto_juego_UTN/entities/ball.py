

from settings import *

def create_ball():
    posicion_pelota_x = ANCHO // 2
    posicion_pelota_y = ALTO - 170
    radio_pelota = 12
    velocidad_pelota_x = 4
    velocidad_pelota_y = -4
    
    return posicion_pelota_x, posicion_pelota_y, radio_pelota, velocidad_pelota_x, velocidad_pelota_y
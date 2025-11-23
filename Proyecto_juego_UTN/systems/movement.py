def move_ball(posicion_pelota_x, posicion_pelota_y, velocidad_pelota_x, velocidad_pelota_y):
    
    posicion_pelota_x += velocidad_pelota_x
    posicion_pelota_y += velocidad_pelota_y

    return posicion_pelota_x, posicion_pelota_y
def mover_pelota(posicion_pelota_x, posicion_pelota_y, velocidad_pelota_x, velocidad_pelota_y):
    """
    Actualiza la posición de la pelota en función de su velocidad actual.

    Esta función se ejecuta en cada frame dentro del loop principal del juego.
    Su único propósito es mover la pelota sumando la velocidad a su posición.
    El cálculo de rebotes y colisiones NO se hace aquí, sino en las funciones
    correspondientes (colision_pelota_bloques y colision_pelota_paredes_y_paleta).

    Parámetros
    ----------
    posicion_pelota_x : int or float
        Posición X actual de la pelota.
    posicion_pelota_y : int or float
        Posición Y actual de la pelota.
    velocidad_pelota_x : int or float
        Velocidad en el eje X (positiva = derecha, negativa = izquierda).
    velocidad_pelota_y : int or float
        Velocidad en el eje Y (positiva = abajo, negativa = arriba).

    Returns
    -------
    tuple
        (nueva_x, nueva_y): posiciones actualizadas de la pelota.
    """
    posicion_pelota_x += velocidad_pelota_x
    posicion_pelota_y += velocidad_pelota_y

    return posicion_pelota_x, posicion_pelota_y
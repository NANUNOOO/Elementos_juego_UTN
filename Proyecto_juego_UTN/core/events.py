import pygame

from settings import *
from entities.paddle import *
from utils import state
from utils.file_manager import guardar_nuevo_puntaje

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

def procesar_eventos(estado_actual):
    for evento in pygame.event.get():
        
        # --- Cerrar juego ---
        if evento.type == pygame.QUIT:
            return False, estado_actual   # False = salir del juego

        # --- Eventos del ESTADO JUEGO ---
        if estado_actual == "JUEGO":

            # Iniciar lanzamiento con ESPACIO
            if not state.juego_esta_activo and state.vidas_jugador > 0:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    state.juego_esta_activo = True

            # Se quedó sin vidas → GAME OVER
            if not state.juego_esta_activo and state.vidas_jugador <= 0:
                estado_actual = "GAME_OVER"

        # --- Eventos del ESTADO GAME OVER ---
        elif estado_actual == "GAME_OVER":

            if evento.type == pygame.KEYDOWN:

                # ENTER → guardar puntaje y cambiar a ranking
                if evento.key == pygame.K_RETURN:
                    nombre = state.nombre_usuario_entrada or "Anonimo"
                    guardar_nuevo_puntaje(nombre, state.puntuacion_actual)
                    estado_actual = "RANKING"

                # BACKSPACE → borrar letra
                elif evento.key == pygame.K_BACKSPACE:
                    state.nombre_usuario_entrada = state.nombre_usuario_entrada[:-1]

                # Escribir letra (máx 10 chars)
                else:
                    if (
                        len(state.nombre_usuario_entrada) < 10
                        and evento.unicode.isalnum()
                    ):
                        state.nombre_usuario_entrada += evento.unicode

    return True, estado_actual
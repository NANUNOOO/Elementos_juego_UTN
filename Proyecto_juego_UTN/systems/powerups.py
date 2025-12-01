import pygame

from utils import state
from settings import *

def activar_power_up(tipo_power_up):
    tiempo_expiracion_nuevo = pygame.time.get_ticks() + state.DURACION_POWER_UP_MILISEGUNDOS

    # Refrescar tiempo si ya existe
    for efecto_existente in state.lista_efectos_activos:
        if efecto_existente["tipo"] == tipo_power_up:
            efecto_existente["expira_en"] = tiempo_expiracion_nuevo
            return

    # Agregar nuevo efecto
    state.lista_efectos_activos.append({
        "tipo": tipo_power_up,
        "expira_en": tiempo_expiracion_nuevo
    })

    centro_x_paleta_anterior = state.rectangulo_paleta.centerx

    if tipo_power_up == "hoja":
        nuevo_ancho = int(state.ANCHO_PALETA_ORIGINAL * 1.4)
        state.imagen_paleta_actual = pygame.transform.scale(state.imagen_paleta_base, (nuevo_ancho, 30))
        state.rectangulo_paleta.width = nuevo_ancho
        state.rectangulo_paleta.centerx = centro_x_paleta_anterior

    elif tipo_power_up == "fuego":
        nuevo_ancho = int(state.ANCHO_PALETA_ORIGINAL * 0.6)
        state.imagen_paleta_actual = pygame.transform.scale(state.imagen_paleta_base, (nuevo_ancho, 30))
        state.rectangulo_paleta.width = nuevo_ancho
        state.rectangulo_paleta.centerx = centro_x_paleta_anterior

    elif tipo_power_up == "viento":
        state.velocidad_pelota_x *= 1.3
        state.velocidad_pelota_y *= 1.3

    elif tipo_power_up == "gota":
        state.velocidad_pelota_x *= 0.7
        state.velocidad_pelota_y *= 0.7


def desactivar_power_up(tipo_power_up):
    centro_x_paleta_anterior = state.rectangulo_paleta.centerx

    if tipo_power_up in ["hoja", "fuego"]:
        state.imagen_paleta_actual = pygame.transform.scale(
            state.imagen_paleta_base,
            (state.ANCHO_PALETA_ORIGINAL, 30)
        )
        state.rectangulo_paleta.width = state.ANCHO_PALETA_ORIGINAL
        state.rectangulo_paleta.centerx = centro_x_paleta_anterior

    elif tipo_power_up in ["viento", "gota"]:
        direccion_x = 1 if state.velocidad_pelota_x > 0 else -1
        direccion_y = 1 if state.velocidad_pelota_y > 0 else -1
        state.velocidad_pelota_x = state.VELOCIDAD_PELOTA_BASE * direccion_x
        state.velocidad_pelota_y = state.VELOCIDAD_PELOTA_BASE * direccion_y
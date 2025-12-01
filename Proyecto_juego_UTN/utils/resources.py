import pygame
import os

from assets.fonts.font_loader import crear_fuente_titulo,crear_fuente_botones,crear_fuente_general,crear_fuente_puntuacion
from settings import *
import state

diccionario_imagenes_bloques = {}
diccionario_imagenes_powerups = {}

def cargar_imagen(ruta_archivo, tamano_deseado=None):
    imagen_cargada = pygame.image.load(ruta_archivo)
    if tamano_deseado:
        imagen_cargada = pygame.transform.scale(imagen_cargada, tamano_deseado)
    return imagen_cargada

def inicializar_recursos():
    global imagen_paleta_base, imagen_corazon_1, diccionario_imagenes_bloques, diccionario_imagenes_powerups
    global IMAGEN_FONDO, fuente_titulo_principal, fuente_botones, fuente_texto_general, fuente_puntuacion

    fuente_titulo_principal  = crear_fuente_titulo()
    fuente_botones = crear_fuente_botones()
    fuente_texto_general = crear_fuente_general()
    fuente_puntuacion = crear_fuente_puntuacion()

    # Imágenes
    IMAGEN_FONDO = cargar_imagen("fondoazul.jpg", (ANCHO, ALTO))
    # Icono (opcional)
    if os.path.exists("imagenes/arkanoide.png"):
        pygame.display.set_icon(cargar_imagen("imagenes/arkanoide.png"))

    imagen_paleta_base = cargar_imagen("imagenes/barraroja2.png", (170, 30))
    imagen_corazon_1 = cargar_imagen("imagenes/corazon1.png", (45, 45))

    state.diccionario_imagenes_bloques = {
        "rojo": cargar_imagen("imagenes/cuborojo.jpg", (65, 23)),
        "verde": cargar_imagen("imagenes/cuboverde.jpg", (65, 23)),
        "azul": cargar_imagen("imagenes/cuboazul.jpg", (65, 23)),
        "gris": cargar_imagen("imagenes/cubogris.jpg", (65, 23)),
    }

    state.diccionario_imagenes_powerups = {
        "hoja": cargar_imagen("imagenes/hoja.png", (40, 40)),
        "fuego": cargar_imagen("imagenes/fuego2.png", (40, 40)),
        "viento": cargar_imagen("imagenes/viento.png", (40, 40)),
        "gota": cargar_imagen("imagenes/gota.png", (40, 40)),
    }
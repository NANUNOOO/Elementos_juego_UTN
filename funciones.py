import pygame
import random
import os
from constantes import *

# --- VARIABLES GLOBALES (ESTADO DEL JUEGO) ---
# Las definimos aquí para poder modificarlas desde las funciones
lista_bloques = []
lista_power_ups_cayendo = []
lista_efectos_activos = []

posicion_pelota_x = 0
posicion_pelota_y = 0
velocidad_pelota_x = 0
velocidad_pelota_y = 0
vidas_jugador = 3
puntuacion_actual = 0
juego_esta_activo = False
nombre_usuario_entrada = ""

# Variables para imágenes y rectángulos (se inician en inicializar_recursos)
imagen_paleta_actual = None
rectangulo_paleta = None
imagen_paleta_base = None
imagen_corazon_1 = None
diccionario_imagenes_bloques = {}
diccionario_imagenes_powerups = {}
fuente_titulo_principal = None
fuente_botones = None
fuente_texto_general = None
fuente_puntuacion = None
IMAGEN_FONDO = None

# --- GESTION DE RECURSOS ---

def cargar_imagen(ruta_archivo, tamano_deseado=None):
    # Sin try-except, si falla el juego se cierra avisando el error
    imagen_cargada = pygame.image.load(ruta_archivo)
    if tamano_deseado:
        imagen_cargada = pygame.transform.scale(imagen_cargada, tamano_deseado)
    return imagen_cargada

def inicializar_recursos():
    """Carga todas las imágenes y fuentes. Llamar despues de pygame.init()"""
    global imagen_paleta_base, imagen_corazon_1, diccionario_imagenes_bloques, diccionario_imagenes_powerups
    global IMAGEN_FONDO, fuente_titulo_principal, fuente_botones, fuente_texto_general, fuente_puntuacion
    
    # Fuentes
    fuente_titulo_principal = pygame.font.SysFont("Arial", 50, bold=True)
    fuente_botones = pygame.font.SysFont("Arial", 30, bold=True)
    fuente_texto_general = pygame.font.SysFont("Arial", 25)
    fuente_puntuacion = pygame.font.Font(None, 36)

    # Imágenes
    IMAGEN_FONDO = cargar_imagen("fondoazul.jpg", (ANCHO_VENTANA, ALTO_VENTANA))
    # Icono (opcional)
    if os.path.exists("imagenes/arkanoide.png"):
        pygame.display.set_icon(cargar_imagen("imagenes/arkanoide.png"))

    imagen_paleta_base = cargar_imagen("imagenes/barraroja2.png", (170, 30))
    imagen_corazon_1 = cargar_imagen("imagenes/corazon1.png", (45, 45))

    diccionario_imagenes_bloques["rojo"] = cargar_imagen("imagenes/cuborojo.jpg", (65, 23))
    diccionario_imagenes_bloques["verde"] = cargar_imagen("imagenes/cuboverde.jpg", (65, 23))
    diccionario_imagenes_bloques["azul"] = cargar_imagen("imagenes/cuboazul.jpg", (65, 23))
    diccionario_imagenes_bloques["gris"] = cargar_imagen("imagenes/cubogris.jpg", (65, 23))

    diccionario_imagenes_powerups["hoja"] = cargar_imagen("imagenes/hoja.png", (40, 40))
    diccionario_imagenes_powerups["fuego"] = cargar_imagen("imagenes/fuego2.png", (40, 40))
    diccionario_imagenes_powerups["viento"] = cargar_imagen("imagenes/viento.png", (40, 40))
    diccionario_imagenes_powerups["gota"] = cargar_imagen("imagenes/gota.png", (40, 40))

# --- FUNCIONES DE DIBUJO ---

def dibujar_texto_centrado(superficie_destino, texto_a_mostrar, fuente_texto, color_texto, posicion_y):
    superficie_texto = fuente_texto.render(texto_a_mostrar, True, color_texto)
    rectangulo_texto = superficie_texto.get_rect(center=(ANCHO_VENTANA // 2, posicion_y))
    superficie_destino.blit(superficie_texto, rectangulo_texto)

def dibujar_boton_interactivo(superficie_destino, rectangulo_boton, texto_boton):
    posicion_mouse = pygame.mouse.get_pos()
    
    if rectangulo_boton.collidepoint(posicion_mouse):
        color_actual_boton = COLOR_AZUL_HOVER
    else:
        color_actual_boton = COLOR_AZUL_BOTON
    
    pygame.draw.rect(superficie_destino, color_actual_boton, rectangulo_boton, border_radius=12)
    pygame.draw.rect(superficie_destino, COLOR_GRIS_CLARO, rectangulo_boton, 2, border_radius=12)
    
    superficie_texto = fuente_botones.render(texto_boton, True, COLOR_BLANCO)
    rectangulo_texto = superficie_texto.get_rect(center=rectangulo_boton.center)
    superficie_destino.blit(superficie_texto, rectangulo_texto)
    
    if rectangulo_boton.collidepoint(posicion_mouse) and pygame.mouse.get_pressed()[0]:
        return True
    return False

# --- ARCHIVOS ---

def leer_ranking_desde_archivo():
    nombre_archivo_puntajes = "ranking.txt" # Cambiado a ranking.txt
    lista_mejores_puntajes = []
    
    if os.path.exists(nombre_archivo_puntajes):
        with open(nombre_archivo_puntajes, "r") as archivo_lectura:
            for linea_texto in archivo_lectura:
                datos_jugador = linea_texto.strip().split(",")
                if len(datos_jugador) == 2:
                    nombre_jugador = datos_jugador[0]
                    puntaje_jugador = int(datos_jugador[1])
                    lista_mejores_puntajes.append((nombre_jugador, puntaje_jugador))
        
    lista_mejores_puntajes.sort(key=lambda x: x[1], reverse=True)
    return lista_mejores_puntajes[:5]

def guardar_nuevo_puntaje(nombre_jugador, puntaje_obtenido):
    nombre_archivo_puntajes = "ranking.txt" # Cambiado a ranking.txt
    with open(nombre_archivo_puntajes, "a") as archivo_escritura:
        archivo_escritura.write(f"{nombre_jugador},{puntaje_obtenido}\n")

# --- LOGICA DE JUEGO ---

def iniciar_nueva_partida():
    global lista_bloques, vidas_jugador, puntuacion_actual, juego_esta_activo
    global lista_efectos_activos, lista_power_ups_cayendo
    global posicion_pelota_x, posicion_pelota_y, velocidad_pelota_x, velocidad_pelota_y
    global imagen_paleta_actual, rectangulo_paleta, nombre_usuario_entrada
    
    vidas_jugador = 3
    puntuacion_actual = 0
    nombre_usuario_entrada = ""
    juego_esta_activo = False
    lista_efectos_activos = []
    lista_power_ups_cayendo = []
    
    # Reiniciar Paleta
    imagen_paleta_actual = imagen_paleta_base.copy()
    imagen_paleta_actual = pygame.transform.scale(imagen_paleta_actual, (ANCHO_PALETA_ORIGINAL, 30))
    rectangulo_paleta = imagen_paleta_actual.get_rect()
    rectangulo_paleta.centerx = ANCHO_VENTANA // 2
    rectangulo_paleta.y = ALTO_VENTANA - 80
    
    # Reiniciar Pelota
    posicion_pelota_x = ANCHO_VENTANA // 2
    posicion_pelota_y = ALTO_VENTANA - 170
    velocidad_pelota_x = VELOCIDAD_PELOTA_BASE
    velocidad_pelota_y = -VELOCIDAD_PELOTA_BASE
    
    # Generar Bloques
    lista_bloques.clear()
    cantidad_filas = random.choice([7, 8])
    cantidad_columnas = cantidad_filas
    ancho_bloque_individual = 65
    alto_bloque_individual = 23
    espacio_entre_bloques = 10 
    
    for indice_fila in range(cantidad_filas):
        for indice_columna in range(cantidad_columnas):
            ancho_total = cantidad_columnas * ancho_bloque_individual + (cantidad_columnas - 1) * espacio_entre_bloques
            margen_x = (ANCHO_VENTANA - ancho_total) // 2
            
            pos_x = indice_columna * (ancho_bloque_individual + espacio_entre_bloques) + margen_x
            pos_y = indice_fila * (alto_bloque_individual + espacio_entre_bloques) + 30 
            
            rect = pygame.Rect(pos_x, pos_y, ancho_bloque_individual, alto_bloque_individual)
            tipo = random.choice(LISTA_TIPOS_BLOQUES)
            
            lista_bloques.append({
                "rectangulo": rect, 
                "tipo": tipo, 
                "imagen": diccionario_imagenes_bloques[tipo]
            })

def activar_power_up(tipo_power_up):
    global imagen_paleta_actual, rectangulo_paleta, velocidad_pelota_x, velocidad_pelota_y
    tiempo_expiracion_nuevo = pygame.time.get_ticks() + DURACION_POWER_UP_MILISEGUNDOS
    
    for efecto_existente in lista_efectos_activos:
        if efecto_existente["tipo"] == tipo_power_up:
            efecto_existente["expira_en"] = tiempo_expiracion_nuevo
            return

    lista_efectos_activos.append({"tipo": tipo_power_up, "expira_en": tiempo_expiracion_nuevo})
    
    centro_x_paleta_anterior = rectangulo_paleta.centerx
    
    if tipo_power_up == "hoja":
        nuevo_ancho = int(ANCHO_PALETA_ORIGINAL * 1.4)
        imagen_paleta_actual = pygame.transform.scale(imagen_paleta_base, (nuevo_ancho, 30))
        rectangulo_paleta.width = nuevo_ancho
        rectangulo_paleta.centerx = centro_x_paleta_anterior
        
    elif tipo_power_up == "fuego":
        nuevo_ancho = int(ANCHO_PALETA_ORIGINAL * 0.6)
        imagen_paleta_actual = pygame.transform.scale(imagen_paleta_base, (nuevo_ancho, 30))
        rectangulo_paleta.width = nuevo_ancho
        rectangulo_paleta.centerx = centro_x_paleta_anterior
        
    elif tipo_power_up == "viento":
        velocidad_pelota_x *= 1.3
        velocidad_pelota_y *= 1.3
        
    elif tipo_power_up == "gota":
        velocidad_pelota_x *= 0.7
        velocidad_pelota_y *= 0.7

def desactivar_power_up(tipo_power_up):
    global imagen_paleta_actual, rectangulo_paleta, velocidad_pelota_x, velocidad_pelota_y
    centro_x_paleta_anterior = rectangulo_paleta.centerx
    
    if tipo_power_up in ["hoja", "fuego"]:
        imagen_paleta_actual = pygame.transform.scale(imagen_paleta_base, (ANCHO_PALETA_ORIGINAL, 30))
        rectangulo_paleta.width = ANCHO_PALETA_ORIGINAL
        rectangulo_paleta.centerx = centro_x_paleta_anterior
        
    elif tipo_power_up in ["viento", "gota"]:
        direccion_x = 1 if velocidad_pelota_x > 0 else -1
        direccion_y = 1 if velocidad_pelota_y > 0 else -1
        velocidad_pelota_x = VELOCIDAD_PELOTA_BASE * direccion_x
        velocidad_pelota_y = VELOCIDAD_PELOTA_BASE * direccion_y
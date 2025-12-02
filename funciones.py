import pygame
import random
import os
from constantes import *
from mapas_niveles.configuracion_niveles import *

# --- VARIABLES GLOBALES (ESTADO DEL JUEGO) ---
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
sonido_habilitado = True

# Variables para imágenes y recursos
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

diccionario_sonidos = {}

# --- GESTION DE RECURSOS ---

def cargar_imagen(ruta_archivo, tamano_deseado=None):
    """
    Carga una imagen desde un archivo y, opcionalmente, la redimensiona a un tamaño específico.

    Args:
        ruta_archivo (str): La ruta al archivo de la imagen.
        tamano_deseado (tuple, optional): Una tupla (ancho, alto) para redimensionar la imagen. 
                                          Si es None, se usa el tamaño original. Defaults to None.

    Returns:
        pygame.Surface: El objeto imagen de Pygame cargado y escalado.
    """
    imagen_cargada = pygame.image.load(ruta_archivo)
    if tamano_deseado:
        imagen_cargada = pygame.transform.scale(imagen_cargada, tamano_deseado)
    return imagen_cargada

def cargar_sonido(nombre_archivo):
    """
    Carga un archivo de sonido, establece su volumen y maneja errores si el archivo no se encuentra.

    Args:
        nombre_archivo (str): El nombre del archivo de sonido (asume que está en la carpeta 'sonidos/').

    Returns:
        pygame.mixer.Sound o None: El objeto de sonido de Pygame cargado, o None si el archivo no existe.
    """
    ruta = os.path.join("sonidos", nombre_archivo)
    if os.path.exists(ruta):
        sonido = pygame.mixer.Sound(ruta)
        sonido.set_volume(VOLUMEN_EFECTOS)
        return sonido
    else:
        print(f"Advertencia: No se encontró el sonido {nombre_archivo}")
        return None

def inicializar_recursos():
    """
    Inicializa el sistema de mezcla de audio (pygame.mixer) y carga todos los recursos 
    globales del juego (fuentes, imágenes, sonidos y música de fondo).
    
    Modifica las variables globales: imagen_paleta_base, diccionario_imagenes_bloques, etc.
    """
    global imagen_paleta_base, imagen_corazon_1, diccionario_imagenes_bloques, diccionario_imagenes_powerups
    global IMAGEN_FONDO, fuente_titulo_principal, fuente_botones, fuente_texto_general, fuente_puntuacion
    global diccionario_sonidos

    pygame.mixer.init()
    
    fuente_titulo_principal = pygame.font.SysFont("Arial", 50, bold=True)
    fuente_botones = pygame.font.SysFont("Arial", 30, bold=True)
    fuente_texto_general = pygame.font.SysFont("Arial", 25)
    fuente_puntuacion = pygame.font.Font(None, 36)

    IMAGEN_FONDO = cargar_imagen("imagenes/fondoazul.jpg", (ANCHO_VENTANA, ALTO_VENTANA))
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

    # --- CARGA DE SONIDOS ---
    diccionario_sonidos["rebote"] = cargar_sonido("rebote.wav")
    diccionario_sonidos["romper"] = cargar_sonido("romper.wav")
    diccionario_sonidos["perder_vida"] = cargar_sonido("perder.wav")
    diccionario_sonidos["game_over"] = cargar_sonido("game_over.wav")
    diccionario_sonidos["powerup"] = cargar_sonido("powerup.wav")

    # Música de fondo (Ahora busca .wav que es lo que genera el script)
    ruta_musica = os.path.join("sonidos", "musica_fondo.wav")
    if os.path.exists(ruta_musica):
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
        pygame.mixer.music.play(-1)
    else:
        print("Advertencia: No se encontró musica_fondo.wav")

# --- FUNCIONES DE AUDIO ---

def reproducir_sonido(nombre):
    """
    Reproduce un efecto de sonido específico, solo si el audio está habilitado globalmente.

    Args:
        nombre (str): La clave del sonido a reproducir dentro del 'diccionario_sonidos' (ej. "rebote").
    """
    if sonido_habilitado and nombre in diccionario_sonidos and diccionario_sonidos[nombre]:
        diccionario_sonidos[nombre].play()

def alternar_sonido():
    """
    Activa o desactiva globalmente el audio del juego ('sonido_habilitado'). 
    Pausa o reanuda la música de fondo según el nuevo estado.
    """
    global sonido_habilitado
    sonido_habilitado = not sonido_habilitado
    
    if sonido_habilitado:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

# --- FUNCIONES DE ORDENAMIENTO Y ARCHIVOS ---

def ordenar_de_mayor_a_menor(matriz, columna_puntaje):
    """
    Implementa el algoritmo de ordenamiento Burbuja para ordenar una lista de tuplas o listas 
    de forma descendente, basándose en el valor de una columna específica (usado para el ranking).

    Args:
        matriz (list): Una lista de listas/tuplas (ej. [("Mati", 100), ...]). 
                       Esta lista es modificada directamente.
        columna_puntaje (int): El índice de la columna que contiene el puntaje a comparar (ej. 1).
    """
    n = len(matriz)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if matriz[j][columna_puntaje] < matriz[j + 1][columna_puntaje]:
                aux = matriz[j + 1]
                matriz[j + 1] = matriz[j]
                matriz[j] = aux

def leer_ranking_desde_archivo():
    """
    Lee los nombres y puntajes desde el archivo "ranking.txt", los parsea, los ordena 
    de mayor a menor y devuelve solo el top 5 de los mejores puntajes.

    Returns:
        list: Una lista con las 5 mejores tuplas (nombre_jugador, puntaje_jugador) o menos.
    """
    nombre_archivo_puntajes = "ranking.txt"
    lista_mejores_puntajes = []
    if os.path.exists(nombre_archivo_puntajes):
        with open(nombre_archivo_puntajes, "r") as archivo_lectura:
            for linea_texto in archivo_lectura:
                datos_jugador = linea_texto.strip().split(",")
                if len(datos_jugador) == 2:
                    nombre_jugador = datos_jugador[0]
                    puntaje_jugador = int(datos_jugador[1])
                    lista_mejores_puntajes.append((nombre_jugador, puntaje_jugador))
    
    ordenar_de_mayor_a_menor(lista_mejores_puntajes, 1)
    return lista_mejores_puntajes[:5]

def guardar_nuevo_puntaje(nombre_jugador, puntaje_obtenido):
    """
    Agrega el puntaje del jugador actual al archivo "ranking.txt" en una nueva línea.

    Args:
        nombre_jugador (str): El nombre que ingresó el jugador.
        puntaje_obtenido (int): La puntuación final obtenida en la partida.
    """
    nombre_archivo_puntajes = "ranking.txt"
    with open(nombre_archivo_puntajes, "a") as archivo_escritura:
        archivo_escritura.write(f"{nombre_jugador},{puntaje_obtenido}\n")

# --- DIBUJO ---

def dibujar_texto_centrado(superficie_destino, texto_a_mostrar, fuente_texto, color_texto, posicion_y):
    """
    Dibuja una cadena de texto centrada horizontalmente en la ventana, en una posición Y dada.

    Args:
        superficie_destino (pygame.Surface): La superficie donde se dibujará (generalmente la pantalla).
        texto_a_mostrar (str): El texto que se va a dibujar.
        fuente_texto (pygame.font.Font): El objeto fuente de Pygame a utilizar.
        color_texto (tuple): El color del texto.
        posicion_y (int): La coordenada Y donde se centrará el texto.
    """
    superficie_texto = fuente_texto.render(texto_a_mostrar, True, color_texto)
    rectangulo_texto = superficie_texto.get_rect(center=(ANCHO_VENTANA // 2, posicion_y))
    superficie_destino.blit(superficie_texto, rectangulo_texto)

def dibujar_boton_interactivo(superficie_destino, rectangulo_boton, texto_boton):
    """
    Dibuja un botón con efecto de "hover" (cambio de color al pasar el mouse) y detecta si fue clickeado.

    Args:
        superficie_destino (pygame.Surface): La pantalla donde se dibuja.
        rectangulo_boton (pygame.Rect): El objeto Rect que define la posición y tamaño del botón.
        texto_boton (str): El texto que se muestra dentro del botón.

    Returns:
        bool: True si el botón fue clickeado (mouse presionado), False en caso contrario.
    """
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

# --- LOGICA DE JUEGO ---

def iniciar_nueva_partida(reinicio_completo=False):
    """
    Configura o reinicia el estado de un nivel. Reinicia la posición y velocidad de la paleta y la pelota. 
    Genera el tablero de bloques a partir del mapa del nivel actual.

    Args:
        reinicio_completo (bool, optional): Si es True, reinicia el puntaje, vidas y el índice de nivel a cero. 
                                            Si es False, solo prepara el siguiente nivel. Defaults to False.
    """
    global lista_bloques, vidas_jugador, puntuacion_actual, juego_esta_activo
    global lista_efectos_activos, lista_power_ups_cayendo
    global posicion_pelota_x, posicion_pelota_y, velocidad_pelota_x, velocidad_pelota_y
    global imagen_paleta_actual, rectangulo_paleta, nombre_usuario_entrada
    global nivel_actual_indice
    
    if reinicio_completo :
        vidas_jugador = 3
        puntuacion_actual = 0
        nombre_usuario_entrada = ""
        nivel_actual_indice = 0
    
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
    ancho_bloque_individual = 65
    alto_bloque_individual = 23
    espacio_entre_bloques = 10 
      
    # 1. Obtener la configuración del nivel actual
    config_nivel = CONFIGURACION_NIVELES[nivel_actual_indice]
    mapa_nivel = config_nivel["mapa"]

    # Calcular el ancho total del tablero para centrarlo (lo tomas de la primera fila)
    cantidad_columnas = len(mapa_nivel[0])
    ancho_total = cantidad_columnas * ancho_bloque_individual + (cantidad_columnas - 1) * espacio_entre_bloques
    margen_x = (ANCHO_VENTANA - ancho_total) // 2

    for indice_fila, fila in enumerate(mapa_nivel):
        for indice_columna, tipo_bloque_str in enumerate(fila):
            
            # 2. Ignorar si la celda está vacía
            if tipo_bloque_str == "vacio":
                continue 
            
            # 3. Calcular la posición (igual que lo hacías antes)
            pos_x = indice_columna * (ancho_bloque_individual + espacio_entre_bloques) + margen_x
            pos_y = indice_fila * (alto_bloque_individual + espacio_entre_bloques) + 30 
            
            rect = pygame.Rect(pos_x, pos_y, ancho_bloque_individual, alto_bloque_individual)
            
            
            lista_bloques.append({
                "rectangulo": rect, 
                "tipo": tipo_bloque_str, # Aquí usamos directamente el color
                "imagen": diccionario_imagenes_bloques[tipo_bloque_str]
            })


def activar_power_up(tipo_power_up):
    """
    Aplica el efecto de un power-up al juego (modifica la paleta o la velocidad de la pelota) 
    y lo añade a la lista de efectos activos con un temporizador. Si el efecto ya está activo, 
    reinicia su temporizador.

    Args:
        tipo_power_up (str): El tipo de power-up activado (ej. "hoja", "fuego", "viento", "gota").
    """
    global imagen_paleta_actual, rectangulo_paleta, velocidad_pelota_x, velocidad_pelota_y
    
    reproducir_sonido("powerup")

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
    """
    Revierte el efecto de un power-up que ha expirado, devolviendo la paleta o la velocidad 
    de la pelota a sus valores base/normales, ajustando la dirección actual.

    Args:
        tipo_power_up (str): El tipo de power-up que se va a desactivar.
    """
    global imagen_paleta_actual, rectangulo_paleta, velocidad_pelota_x, velocidad_pelota_y
    centro_x_paleta_anterior = rectangulo_paleta.centerx
    
    if tipo_power_up in ["hoja", "fuego"]:
        imagen_paleta_actual = pygame.transform.scale(imagen_paleta_base, (ANCHO_PALETA_ORIGINAL, 30))
        rectangulo_paleta.width = ANCHO_PALETA_ORIGINAL
        rectangulo_paleta.centerx = centro_x_paleta_anterior
        
    elif tipo_power_up in ["viento", "gota"]:
        # Normaliza la velocidad de vuelta a la velocidad base, manteniendo la dirección
        max_velocidad_componente = max(abs(velocidad_pelota_x), abs(velocidad_pelota_y))
        if max_velocidad_componente > 0:
            factor_escala = VELOCIDAD_PELOTA_BASE / max_velocidad_componente
            velocidad_pelota_x *= factor_escala
            velocidad_pelota_y *= factor_escala


def dibujar_mensaje_victoria_nivel(superficie_destino, estado_actual_ref):
    """
    Dibuja la pantalla de 'Nivel Completado' con un botón 'Continuar'. 
    Si se presiona, avanza al siguiente nivel y cambia el estado del juego.

    Args:
        superficie_destino (pygame.Surface): La pantalla.
        estado_actual_ref (list): Una lista mutable que contiene el estado actual del juego (ej. ["PAUSA"]).

    Returns:
        bool: True si se presionó el botón "CONTINUAR", False en caso contrario.
    """
    global nivel_actual_indice, juego_esta_activo
    
    # 1. Dibujar el mensaje de victoria
    dibujar_texto_centrado(superficie_destino, 
                            f"¡NIVEL {nivel_actual_indice} COMPLETO!", 
                            fuente_titulo_principal, 
                            COLOR_BLANCO, 
                            ALTO_VENTANA // 3)
    
    # 2. Botón de Continuar
    rect_boton = pygame.Rect(0, 0, 250, 60)
    rect_boton.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2)
    
    if dibujar_boton_interactivo(superficie_destino, rect_boton, "CONTINUAR"):
        # Al presionar, inicia el nuevo nivel y vuelve al estado JUEGO
        iniciar_nueva_partida() # Esta función lee el nuevo nivel_actual_indice
        juego_esta_activo = False # Para que la pelota espere el ESPACIO
        estado_actual_ref[0] = "JUEGO" # Cambia el estado en el main.py
        return True
    return False


def dibujar_mensaje_victoria_final(superficie_destino, estado_actual_ref):
    """
    Dibuja la pantalla de 'Victoria Total' (Juego Completado), mostrando la puntuación final 
    y un botón para volver al menú principal.

    Args:
        superficie_destino (pygame.Surface): La pantalla.
        estado_actual_ref (list): Una lista mutable que contiene el estado actual del juego (ej. ["PAUSA"]).

    Returns:
        bool: True si se presionó el botón "VOLVER AL MENÚ", False en caso contrario.
    """
    global puntuacion_actual
    
    # 1. Dibujar el mensaje de victoria final
    dibujar_texto_centrado(superficie_destino, 
                            "¡FELICIDADES, JUEGO COMPLETADO!", 
                            fuente_titulo_principal, 
                            COLOR_BLANCO, 
                            ALTO_VENTANA // 3)
                            
    dibujar_texto_centrado(superficie_destino, 
                            f"Puntuación Final: {puntuacion_actual}", 
                            fuente_puntuacion, 
                            COLOR_BLANCO, 
                            ALTO_VENTANA // 3 + 80)
    # 2. Botón para volver al Menú
    rect_boton = pygame.Rect(0, 0, 250, 60)
    rect_boton.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + 150)
    
    if dibujar_boton_interactivo(superficie_destino, rect_boton, "VOLVER AL MENÚ"):
        # Reinicia el índice de nivel para una nueva partida desde 0
        global nivel_actual_indice
        nivel_actual_indice = 0 
        estado_actual_ref[0] = "MENU" # Cambia el estado en el main.py
        return True
    return False

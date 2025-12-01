
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
ANCHO_PALETA_ORIGINAL = 170
VELOCIDAD_PELOTA_BASE = 5
DURACION_POWER_UP_SEGUNDOS = 6
DURACION_POWER_UP_MILISEGUNDOS = DURACION_POWER_UP_SEGUNDOS * 1000 
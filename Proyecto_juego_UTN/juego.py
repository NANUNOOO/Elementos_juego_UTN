import pygame
import random

from constantes import ALTO, ANCHO, NOMBRE_DEL_JUEGO

pygame.init ()


ventana = pygame.display.set_mode((ANCHO, ALTO))

ICONO = pygame.image.load("imagenes/arkanoide.png")
COLOR_FONDO = (8, 15, 46)
BLANCO = (255, 255, 255)
IMAGEN_FONDO = pygame.image.load("imagenes/fondoazul.jpg")
paleta = pygame.image.load ("imagenes/barraroja2.png")
paleta = pygame.transform.scale(paleta, (170, 30))
clock = pygame.time.Clock()
bandera_dibujo = True

#ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN) # para pantalla completa
# ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE) # para pantalla redimensionable
#ventana = pygame.display.set_mode((ANCHO, ALTO), pygame.NOFRAME) # para pantalla sin bordes
pygame.display.set_caption(NOMBRE_DEL_JUEGO)
pygame.display.set_icon(ICONO)

velocidad_paleta = 15

paleta_rect = paleta.get_rect()
paleta_rect.x = ANCHO // 2 - paleta_rect.width // 2
paleta_rect.y = ALTO - 80 

#Pelota 
posicion_pelota_x = ANCHO // 2
posicion_pelota_y = ALTO - 170
radio_pelota = 12
velocidad_pelota_x = 4
velocidad_pelota_y = -4


# bloques
filas = 8
columnas = 8
ancho_bloque = 60
alto_bloque = 20
espacio = 10  # separación entre bloques

#colores posibles

colores_posibles = [(255, 0, 0), #rojo
                    (0, 255, 0), #verde
                    (0, 128, 255), #azul
                    (176, 174, 174) #gris
                    ]

bloques = []

for fila in range(filas):
    for columnas in range(columnas + 1):
        x = columnas * (ancho_bloque + espacio) + 90
        y = fila * (alto_bloque + espacio) + 30
        bloque = pygame.Rect(x, y, ancho_bloque, alto_bloque)
        color = random.choice(colores_posibles)# Se carga un color aleatorio
        bloques.append({"rect":bloque, "color":color})


clock = pygame.time.Clock()

corriendo = True

while corriendo:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            corriendo = False
  
    
    ventana.blit(IMAGEN_FONDO, (0,0))
    ventana.blit(paleta, paleta_rect)

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_LEFT] and paleta_rect.x> 0:
        paleta_rect.x -= velocidad_paleta

    if keys[pygame.K_RIGHT] and paleta_rect.x + paleta_rect.width < ANCHO:
        paleta_rect.x += velocidad_paleta
        


    posicion_pelota_x += velocidad_pelota_x
    posicion_pelota_y += velocidad_pelota_y

    pelota = pygame.draw.circle(ventana, (255, 255, 255), (posicion_pelota_x, posicion_pelota_y), radio_pelota)
    pelota_top_cords = (pelota.centerx, pelota.centery - (pelota.height / 2))
    pelota_bottom_cords = (pelota.centerx, pelota.centery + (pelota.height / 2))
    pelota_left_cords = (pelota.centerx - (pelota.width / 2), pelota.centery)
    pelota_right_cords = (pelota.centerx + (pelota.width / 2), pelota.centery)


    bloques_a_borrar = []

    for bloque in bloques:
        bloque_rect = pygame.draw.rect(ventana, bloque["color"], bloque["rect"], border_radius=5)


        if bloque_rect.collidepoint(pelota_top_cords): 
            velocidad_pelota_y *= -1
            bloques_a_borrar.append(bloque) 
        elif bloque_rect.collidepoint(pelota_bottom_cords): 
            velocidad_pelota_y *= -1
            bloques_a_borrar.append(bloque)
        elif bloque_rect.collidepoint(pelota_left_cords): 
            velocidad_pelota_x *= -1 
            bloques_a_borrar.append(bloque)
        elif bloque_rect.collidepoint(pelota_right_cords): 
            velocidad_pelota_x *= -1 
            bloques_a_borrar.append(bloque)


    for bloque_rect in bloques_a_borrar:
        bloques.remove(bloque_rect)
        
    #Rebote contra las paredes
    if posicion_pelota_x - radio_pelota <= 0 or posicion_pelota_x + radio_pelota >= ANCHO:
        velocidad_pelota_x *= -1
    if posicion_pelota_y - radio_pelota <= 0:
        velocidad_pelota_y *= -1

    #Rebote en la paleta
    if paleta_rect.collidepoint(pelota_bottom_cords):
        velocidad_pelota_y *= -1



    pygame.display.flip()
    clock.tick(50)

pygame.quit()
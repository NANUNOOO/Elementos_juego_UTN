# 1. Librerías estándar de Python
import sys
import os
import random

# 2. Librerías externas
import pygame

# 3. Nuestras librerías locales
from constantes import *
import funciones 

# --- INICIALIZACION ---
pygame.init()

ventana_principal = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption(NOMBRE_DEL_JUEGO)
reloj_control = pygame.time.Clock()

# Inicializamos las imagenes y fuentes
funciones.inicializar_recursos()

# --- VARIABLES LOCALES DEL MENU ---
ESTADO_ACTUAL = "MENU"
se_hizo_clic_previamente = False
coord_centro_x_pantalla = ANCHO_VENTANA // 2

# Definición de Botones
rectangulo_boton_jugar = pygame.Rect(0, 0, 250, 50)
rectangulo_boton_jugar.center = (coord_centro_x_pantalla, 200)

rectangulo_boton_ranking = pygame.Rect(0, 0, 250, 50)
rectangulo_boton_ranking.center = (coord_centro_x_pantalla, 270)

rectangulo_boton_creditos = pygame.Rect(0, 0, 250, 50)
rectangulo_boton_creditos.center = (coord_centro_x_pantalla, 340)

rectangulo_boton_salir = pygame.Rect(0, 0, 250, 50)
rectangulo_boton_salir.center = (coord_centro_x_pantalla, 410)

rectangulo_boton_volver = pygame.Rect(20, ALTO_VENTANA - 70, 150, 50)

juego_corriendo = True

# --- BUCLE PRINCIPAL ---
while juego_corriendo:
    tiempo_actual_milisegundos = pygame.time.get_ticks()
    mouse_esta_presionado = pygame.mouse.get_pressed()[0]
    
    # --- 1. PROCESAMIENTO DE EVENTOS ---
    for evento_detectado in pygame.event.get():
        if evento_detectado.type == pygame.QUIT:
            juego_corriendo = False
        
        # Eventos estado JUEGO (Solo inputs como ESPACIO)
        if ESTADO_ACTUAL == "JUEGO":
            if not funciones.juego_esta_activo and funciones.vidas_jugador > 0:
                if evento_detectado.type == pygame.KEYDOWN and evento_detectado.key == pygame.K_SPACE:
                    funciones.juego_esta_activo = True
            
            # se saco el chequeo de game over para que no espere una tecla y me salte la pantalla que me pida el nombre

        # Eventos estado GAME_OVER
        elif ESTADO_ACTUAL == "GAME_OVER":
            if evento_detectado.type == pygame.KEYDOWN:
                if evento_detectado.key == pygame.K_RETURN:
                    nombre = funciones.nombre_usuario_entrada if funciones.nombre_usuario_entrada else "Anonimo"
                    funciones.guardar_nuevo_puntaje(nombre, funciones.puntuacion_actual)
                    ESTADO_ACTUAL = "RANKING"
                elif evento_detectado.key == pygame.K_BACKSPACE:
                    funciones.nombre_usuario_entrada = funciones.nombre_usuario_entrada[:-1]
                else:
                    if len(funciones.nombre_usuario_entrada) < 10 and evento_detectado.unicode.isalnum():
                        funciones.nombre_usuario_entrada += evento_detectado.unicode

    # --- 2. LOGICA DE CAMBIO DE ESTADO AUTOMÁTICO ---
    # Verificamos si perdió FUERA del bucle de eventos. Así es instantáneo.
    if ESTADO_ACTUAL == "JUEGO" and funciones.vidas_jugador <= 0:
        ESTADO_ACTUAL = "GAME_OVER"

    # --- 3. DIBUJO Y LOGICA DE JUEGO ---
    ventana_principal.blit(funciones.IMAGEN_FONDO, (0, 0))

    if ESTADO_ACTUAL == "MENU":
        funciones.dibujar_texto_centrado(ventana_principal, "ARKANOID PRO", funciones.fuente_titulo_principal, COLOR_BLANCO, 100)
        
        if funciones.dibujar_boton_interactivo(ventana_principal, rectangulo_boton_jugar, "JUGAR") and not se_hizo_clic_previamente:
            funciones.iniciar_nueva_partida()
            ESTADO_ACTUAL = "JUEGO"
            
        if funciones.dibujar_boton_interactivo(ventana_principal, rectangulo_boton_ranking, "RANKING") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "RANKING"
            
        if funciones.dibujar_boton_interactivo(ventana_principal, rectangulo_boton_creditos, "CREDITOS") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "CREDITOS"
            
        if funciones.dibujar_boton_interactivo(ventana_principal, rectangulo_boton_salir, "SALIR") and not se_hizo_clic_previamente:
            juego_corriendo = False

    elif ESTADO_ACTUAL == "RANKING":
        funciones.dibujar_texto_centrado(ventana_principal, "MEJORES PUNTAJES", funciones.fuente_titulo_principal, COLOR_BLANCO, 80)
        lista_top_5 = funciones.leer_ranking_desde_archivo()
        pos_y = 180
        
        if not lista_top_5:
            funciones.dibujar_texto_centrado(ventana_principal, "No hay datos disponibles", funciones.fuente_botones, COLOR_BLANCO, pos_y)
        
        for indice, (nombre, puntos) in enumerate(lista_top_5):
            texto = f"{indice + 1}. {nombre} - {puntos}"
            funciones.dibujar_texto_centrado(ventana_principal, texto, funciones.fuente_botones, COLOR_BLANCO, pos_y)
            pos_y += 60
            
        if funciones.dibujar_boton_interactivo(ventana_principal, rectangulo_boton_volver, "VOLVER") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "MENU"

    elif ESTADO_ACTUAL == "CREDITOS":
        funciones.dibujar_texto_centrado(ventana_principal, "ALUMNOS", funciones.fuente_titulo_principal, COLOR_BLANCO, 100)
        lista_alumnos = ["Barrera, Valeria", "Macura, Matias", "Ruiz Diaz, Nahuel"]
        pos_y = 200
        for alumno in lista_alumnos:
            funciones.dibujar_texto_centrado(ventana_principal, alumno, funciones.fuente_botones, COLOR_BLANCO, pos_y)
            pos_y += 50
            
        if funciones.dibujar_boton_interactivo(ventana_principal, rectangulo_boton_volver, "VOLVER") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "MENU"

    elif ESTADO_ACTUAL == "GAME_OVER":
        funciones.dibujar_texto_centrado(ventana_principal, "GAME OVER", funciones.fuente_titulo_principal, COLOR_BLANCO, 150)
        funciones.dibujar_texto_centrado(ventana_principal, f"Puntuacion Final: {funciones.puntuacion_actual}", funciones.fuente_botones, COLOR_BLANCO, 220)
        
        funciones.dibujar_texto_centrado(ventana_principal, "Ingresa tu nombre:", funciones.fuente_texto_general, COLOR_GRIS_CLARO, 300)
        
        pygame.draw.rect(ventana_principal, COLOR_BLANCO, (coord_centro_x_pantalla - 100, 330, 200, 40), 2)
        funciones.dibujar_texto_centrado(ventana_principal, funciones.nombre_usuario_entrada, funciones.fuente_botones, COLOR_BLANCO, 350)
        
        funciones.dibujar_texto_centrado(ventana_principal, "Presiona ENTER para guardar", funciones.fuente_texto_general, COLOR_GRIS_CLARO, 450)

    elif ESTADO_ACTUAL == "JUEGO":
        # UI
        texto_pts = funciones.fuente_puntuacion.render(f"Puntos: {funciones.puntuacion_actual}", True, COLOR_BLANCO)
        ventana_principal.blit(texto_pts, (ANCHO_VENTANA - 150, ALTO_VENTANA - 40))
        
        for i in range(funciones.vidas_jugador):
            ventana_principal.blit(funciones.imagen_corazon_1, (30 + (i * 45), ALTO_VENTANA - 60))

        ventana_principal.blit(funciones.imagen_paleta_actual, funciones.rectangulo_paleta)
        
        if funciones.vidas_jugador > 0:
            pygame.draw.circle(ventana_principal, COLOR_BLANCO, (int(funciones.posicion_pelota_x), int(funciones.posicion_pelota_y)), RADIO_PELOTA)
        
        if not funciones.juego_esta_activo and funciones.vidas_jugador > 0:
            mensaje = funciones.fuente_texto_general.render("Presiona ESPACIO para lanzar", True, COLOR_BLANCO)
            rect_msg = mensaje.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
            ventana_principal.blit(mensaje, rect_msg)
            
            funciones.posicion_pelota_x = funciones.rectangulo_paleta.centerx
            funciones.posicion_pelota_y = funciones.rectangulo_paleta.top - RADIO_PELOTA - 2

        if funciones.juego_esta_activo and funciones.vidas_jugador > 0:
            # Gestion PowerUps
            a_borrar_efectos = []
            for ef in funciones.lista_efectos_activos:
                if tiempo_actual_milisegundos >= ef["expira_en"]:
                    funciones.desactivar_power_up(ef["tipo"])
                    a_borrar_efectos.append(ef)
            for ef in a_borrar_efectos: funciones.lista_efectos_activos.remove(ef)
            
            # Movimiento Paleta
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and funciones.rectangulo_paleta.left > 0:
                funciones.rectangulo_paleta.x -= VELOCIDAD_PALETA
            if keys[pygame.K_RIGHT] and funciones.rectangulo_paleta.right < ANCHO_VENTANA:
                funciones.rectangulo_paleta.x += VELOCIDAD_PALETA
            
            # Movimiento Pelota
            funciones.posicion_pelota_x += funciones.velocidad_pelota_x
            funciones.posicion_pelota_y += funciones.velocidad_pelota_y
            
            # Rebotes
            if funciones.posicion_pelota_x - RADIO_PELOTA <= 0 or funciones.posicion_pelota_x + RADIO_PELOTA >= ANCHO_VENTANA:
                funciones.velocidad_pelota_x *= -1
            if funciones.posicion_pelota_y - RADIO_PELOTA <= 0:
                funciones.velocidad_pelota_y *= -1
            
            # Perder Vida
            if funciones.posicion_pelota_y + RADIO_PELOTA >= ALTO_VENTANA:
                funciones.vidas_jugador -= 1
                funciones.juego_esta_activo = False
                for ef in funciones.lista_efectos_activos: funciones.desactivar_power_up(ef["tipo"])
                funciones.lista_efectos_activos.clear()
                funciones.lista_power_ups_cayendo.clear()
            
            # Colision Paleta
            rect_pelota = pygame.Rect(funciones.posicion_pelota_x - RADIO_PELOTA, funciones.posicion_pelota_y - RADIO_PELOTA, RADIO_PELOTA * 2, RADIO_PELOTA * 2)
            if funciones.rectangulo_paleta.colliderect(rect_pelota) and funciones.velocidad_pelota_y > 0:
                funciones.velocidad_pelota_y *= -1
                diff = (funciones.rectangulo_paleta.centerx - funciones.posicion_pelota_x) / (funciones.rectangulo_paleta.width / 2)
                funciones.velocidad_pelota_x = -diff * 5 + (funciones.velocidad_pelota_x * 0.5)

            # Colision Bloques
            bloques_borrar = []
            for bloque in funciones.lista_bloques:
                ventana_principal.blit(bloque["imagen"], bloque["rectangulo"])
                if bloque["rectangulo"].colliderect(rect_pelota):
                    funciones.velocidad_pelota_y *= -1
                    funciones.puntuacion_actual += VALORES_PUNTOS_BLOQUES[bloque["tipo"]]
                    bloques_borrar.append(bloque)
                    if random.random() < 0.3:
                        tipo = random.choice(LISTA_TIPOS_POWER_UP)
                        rect_pu = funciones.diccionario_imagenes_powerups[tipo].get_rect(center=bloque["rectangulo"].center)
                        funciones.lista_power_ups_cayendo.append({"rectangulo": rect_pu, "tipo": tipo, "imagen": funciones.diccionario_imagenes_powerups[tipo]})
            for b in bloques_borrar: funciones.lista_bloques.remove(b)

            # Movimiento PowerUps
            pu_borrar = []
            for pu in funciones.lista_power_ups_cayendo:
                pu["rectangulo"].y += VELOCIDAD_CAIDA_POWERUP
                ventana_principal.blit(pu["imagen"], pu["rectangulo"])
                if funciones.rectangulo_paleta.colliderect(pu["rectangulo"]):
                    funciones.activar_power_up(pu["tipo"])
                    pu_borrar.append(pu)
                elif pu["rectangulo"].top > ALTO_VENTANA:
                    pu_borrar.append(pu)
            for pu in pu_borrar: funciones.lista_power_ups_cayendo.remove(pu)
        else:
            for bloque in funciones.lista_bloques:
                ventana_principal.blit(bloque["imagen"], bloque["rectangulo"])

    se_hizo_clic_previamente = mouse_esta_presionado
    pygame.display.flip()
    reloj_control.tick(CUADROS_POR_SEGUNDO)

pygame.quit()
sys.exit()
from core.ui import *

def estado_menu():
    if ESTADO_ACTUAL == "MENU":
        dibujar_texto_centrado(ventana_principal, "ARKANOID PRO", fuente_titulo_principal, COLOR_BLANCO, 100)
        
        # Botón JUGAR
        if dibujar_boton_interactivo(ventana_principal, rect_jugar, "JUGAR") and not se_hizo_clic_previamente:
            iniciar_nueva_partida()
            ESTADO_ACTUAL = "JUEGO"
            
        # Botón RANKING
        if dibujar_boton_interactivo(ventana_principal, rect_ranking, "RANKING") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "RANKING"
            
        # Botón CRÉDITOS
        if dibujar_boton_interactivo(ventana_principal, rect_creditos, "CREDITOS") and not se_hizo_clic_previamente:
            ESTADO_ACTUAL = "CREDITOS"
            
        # Botón SALIR
        if dibujar_boton_interactivo(ventana_principal, rect_salir, "SALIR") and not se_hizo_clic_previamente:
            juego_corriendo = False
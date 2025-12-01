from utils.game_states.estado_menu import *
from utils.game_states.estado_ranking import *
from utils.game_states.estado_creditos import *
from utils.game_states.estado_game_over import *
from utils.game_states.estado_juego import *

def run_game(ESTADO_ACTUAL):

    while True:
        if ESTADO_ACTUAL == "MENU":
            ESTADO_ACTUAL = estado_menu()
        
        elif ESTADO_ACTUAL == "RANKING":
            ESTADO_ACTUAL = estado_ranking()

        elif ESTADO_ACTUAL == "CREDITOS":
            ESTADO_ACTUAL = estado_creditos()

        elif ESTADO_ACTUAL == "GAME_OVER":
            ESTADO_ACTUAL = estado_game_over()

        elif ESTADO_ACTUAL == "JUEGO":
            ESTADO_ACTUAL = estado_juego()
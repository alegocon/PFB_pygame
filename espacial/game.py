import pygame as pg
from espacial.escenes import Partida, GameOver

pg.init()

class Game:
    def __init__(self, ancho=1200, alto=600):
        pantalla = pg.display.set_mode((ancho, alto))
        self.escenas = [Partida(pantalla), GameOver(pantalla)]


    def lanzar(self):
        escena_activa = 0
        game_active = True
        retorno = []
        while game_active:
            game_active = self.escenas[escena_activa].bucle_ppal(retorno)
            retorno = game_active
            escena_activa += 1
            if escena_activa == 1:
                game_active = self.escenas[escena_activa].bucle_ppal(retorno)
            if escena_activa == len(self.escenas):
                escena_activa = 0
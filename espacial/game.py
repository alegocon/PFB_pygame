import pygame as pg
from espacial.escenes import Intro, Partida, GameOver

pg.init()

class Game:
    def __init__(self, ancho=1200, alto=600):
        pantalla = pg.display.set_mode((ancho, alto))
        self.escenas = [Intro(pantalla), Partida(pantalla), GameOver(pantalla)]


    def lanzar(self):
        player = 'Jugador'
        puntos = int
        escena_activa = 0
        estado = ''
        game_active = [True,]
        while game_active:
            if escena_activa == 0:
                game_active = self.escenas[escena_activa].bucle_ppal([True,'',''])
                player = game_active[1]
                escena_activa += 1

            game_active = self.escenas[escena_activa].bucle_ppal([True, player, estado])

            if escena_activa == 1:
                puntos = game_active[1]            
                escena_activa += 1

            game_active = self.escenas[escena_activa].bucle_ppal([True, puntos, estado])
            escena_activa += 1
            
            if escena_activa == len(self.escenas):
                escena_activa = 1

                
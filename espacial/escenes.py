import pygame as pg

from espacial.entities import Planeta, Nave, Asteroide
from espacial import niveles, FPS
import random

class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_ppal():
        pass

class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.planeta = Planeta(self.pantalla, self.pantalla.get_width(), 
                         self.pantalla.get_height() // 2)
        self.nave = Nave(self.pantalla, 10, 
                         self.pantalla.get_height()//2, 100, 20)
        self.asteroides = []
        self.todos = []
        self.reset()

    def reset(self):
        self.asteroides = []
        self.todos = []
        self.todos.append(self.planeta)
        self.todos.append(self.nave)
        self.contador_vidas = 3


    def crea_asteroides(self):
        for l in range (0, len(niveles[0])):
            l = Asteroide(self.pantalla, niveles[0][l][0], niveles[0][l][1], 100, 20)
            self.asteroides.append(l)
        
        self.todos = self.todos + self.asteroides

    def bucle_ppal(self) -> bool:
        self.reset()
        self.crea_asteroides()
        # Inicializaciones 

        while self.contador_vidas > 0:
            # Este if equivale a
            # and  len(self.ladrillos) > 0
            # puesto en la línea del while
            
            self.reloj.tick(FPS)

            eventos = pg.event.get()
            for evento in eventos:
                if evento.type == pg.QUIT:
                    return False

            self.pantalla.fill((255, 0, 0))    

            for objeto in self.todos:
                objeto.mover()

            for asteroide in self.asteroides:
                #if asteroide.comprobarToque(self.nave):
                #    print('toque')
                if (self.nave.x in range (asteroide.x, asteroide.x + asteroide.ancho) or \
                    self.nave.ancho + self.nave.x in range (asteroide.x, asteroide.x + asteroide.ancho)) and \
                    (self.nave.y in range (asteroide.y - asteroide.alto, asteroide.y) or \
                    self.nave.y - self.nave.alto in range (asteroide.y - asteroide.alto, asteroide.y)):
                    print('choque')
                    self.asteroides.remove(asteroide)
                    self.todos.remove(asteroide)
                    self.contador_vidas -=1
                    print(self.contador_vidas)
            
                    #print ('Y check: ', self.nave.y - self.nave.alto,"(", asteroide.y - asteroide.alto, asteroide.y,")")
                    #print ('Y check: ', self.nave.y,"(", asteroide.y - asteroide.alto, asteroide.y,")")
                    #print ('X check: ', self.nave.x,"(", asteroide.x, asteroide.x + asteroide.ancho,")")
                    #print ('X check: ', self.nave.ancho + self.nave.x,"(", asteroide.x, asteroide.ancho,")")
                
            for objeto in self.todos:
                objeto.dibujar()

            pg.display.flip()

        return True

class GameOver(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/FredokaOne-Regular.ttf", 25)

    def bucle_ppal(self):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return True

            self.pantalla.fill((30, 30, 255))
            texto = self.fuente.render("GAME OVER", True, (255, 255, 0))
            print(texto.get_rect())

            self.pantalla.blit(texto, (10, 10))

            pg.display.flip()


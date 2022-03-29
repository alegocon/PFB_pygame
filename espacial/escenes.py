import pygame as pg

pg.init()
pg.time.set_timer(pg.USEREVENT, 1000)

from espacial.entities import Planeta, Nave, Asteroide
from espacial import niveles, FPS, vel_nivel


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_ppal():
        pass

class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/FredokaOne-Regular.ttf", 25)
        self.planeta = Planeta(self.pantalla, self.pantalla.get_width(), 
                         self.pantalla.get_height() // 2)
        self.nave = Nave(self.pantalla, 10, 
                         self.pantalla.get_height()//2, 100, 20, 2)

    def reset(self):
        self.asteroides = []
        self.todos = []
        self.todos.append(self.planeta)
        self.todos.append(self.nave)
        
    def crea_asteroides(self, nivel):
        for l in range (0, len(niveles[nivel])):
            l = Asteroide(self.pantalla, niveles[nivel][l][0], niveles[nivel][l][1], 50, 25, vel_nivel[nivel])
            self.asteroides.append(l)
        
        self.todos = self.todos + self.asteroides

    def timer(self):
        self.text='10'.rjust(3)
        self.counter = 10

    def bucle_ppal(self) -> bool:
        nivel = 0
        self.contador_vidas = 3


        while self.contador_vidas > 0 and nivel < len(niveles):
            self.reset()
            self.crea_asteroides(nivel)
            self.timer()

            while self.counter >= 0 and self.contador_vidas > 0 and self.nave.viva:
                
                self.reloj.tick(FPS)

                eventos = pg.event.get()
                for evento in eventos:
                    if evento.type == pg.QUIT:
                        return False
                    elif evento.type == pg.USEREVENT:
                        self.counter -= 1
                        self.text = str(self.counter).rjust(3)

                self.pantalla.fill((255, 0, 0))    

                for objeto in self.todos:
                    objeto.mover()

                for asteroide in self.asteroides:

                    if asteroide.comprobarToque(self.nave):
                        self.asteroides.remove(asteroide)
                        self.todos.remove(asteroide)
                        self.nave.viva = False

                for objeto in self.todos:
                    objeto.dibujar()

                Marcador = self.fuente.render("Tiempo restante: " + self.text + "s | Vidas: " + str(self.contador_vidas) + " | Nivel " + str(nivel), True, (255, 255, 0))
                print(Marcador.get_rect())

                self.pantalla.blit(Marcador, (700, 10))

                pg.display.flip()

            if self.nave.viva:
                while self.nave.x <= 900:
                    self.pantalla.fill((255, 0, 0))  
                    self.nave.x += self.nave.vx
                    self.planeta.dibujar()
                    self.nave.dibujar()
                    pg.display.flip()
                self.nave.reset()
                nivel += 1
            else:
                self.contador_vidas -=1
                self.nave.reset()

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

            self.pantalla.blit(texto, (10, 10))

            pg.display.flip()


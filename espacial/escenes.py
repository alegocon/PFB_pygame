import pygame as pg

pg.init()
pg.time.set_timer(pg.USEREVENT, 1000)

from espacial.entities import Planeta, Nave, Asteroide, Astronauta
from espacial import niveles, FPS, vel_nivel
import random
import sqlite3


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_ppal():
        pass
"""
class Intro(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/AGENCYR.TTF", 100)
        self.fuente2 = pg.font.Font("resources/fonts/AGENCYR.TTF", 50)
        self.user_text = ''

        self.input_rect = pg.Rect(200,200,140,70)
        self.color_active = pg.Color('lightskyblue3')
        self.color_passive = pg.Color('gray15')
        self.color = self.color_passive
        self.active = False

    def bucle_ppal(self):

        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return True

                if evento.type == pg.MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(evento.pos):
                        self.active = True
                    else:
                        self.active = False

                if evento.type == pg.KEYDOWN:
                    if self.active == True:
                        if evento.key == pg.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        else:
                            self.user_text += evento.unicode

            self.pantalla.fill((0, 0, 0))

            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_passive
        
            pg.draw.rect(self.pantalla,self.color,self.input_rect,2)

            text_surface = self.fuente2.render(self.user_text,True,(255,255,255))
            self.pantalla.blit(text_surface,(self.input_rect.x +5,self.input_rect.y + 5))
            self.input_rect.w=max(100,text_surface.get_width())
            pg.display.flip()

            #return self.user_text
"""
        

class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.duracion = 30
        self.fuente = pg.font.Font("resources/fonts/AGENCYR.TTF", 30)
        self.fuente2 = pg.font.Font("resources/fonts/AGENCYR.TTF", 60)
        self.planeta = Planeta(self.pantalla, 1000, 100, 0)
        self.nave = Nave(self.pantalla, 20, -200, 2)
        self.astronauta = Astronauta(self.pantalla, 2400, 300, 2)
        

    def reset(self):
        self.asteroides = []
        self.astronautas = []
        self.todos = []
        self.todos.append(self.planeta)
        self.todos.append(self.astronauta)
        self.todos.append(self.nave)

    def crea_astronautas(self):
        for i in range (0, 5):
            i = Astronauta(self.pantalla, random.randint(1200,2400), 300, 2)
            self.astronautas.append(i)
        self.todos = self.todos + self.asteroides
        
    def crea_asteroides(self, nivel):
        for l in range (0, len(niveles[nivel])):
            l = Asteroide(self.pantalla, niveles[nivel][l][0], niveles[nivel][l][1], vel_nivel[nivel], l)
            self.asteroides.append(l)
        self.todos = self.todos + self.asteroides

    def timer(self):
        self.counter = self.duracion

    def bucle_ppal(self, puntos): 
        nivel = 0
        self.contador_vidas = 3
        self.contador_frames = 0
        self.puntuacion = 0
        
        while self.contador_vidas > 0 and nivel < len(niveles):
            self.reset()
            self.crea_asteroides(nivel)
            self.timer()
            self.nave.reset() 

            while self.counter >= 0 and self.contador_vidas > 0 and self.nave.viva:
                
                self.reloj.tick(FPS)

                eventos = pg.event.get()
                for evento in eventos:
                    if evento.type == pg.QUIT:
                        return False
                    elif evento.type == pg.USEREVENT:
                        self.counter -= 1
                        self.text = str(self.counter).rjust(3)

                self.pantalla.fill((0, 0, 0))    

                for objeto in self.todos:
                    objeto.mover()

                for asteroide in self.asteroides:

                    if asteroide.comprobarToque(self.nave):
                        self.asteroides.remove(asteroide)
                        self.todos.remove(asteroide)
                        self.nave.viva = False

                for astronauta in self.astronautas:
                    
                    if astronauta.comprobarToque(self.nave):
                        self.puntuacion += 50
                        self.astronautas.remove(astronauta)
                        self.todos.remove(astronauta)


                for objeto in self.todos:
                    objeto.dibujar()

                self.contador_frames +=1
                if self.contador_frames == 300:
                    self.puntuacion += 25
                    self.contador_frames = 0

                Marcador = self.fuente.render("Puntuacion: " + str(self.puntuacion) + " | Tiempo restante: " + self.text + "s | Vidas: " + str(self.contador_vidas) + " | Nivel " + str(nivel), True, (102, 204, 102))
                self.pantalla.blit(Marcador, (650, 10))

                pg.display.flip()

            if self.nave.viva:
                self.puntuacion += self.puntuacion
                while self.nave.x <= 900:
                    self.pantalla.fill((0, 0, 0))  
                    self.nave.x += self.nave.vx
                    self.planeta.dibujar()
                    self.nave.dibujar()
                    Mensaje= self.fuente2.render("Bien hecho! Pasas al nivel " + str(nivel+1), True, (102, 204, 102))
                    self.pantalla.blit(Mensaje, (300, 300))
                    pg.display.flip()
                self.nave.reset()
                nivel += 1

            else:
                self.contador_vidas -=1
                if self.contador_vidas > 0:
                    while not self.nave.viva:
                        self.pantalla.fill((0, 0, 0)) 
                        Mensaje = self.fuente2.render("BOOM!!!! Te quedan " + str(self.contador_vidas) + " vidas", True, (102, 204, 102))
                        Mensaje2 = self.fuente.render("Presiona tecla ESPACIO para continuar", True, (102, 204, 102))
                        self.pantalla.blit(Mensaje, (300, 200))
                        self.pantalla.blit(Mensaje2, (300, 500))
                        self.planeta.dibujar()
                        self.nave.dibujar()
                        pg.display.flip()

                        eventos = pg.event.get()
                        for evento in eventos:
                            if evento.type == pg.QUIT:
                                return False
                            if evento.type == pg.KEYDOWN:
                                if evento.key == pg.K_SPACE:
                                    self.nave.reset()
                else:
                    conn = sqlite3.connect('score.db')
                    conn.execute("INSERT INTO puntuaciones (Puntos) \
                            VALUES (?)", (self.puntuacion,))
                    conn.commit()
                    conn.close()               
        return [True, self.puntuacion]


class GameOver(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/AGENCYR.TTF", 100)
        self.fuente2 = pg.font.Font("resources/fonts/AGENCYR.TTF", 50)

    def bucle_ppal(self, retorno):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return True
            
            puntuacion = str(retorno[1])

            self.pantalla.fill((30, 30, 255))
            texto = self.fuente.render("GAME OVER", True, (102, 204, 102))
            texto2 = self.fuente2.render("Tu puntuacion fue " + puntuacion, True, (102, 204, 102))

            self.pantalla.blit(texto, (500, 300))
            self.pantalla.blit(texto2, (500, 500))

            pg.display.flip()


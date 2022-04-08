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

class Intro(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/AGENCYR.TTF", 100)
        self.fuente2 = pg.font.Font("resources/fonts/AGENCYR.TTF", 30)
        self.fuente3 = pg.font.Font("resources/fonts/AGENCYR.TTF", 25)
        self.background = pg.image.load("./resources/img/intro.png")
        self.user_text = ''

        self.input_rect = pg.Rect(self.pantalla.get_width()//2-70,self.pantalla.get_height()//2+100,150,50)
        self.color_active = pg.Color('lightskyblue3')
        self.color_passive = pg.Color('gray15')
        self.color = self.color_passive
        self.active = False

    def bucle_ppal(self, retorno):

        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return [True, self.user_text]
                        

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

            self.pantalla.fill((0,0,0))
            self.pantalla.blit(self.background, (0,0))

            if self.active:
                self.color = self.color_active
            else:
                self.color = self.color_passive
        
            pg.draw.rect(self.pantalla,self.color,self.input_rect,2)

            texto = self.fuente.render("THE QUEST", True, (102, 204, 102))
            texto2 = self.fuente3.render("TU MISIÓN: Encuentra y coloniza nuevos planetas para salvar a la especie humana de su propio exterminio.", True, (102, 204, 102))
            texto3 = self.fuente3.render("Introduce tu nombre en el cuadro inferior y pulsa la tecla ESPACIO cuando estés listo.", True, (102, 204, 102))
            texto4 = self.fuente2.render("BUENA SUERTE!", True, (102, 204, 102))
            texto5 = self.fuente2.render("PLAYER: ", True, (102, 204, 102))
            text_surface = self.fuente2.render(self.user_text,True,(255,255,255))
        
            self.pantalla.blit(texto, (self.pantalla.get_width()//2 - texto.get_width()//2 - 200, self.pantalla.get_height()//2 - texto.get_height()//2 -200))
            self.pantalla.blit(texto2, (self.pantalla.get_width()//2 - texto.get_width()//2 - 200, self.pantalla.get_height()//2 - texto.get_height()//2-50))
            self.pantalla.blit(texto3, (self.pantalla.get_width()//2 - texto.get_width()//2 - 200, self.pantalla.get_height()//2 - texto.get_height()//2))
            self.pantalla.blit(texto4, (self.pantalla.get_width()//2 - texto.get_width()//2+100, self.pantalla.get_height()//2 + texto.get_height()//2-40))
            self.pantalla.blit(texto5, (self.pantalla.get_width()//2 - texto.get_width()//2, self.pantalla.get_height()//2 + 112))
            self.pantalla.blit(text_surface,(self.input_rect.x +10,self.input_rect.y + 10))
            self.input_rect.w=max(150,text_surface.get_width())

            pg.display.flip()
        

class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/AGENCYR.TTF", 30)
        self.fuente2 = pg.font.Font("resources/fonts/AGENCYR.TTF", 60)
        self.planeta = Planeta(self.pantalla, 1000, 100, 0)
        self.nave = Nave(self.pantalla, 20, -200, 2)
        
    def reset(self, nivel):
        self.counter = 3
        self.asteroides = []
        self.astronautas = []
        self.todos = []
        self.todos.append(self.planeta)
        self.todos.append(self.nave)
        self.crea_astronautas()
        self.crea_asteroides(nivel)

    def crea_astronautas(self):
        for l in range (0, 3):
            l = Astronauta(self.pantalla, random.randint(1200,2400), random.randint(0,600), 5)
            self.astronautas.append(l)
        self.todos = self.todos + self.astronautas
        
    def crea_asteroides(self, nivel):
        for l in range (0, len(niveles[nivel])):
            l = Asteroide(self.pantalla, niveles[nivel][l][0], niveles[nivel][l][1], vel_nivel[nivel], l)
            self.asteroides.append(l)
        self.todos = self.todos + self.asteroides

    def bucle_ppal(self, retorno): 
        nivel = 0
        self.contador_vidas = 3
        self.contador_frames = 0
        self.puntuacion = 0
        self.cuenta = ''
        self.player = retorno[1]
        self.nave.viva = retorno[2]
        
        self.reset(nivel)
        self.nave.reset()

        while self.contador_vidas > 0 and nivel < len(niveles)-1:
            
            while self.counter >= 0 and self.contador_vidas > 0 and self.nave.viva and nivel <= len(niveles)-1:
                self.reloj.tick(FPS)

                eventos = pg.event.get()
                for evento in eventos:
                    if evento.type == pg.QUIT:
                        return False
                    elif evento.type == pg.USEREVENT:
                        self.cuenta = str(self.counter).rjust(3)
                        self.counter -= 1

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

                Marcador = self.fuente.render("Puntuacion: " + str(self.puntuacion) + " | Tiempo restante: " + self.cuenta + "s | Vidas: " + str(self.contador_vidas) + " | Nivel " + str(nivel), True, (102, 204, 102))
                self.pantalla.blit(Marcador, (650, 10))
                pg.display.flip()

                if self.counter == 0 and self.nave.viva and nivel < len(niveles)-1:
                    self.nave.aterriza = True
                    self.nave.y = self.pantalla.get_height()//2 - 100
                    i = 1
                    contador_frames = 0
                    while self.nave.x <= 1000:
                        self.pantalla.fill((0, 0, 0)) 
                        self.nave.avanzar()
                        if self.nave.x > 700:
                            contador_frames += 1
                            self.nave.rotar(i)
                            if contador_frames == 40:
                                i += 1
                                contador_frames = 0
                        self.planeta.dibujar()
                        self.nave.dibujar()
                        Mensaje= self.fuente2.render("Bien hecho! Pasas al nivel " + str(nivel+1), True, (102, 204, 102))
                        Mensaje2 = self.fuente.render("Presiona tecla ESPACIO para continuar", True, (102, 204, 102))
                        self.pantalla.blit(Mensaje, (self.pantalla.get_width()//2 - Mensaje.get_width()//2, self.pantalla.get_height()//2 - Mensaje.get_height()//2))
                        self.pantalla.blit(Mensaje2, (self.pantalla.get_width()//2 - Mensaje2.get_width()//2, self.pantalla.get_height()//2 - Mensaje2.get_height()//2 + 75))
                        pg.display.flip()
                    nivel += 1
                    self.reset(nivel)
                    self.nave.reset()
                    pg.event.clear()

                elif not self.nave.viva:
                    self.contador_vidas -=1
                    if self.contador_vidas > 0:
                        while not self.nave.viva:
                            self.pantalla.fill((0, 0, 0)) 
                            Mensaje = self.fuente2.render("BOOM!!!! Te quedan " + str(self.contador_vidas) + " vidas", True, (102, 204, 102))
                            Mensaje2 = self.fuente.render("Presiona tecla ESPACIO para continuar", True, (102, 204, 102))
                            self.pantalla.blit(Mensaje, (self.pantalla.get_width()//2 - Mensaje.get_width()//2, self.pantalla.get_height()//2 - Mensaje.get_height()//2))
                            self.pantalla.blit(Mensaje2, (self.pantalla.get_width()//2 - Mensaje2.get_width()//2, self.pantalla.get_height()//2 - Mensaje2.get_height()//2 + 75))
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
                                        self.reset(nivel)
                    else:
                        conn = sqlite3.connect('score.db')
                        conn.execute("INSERT INTO puntuaciones (Player,Puntos) \
                                VALUES (?,?)", (self.player, self.puntuacion,))
                        conn.commit()
                        conn.close() 
              
        return [True, self.puntuacion, self.nave.viva]


class GameOver(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.fuente = pg.font.Font("resources/fonts/AGENCYR.TTF", 100)
        self.fuente2 = pg.font.Font("resources/fonts/AGENCYR.TTF", 50)
        self.fuente3 = pg.font.Font("resources/fonts/AGENCYR.TTF", 25)
        self.background = pg.image.load("./resources/img/intro.png")

    def bucle_ppal(self, retorno):
        while True:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    return False
                
                if evento.type == pg.KEYDOWN:
                    if evento.key == pg.K_SPACE:
                        return True
            if retorno[2]:
                Mensaje = "GAME OVER"
            else:
                Mensaje = "JUEGO COMPLETO"

            puntuacion = str(retorno[1])
            texto = self.fuente.render(Mensaje, True, (102, 204, 102))
            texto2 = self.fuente2.render("Tu puntuacion fue " + puntuacion, True, (102, 204, 102))
            texto3 = self.fuente3.render("TOP PUNTUACIONES", True, (102, 204, 102))
            texto4 = self.fuente3.render("Pulsa tecla ESPACIO para jugar de nuevo", True, (102, 204, 102))

            self.pantalla.blit(self.background, (0,0))
            self.pantalla.blit(texto, (self.pantalla.get_width()//2 - texto.get_width()//2, self.pantalla.get_height()//2 - texto.get_height()//2-125))
            self.pantalla.blit(texto2, (self.pantalla.get_width()//2 - texto2.get_width()//2, self.pantalla.get_height()//2 - texto2.get_height()//2-50))
            self.pantalla.blit(texto3, (self.pantalla.get_width()//2 - texto3.get_width()//2, self.pantalla.get_height()//2 - texto3.get_height()//2+25))
            self.pantalla.blit(texto4, (self.pantalla.get_width()//2 - texto4.get_width()//2, self.pantalla.get_height()-100))
            
            con = sqlite3.connect('score.db')
            cur = con.cursor()
            cur.execute("""
                        SELECT Player,Puntos 
                        FROM puntuaciones \
                        ORDER BY Puntos DESC
                        """
                )
            datos = cur.fetchall()
            cur.close()

            for i in range(3):
                
                player = self.fuente3.render(str(datos[i][0]), True, (102, 204, 102))
                separator = self.fuente3.render(str(40*'.'), True, (102, 204, 102))
                score = self.fuente3.render(str(datos[i][1]), True, (102, 204, 102))
                self.pantalla.blit(player, (self.pantalla.get_width()//2-125, self.pantalla.get_height()//2 +50+ 25*i))
                self.pantalla.blit(separator, (self.pantalla.get_width()//2-75, self.pantalla.get_height()//2 +50+ 25*i))
                self.pantalla.blit(score, (self.pantalla.get_width()//2+100, self.pantalla.get_height()//2 +50+ 25*i))
            
            pg.display.flip()


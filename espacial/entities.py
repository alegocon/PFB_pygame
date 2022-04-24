import pygame as pg
import random

class Objeto:
    def __init__(self, padre, x, y, ancho, alto, vx):
        self.padre = padre
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.vx = vx

    def intersecta(self, nave) -> bool:
        return (nave.x in range (self.x, self.x + self.ancho) or \
                nave.ancho + nave.x in range (self.x, self.x + self.ancho)) and \
                (nave.y in range (self.y, self.y + self.alto) or \
                nave.y + nave.alto in range (self.y, self.y + self.alto))

    def dibujar(self):
        pass

    def mover(self):
        pass

class Asteroide(Objeto):
    def __init__(self, padre, x, y, vx, l):

        i = l % 3
        self.imagen_ast = pg.image.load(f"./resources/img/ast-{i}.png")
        self.rect = self.imagen_ast.get_rect()
        
        super().__init__(padre, x, y, self.rect.w, self.rect.h, vx)
        self.vx = vx
        self.x_ini = x
        self.y_ini = y

    def mover(self):
        self.x -= self.vx
        if self.x + self.ancho <= 0:
            self.x = self.padre.get_width()
            self.y = self.y + random.randint(-50,50)

    def comprobarToque(self, nave):
        if self.intersecta(nave):
            return True
    
    def dibujar(self):
        self.padre.blit(self.imagen_ast, (self.x, self.y))

class Nave(Objeto):
    def __init__(self, padre, x, y, vx):
        self.images = []
        self.explosion = []
        i = 0
        for i in range(4):
            self.imagen_nave = pg.image.load(f"./resources/img/nave-{i}.png")
            self.images.append(self.imagen_nave)
        for i in range(4):
            self.nave_ex = pg.image.load(f"./resources/img/nave-ex{i}.png")
            self.explosion.append(self.nave_ex)

        self.nave_activa = 0
        self.frecuencia = 60
        self.contador_frames = 0
        self.rot_cont = 1
        self.angle = 0

        self.image = self.images[self.nave_activa]
        self.rect = self.image.get_rect()

        super().__init__(padre, x, y, self.rect.w, self.rect.h // 2, vx)
        self.vy = 2
        self.vx = 0.8
        self.x_ini = 10
        self.y_ini = self.padre.get_height() // 2 - self.rect.w//2
        self.viva = True
        self.aterriza = False

    def reset(self):
        self.x = self.x_ini
        self.y = self.y_ini
        self.vy = 2
        self.viva = True

    def avanzar(self):
        self.x += self.vx

    def rotar(self,i):
        self.img = pg.image.load(f"./resources/img/nave-{0}.png")
        self.centro = self.img.get_rect().center
        self.angle = 18*i
        self.rot_img = pg.transform.rotate(self.img, self.angle)
        self.rot_img_rect = self.rot_img.get_rect(center = self.centro)

    def dibujar(self):
        if self.viva and self.aterriza and self.x >=500:
            self.padre.blit(self.rot_img, (self.rot_img_rect.x + self.x, self.rot_img_rect.y + self.y))

        elif self.viva == True:
            self.padre.blit(self.images[self.nave_activa], (self.x, self.y))

            self.contador_frames += 1
            if self.contador_frames == self.frecuencia:
                self.nave_activa += 1
                if self.nave_activa >= len(self.images):
                    self.nave_activa = 0
                self.contador_frames = 0

        else:
            self.padre.blit(self.explosion[self.nave_activa], (self.x, self.y))

            self.contador_frames += 1
            if self.contador_frames == self.frecuencia:
                self.nave_activa += 1
                if self.nave_activa >= len(self.explosion):
                    self.nave_activa = 0
                self.contador_frames = 0

    def mover(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_UP]:
            self.y -= self.vy
        if teclas[pg.K_DOWN]:
            self.y += self.vy

        if self.y <= self.rect.h //2:
            self.y = self.rect.h //2
        if self.y + self.rect.h  >= self.padre.get_height():
            self.y = self.padre.get_height() - self.rect.h

class Planeta(Objeto):
    def __init__(self, padre, x, y, vx):

        self.imagen = pg.image.load(f"./resources/img/planet.png")
        SCALED_AST = (400, 400)
        self.imagen = pg.transform.scale(self.imagen, SCALED_AST)
        self.rect = self.imagen.get_rect()
        
        super().__init__(padre, x, y, self.rect.w, self.rect.h, vx)
        self.x_ini = x
        self.y_ini = y
        self.vy = 0

    def dibujar(self):
        self.padre.blit(self.imagen, (self.x, self.y))
        
class Astronauta(Objeto):
    def __init__(self, padre, x, y, vx):
        self.imagen = pg.image.load(f"./resources/img/astro1.png")
        self.rect = self.imagen.get_rect()
        
        super().__init__(padre, x, y, self.rect.w, self.rect.h, vx)
        self.vx = -2
        self.vy = 1
        self.x_ini = x
        self.y_ini = y

    def mover(self):
        self.x += self.vx
        self.y += self.vy

        if self.y >= 600:
            self.vy *= -1

        if self.y <= 0:
            self.vy *= -1

        if self.x <= 0:
            self.x = self.padre.get_width()

    def comprobarToque(self, nave):
        if self.intersecta(nave):
            return True
    
    def dibujar(self):
        self.padre.blit(self.imagen, (self.x, self.y))

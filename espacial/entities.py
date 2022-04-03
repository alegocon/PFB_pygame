import pygame as pg
import random

class Vigneta:
    def __init__(self, padre, x, y, ancho, alto, vx, color = (255, 255, 255)):
        self.padre = padre
        self.x = x
        self.y = y
        self.color = color
        self.ancho = ancho
        self.alto = alto
        self.vx = vx

    @property
    def xcentro(self):
        return self.x + self.ancho // 2

    @property
    def ycentro(self):
        return self.y + self.alto // 2

    def intersecta(self, nave) -> bool:
        return (nave.x in range (self.x, self.x + self.ancho) or \
                nave.ancho + nave.x in range (self.x, self.x + self.ancho)) and \
                (nave.y in range (self.y - self.alto, self.y) or \
                nave.y - nave.alto in range (self.y - self.alto, self.y))

    def dibujar(self):
        pass

    def mover(self):
        pass

class Asteroide(Vigneta):
    def __init__(self, padre, x, y, vx, l):

        i = l % 3
        self.imagen_ast = pg.image.load(f"./resources/img/ast-{i}.png")
        SCALED_AST = (75, 50)
        self.imagen_ast = pg.transform.scale(self.imagen_ast, SCALED_AST)
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
        #pg.draw.rect(self.padre, self.color, (self.x, self.y, self.ancho, self.alto))
        self.padre.blit(self.imagen_ast, (self.x, self.y))

class Nave(Vigneta):
    def __init__(self, padre, x, y, vx):
        self.images = []
        self.explosion = []
        i = 0
        for i in range(3):
            self.imagen_nave = pg.image.load(f"./resources/img/nave-{i}.png")
            SCALED_NAVE = (100, 51)
            self.images.append(pg.transform.scale(self.imagen_nave, SCALED_NAVE))
        for i in range(3):
            self.nave_ex = pg.image.load(f"./resources/img/nave-ex{i}.png")
            SCALED_NAVE = (100, 51)
            self.explosion.append(pg.transform.scale(self.nave_ex, SCALED_NAVE))

        self.nave_activa = 0
        self.frecuencia = 60
        self.contador_frames = 0

        self.image = self.images[self.nave_activa]
        self.rect = self.image.get_rect()
        
        super().__init__(padre, x, y, self.rect.w, self.rect.h // 2, vx)
        self.vy = 2
        self.vx = 0.8
        self.x_ini = 10
        self.y_ini = 0
        self.viva = True

    def reset(self):
        self.x = self.x_ini
        self.y = self.y_ini
        self.vy = 2
        self.viva = True

    def dibujar(self):

        if self.viva:
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

class Planeta(Vigneta):
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
        
class Astronauta(Vigneta):
    def __init__(self, padre, x, y, vx):

        self.imagen = pg.image.load(f"./resources/img/astro1.png")
        SCALED_AST = (100, 60)
        self.imagen_ast = pg.transform.scale(self.imagen, SCALED_AST)
        self.rect = self.imagen.get_rect()
        
        super().__init__(padre, x, y, self.rect.w, self.rect.h, vx)
        self.vx = -2
        self.vy = 2
        self.x_ini = x
        self.y_ini = y
        vy = 0

    def mover(self):
        self.x += self.vx
        self.y += self.vy

        if self.y >= 600: #self.padre.get_height() - self.rect.h:
            self.vy *= -1

        if self.y <= 0: #60 + self.rect.h:
            self.vy *= -1

        if self.x <= 0:
            self.x = self.padre.get_width()

    def comprobarToque(self, nave):
        if self.intersecta(nave):
            return True
    
    def dibujar(self):
        #pg.draw.rect(self.padre, self.color, (self.x, self.y, self.ancho, self.alto))
        self.padre.blit(self.imagen_ast, (self.x, self.y))

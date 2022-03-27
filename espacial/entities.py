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
    def __init__(self, padre, x, y, ancho, alto, vx, color = (255, 255, 255)):
        super().__init__(padre, x, y, ancho, alto, vx, color)
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
        pg.draw.rect(self.padre, self.color, (self.x, self.y, self.ancho, self.alto))

class Nave(Vigneta):
    def __init__(self, padre, x, y, ancho, alto, color = (255, 255, 0)):
        super().__init__(padre, x, y, ancho, alto, color)
        self.vy = 2

    def dibujar(self):
        pg.draw.rect(self.padre, self.color, (self.x, self.y, self.ancho, self.alto))

    def mover(self):
        teclas = pg.key.get_pressed()
        if teclas[pg.K_UP]:
            self.y -= self.vy
        if teclas[pg.K_DOWN]:
            self.y += self.vy

        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= self.padre.get_height():
            self.y = self.padre.get_height() - self.alto

class Planeta(Vigneta):
    def __init__(self, padre, x, y, color = (255, 255, 255), radio = 200):
        super().__init__(padre, x - radio, y - radio, 2 * radio, 2 * radio, color)
        self.radio = radio

    def dibujar(self):
        pg.draw.circle(self.padre, self.color, (self.xcentro, self.ycentro), self.radio)


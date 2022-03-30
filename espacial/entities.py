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
    def __init__(self, padre, x, y, ancho, alto, vx, color = (0, 0, 255)):
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
    def __init__(self, padre, x, y, vx):
        self.images = []
        i = 0
        for i in range(3):
            self.imagen_nave = pg.image.load(f"./resources/img/nave-{i}.png")
            SCALED_NAVE = (100, 51)
            self.images.append(pg.transform.scale(self.imagen_nave, SCALED_NAVE))
        self.nave_activa = 0
        self.frecuencia = 10
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
        self.padre.blit(self.images[self.nave_activa], (self.x, self.y))

        self.contador_frames += 1
        if self.contador_frames == self.frecuencia:
            self.nave_activa += 1
            if self.nave_activa >= len(self.images):
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
    def __init__(self, padre, x, y, color = (255, 255, 255), radio = 200):
        super().__init__(padre, x - radio, y - radio, 2 * radio, 2 * radio, color)
        self.radio = radio

    def dibujar(self):
        pg.draw.circle(self.padre, self.color, (self.xcentro, self.ycentro), self.radio)


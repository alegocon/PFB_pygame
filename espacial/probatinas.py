
import pygame as pg
import sys

class Print:
    def __init__(self):
        self.x = 5
        return self.x


pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode([800,800])
fuente2 = pg.font.Font(None,32)
user_text = ''

input_rect = pg.Rect(200,200,140,32)
color_active = pg.Color('lightskyblue3')
color_passive = pg.Color('gray15')
color = color_passive
active = False


while True:
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            pg.quit()
            sys.exit()

        if evento.type == pg.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(pg.mouse.get_pos()):
                active = True
            else:
                active = False
        pg.display.update()

        if evento.type == pg.KEYDOWN:
            active == True
            if evento.key == pg.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += evento.unicode

        screen.fill(pg.Color('black'))

        if active:
            color = color_active
        else:
            color = color_passive
        
        pg.draw.rect(screen,color,input_rect,2)

        text_surface = fuente2.render(user_text,True,(255,255,255))
        screen.blit(text_surface,(input_rect.x + 5,input_rect.y + 5))
        input_rect.w = max(100,text_surface.get_width()+10)

        edad = print()
        print(edad)

        Mensaje2 = fuente2.render("Tengo " + str(edad), True, (102, 204, 102))
        screen.blit(Mensaje2, (300, 200))

        pg.display.flip()
        clock.tick(60)



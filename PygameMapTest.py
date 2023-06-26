import pygame
import WFC_Test_2 as wfc

TILE_ID = wfc.TILE_ID
print(TILE_ID)
GRIDS_LIST = wfc.generate()
SWIDTH = 1440
SHEIGHT = 720
SCREEN = (SWIDTH, SHEIGHT)
SMAP = (SWIDTH, SHEIGHT*0.8) 
STILES = (SWIDTH//wfc.SIZE_X, SHEIGHT//wfc.SIZE_Y)

def load_images(): # will return arrays, initialise all the classes? maybe? 
    return


class tile:
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.ID = ID
        self.size = STILES
        self.impassable = False
        self.damages = False
        self.heals = False
        self.image = pygame.image.load('PLACEHOLDER_%s_tile.png' % ID)  # MUST CHANGE, VERY INEFFICIENT

x = 50
y = 50
vel = 15

run = True

pygame.init()

ICONS = {   # i dont know what this was for
    "" : 0
    }

win = pygame.display.set_mode(SCREEN)
player_icon = pygame.image.load('./A-Level-NEA-new/assets/PLAYER_placeholder.png')
player_icon = pygame.transform.scale(player_icon, (64 , 64))
bg = pygame.image.load('./A-Level-NEA-new/assets/BACKGROUND_placeholder.png')
pygame.display.set_caption("very cool epic game for cool people")


clock = pygame.time.Clock()


def redraw():
    win.blit(bg, (0,0))
    win.blit(player_icon, (x,y))
    pygame.display.update()

while run:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= vel

    elif keys[pygame.K_RIGHT]:
        x += vel

    elif keys[pygame.K_UP]:
        y -= vel

    elif keys[pygame.K_DOWN]:
        y += vel

    redraw()


pygame.quit()
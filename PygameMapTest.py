import pygame
import WFC_Test_2 as wfc

GRIDS_LIST = wfc.generate()
SWIDTH = 1920
SHEIGHT = 1080
SCREEN = (SWIDTH, SHEIGHT)
SMAP = (SWIDTH, SHEIGHT*0.8) 
STILES = (SWIDTH//wfc.SIZE_X, SWIDTH//wfc.SIZE_X)
print(STILES)

tile_icons = [None] * len(wfc.TILE_ID)
for id in range(len(wfc.TILE_ID)):
    tile_icons[id] =  pygame.image.load('./A-Level-NEA-new/assets/TILE_%s_placeholder.png' % id)

 
class tile:
    def __init__(self, x, y, ID):
        self.ID = ID
        self.x = x
        self.y = y
        self.size = STILES
        self.impassable = False
        self.damages = False
        self.heals = False
        self.image = pygame.transform.scale(tile_icons[self.ID], self.size) 

class entity:   # keep an eye on, inheritance may not be suitable here.
    def __init__(self):
        self.x = 0
        self.y = 0
        self.vel = 0
        self.health = 0

def conv_tiles_to_classes(maplist):
    start_y = SHEIGHT*0.2
    offsetx = SWIDTH//wfc.SIZE_X
    offsety = (SHEIGHT-start_y)//wfc.SIZE_Y
    for i in range(len(maplist)):
        for y in range(wfc.SIZE_Y):
            for x in range(wfc.SIZE_X): 
                maplist[i][y][x] = tile(x*offsetx,start_y+(y*offsety),maplist[i][y][x])
 

def draw_map(maplist, mapnum):
        map = maplist[mapnum]
        for x in range(wfc.SIZE_X):
            for y in range(wfc.SIZE_Y):
                win.blit(map[y][x].image, (map[y][x].x,map[y][x].y))
                print(map[y][x].size)

conv_tiles_to_classes(GRIDS_LIST)
x = 50
y = 50
vel = 5

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
    draw_map(GRIDS_LIST, 1)
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
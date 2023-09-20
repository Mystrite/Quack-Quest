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

class player:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.vel = 5
        self.direction = "UP"
        self.icons = {
            "UP" : pygame.image.load('./A-Level-NEA-new/assets/Duck_UP.png'),
            "DOWN" : pygame.image.load('./A-Level-NEA-new/assets/Duck_DOWN.png'),
            "LEFT" : pygame.image.load('./A-Level-NEA-new/assets/Duck_LEFT.png'),
            "RIGHT" : pygame.image.load('./A-Level-NEA-new/assets/Duck_RIGHT.png')
        }


    def draw(self,win):
        
        win.blit(self.icons[self.direction], (self.x,self.y))
        

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

conv_tiles_to_classes(GRIDS_LIST)


run = True

pygame.init()

win = pygame.display.set_mode(SCREEN)

player_up = pygame.image.load('./A-Level-NEA-new/assets/Duck_UP.png')
player_down = pygame.image.load('./A-Level-NEA-new/assets/Duck_DOWN.png')
player_left = pygame.image.load('./A-Level-NEA-new/assets/Duck_LEFT.png')
player_right = pygame.image.load('./A-Level-NEA-new/assets/Duck_RIGHT.png')
player_icon = player_up
pygame.display.set_caption("very cool epic game for cool people")


clock = pygame.time.Clock()


def redraw():
    draw_map(GRIDS_LIST, 1)
    duck.draw(win)
    pygame.display.update()

duck = player()

while run:
    clock.tick(45)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        duck.x -= duck.vel
        duck.direction = "LEFT"
        player_icon = player_left
    elif keys[pygame.K_RIGHT]:
        duck.x += duck.vel
        duck.direction = "RIGHT"
        player_icon = player_right
    elif keys[pygame.K_UP]:
        duck.y -= duck.vel
        duck.direction = "UP"
        player_icon = player_up

    elif keys[pygame.K_DOWN]:
        duck.y += duck.vel
        duck.direction = "DOWN"
        player_icon = player_down
    redraw()


pygame.quit()

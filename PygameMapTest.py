import pygame, sys
import WFC_Test_2 as wfc


pygame.init()
GRIDS_LIST = wfc.generate()
dispInfObj = pygame.display.Info()
SWIDTH = dispInfObj.current_w
SHEIGHT = dispInfObj.current_h
SCREEN = (SWIDTH, SHEIGHT)
SMAP = (SWIDTH, SHEIGHT*0.8) 
STILES = (SWIDTH//wfc.SIZE_X, SWIDTH//wfc.SIZE_X)

fonts = {
    "comicsans_small" : pygame.font.SysFont("comicsansms", 45),
    "menubutton" : pygame.font.SysFont("aaa", 3)
}

button_icons = {
    "green_forward" : pygame.image.load('./A-Level-NEA-new/assets/GreenArrow.png')
}

tile_icons = [None] * len(wfc.TILE_ID)
for id in range(len(wfc.TILE_ID)):
    tile_icons[id] =  pygame.image.load('./A-Level-NEA-new/assets/TILE_%s_placeholder.png' % id)

win = pygame.display.set_mode(SCREEN)

pygame.display.set_caption("very cool epic game for cool people")

clock = pygame.time.Clock()

def drawtext(text, font, colour, screen, x, y):
    object = font.render(text, 1, colour)
    textrect = object.get_rect()
    textrect.topleft = (x, y)
    screen.blit(object, textrect)

class  centrebutton:
    def __init__(self, width, height, y):
        self.width = width
        self.height = height
        self.x = (SWIDTH-self.width)//2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def filltext(self, text, font, colour, win):
        pygame.draw.rect(win, (255,0,0), self.rect)
        drawtext(text, font, colour, win, self.x+self.width*0.5-(len(text)*12), (self.y)+self.height//5)
    
    
class inputbox(centrebutton):
    def filltext(self, text, font, colour, win):
        pygame.draw.rect(win, (255,0,0), self.rect)
        drawtext(text, font, colour, win, self.x+30, (self.y)+self.height//5)

class clickablebutton:
    def __init__(self, x, y, size, icon): # unfinished!!
        self.x = x
        self.y = y
        self.size = size
        self.icon = pygame.transform.scale(icon, self.size) 
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self):
        win.blit(self.icon, (self.x, self.y))
    
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
        win.blit(pygame.transform.scale(self.icons[self.direction], STILES), (self.x,self.y))
        

def conv_tiles_to_classes(maplist):
    start_y = SHEIGHT*0.2
    offsetx = SWIDTH/wfc.SIZE_X
    offsety = offsetx
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

def redraw():
    draw_map(GRIDS_LIST, 1)
    duck.draw(win)
    pygame.display.update()

def main_menu():
    clock.tick(15)
    running = True
    
    while running:
        mx, my = pygame.mouse.get_pos()

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        win.fill((0,190,255))
        drawtext("Quack Quest", fonts["comicsans_small"], (255,255,255), win, SWIDTH*0.5, SHEIGHT*0.1)
        start_button = centrebutton(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.45)
        leader_button = centrebutton(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.65)
        
        if start_button.rect.collidepoint((mx, my)):
            if click:
                name_select()
        if leader_button.rect.collidepoint((mx, my)):
            if click:
                leaderboard()

        start_button.filltext("Start Game", fonts["comicsans_small"], (255,255,255), win)
        leader_button.filltext("Leaderboard", fonts["comicsans_small"], (255,255,255), win)
        pygame.display.update()

def name_select():
    running = True
    clock.tick(60)
    name = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) <= 15:
                    name += event.unicode

        box = inputbox(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.45)
        box.filltext(name, fonts["comicsans_small"], (255,255,255), win)
        progress_button = clickablebutton((box.x + box.width + 25), box.y , (box.height, box.height), button_icons["green_forward"])
        progress_button.draw()
        pygame.display.flip()

def leaderboard():
    print("leaderboarding!")

duck = player()

def dungeon():
    clock.tick(30)
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            duck.x -= duck.vel
            duck.direction = "LEFT"
        elif keys[pygame.K_RIGHT]:
            duck.x += duck.vel
            duck.direction = "RIGHT"
        elif keys[pygame.K_UP]:
            duck.y -= duck.vel
            duck.direction = "UP"

        elif keys[pygame.K_DOWN]:
            duck.y += duck.vel
            duck.direction = "DOWN"
        redraw()

if __name__ == "__main__":
    main_menu()

pygame.quit()

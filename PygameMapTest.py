import pygame, sys
import random
import WFC_Test_2 as wfc
import re
import time


pygame.init()
GRIDS_LIST, NUM_MAPS = wfc.generate()
dispInfObj = pygame.display.Info()
SWIDTH = dispInfObj.current_w
SHEIGHT = dispInfObj.current_h
SCREEN = (SWIDTH, SHEIGHT)
STILES = (SWIDTH//wfc.SIZE_X, SWIDTH//wfc.SIZE_X)

fontlist = pygame.font.get_fonts()

fonts = {
    "menubutton" : pygame.font.SysFont("ebrima", 45),
    "chambercard" : pygame.font.SysFont("algerian", 100)
}

button_icons = {
    "green_forward" : pygame.image.load('./A-Level-NEA-new/assets/GreenArrow.png'),
    "grey_forward"  : pygame.image.load('./A-Level-NEA-new/assets/GreyedGreenArrow.png')
}

TILE_TYPES = {
    "destruction" : 0, 
    "hurt" : 1,
    "impass" : 2,    
    "heal" : 3,
    "exit" : 4
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
    def __init__(self, x, y, size, icon): 
        self.x = x
        self.y = y
        self.size = size
        self.icon = pygame.transform.scale(icon, self.size) 
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self):
        self.icon = pygame.transform.scale(self.icon, self.size) 
        win.blit(self.icon, (self.x, self.y))
    
class tile:     # switch tile classes to inheritance??
    def __init__(self, x, y, ID):
        self.ID = ID
        self.x = x
        self.y = y
        self.size = STILES
        self.image = pygame.transform.scale(tile_icons[self.ID], self.size) 
        self.collbox = pygame.Rect(self.x, self.y, self.size[0], self.size[1]) # could only create for specified types.

class tilelist:
    def __init__(self):
        self.tile = None
        self.next = None

class player:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.vel = 2
        self.health = 100
        self.direction = "UP"
        self.icons = {
            "UP" : pygame.image.load('./A-Level-NEA-new/assets/Duck_UP.png'),
            "DOWN" : pygame.image.load('./A-Level-NEA-new/assets/Duck_DOWN.png'),
            "LEFT" : pygame.image.load('./A-Level-NEA-new/assets/Duck_LEFT.png'),
            "RIGHT" : pygame.image.load('./A-Level-NEA-new/assets/Duck_RIGHT.png')
        }
        self.rect = pygame.Rect(self.x+STILES[0]//4, self.y+STILES[0]//4, STILES[0]//2, STILES[1]//2)

    def checkcollide(self, tiletype):
        temp = tiletype
        while temp != None:
            docollide = self.rect.colliderect(temp.tile.collbox)
            if docollide:
                return docollide
            temp = temp.next
        return False

    def move(self, newdir, col_list):
        self.direction = newdir
        if self.direction == "UP":
            self.y -= self.vel
            self.rect = pygame.Rect.move(self.rect, 0, -self.vel)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.y += self.vel
                self.rect = pygame.Rect.move(self.rect, 0, self.vel)

        elif self.direction == "DOWN":
            self.y += self.vel
            self.rect = pygame.Rect.move(self.rect, 0, self.vel) 
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.y -= self.vel
                self.rect = pygame.Rect.move(self.rect, 0, -self.vel) 

        elif self.direction == "LEFT":
            self.x -= self.vel
            self.rect = pygame.Rect.move(self.rect, -self.vel, 0)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.x += self.vel
                self.rect = pygame.Rect.move(self.rect, self.vel, 0) 
            
        elif self.direction == "RIGHT":
            self.x += self.vel
            self.rect = pygame.Rect.move(self.rect, self.vel, 0)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.x -= self.vel
                self.rect = pygame.Rect.move(self.rect, -self.vel, 0) 


    def draw(self):
        win.blit(pygame.transform.scale(self.icons[self.direction], STILES), (self.x,self.y))
        # pygame.draw.rect(win, (255,0,0), self.rect) # DEBUG - DUCK HITBOX



def addtolist(head, new):
    if head == None:
        return new
    new.next = head
    return new

def outlist(head):
    temp = head
    while temp != None:
        print(temp.tile.ID, temp.tile.x, temp.tile.y, temp.tile.collbox)
        temp = temp.next
        
def conv_tiles_to_classes(map):
    start_y = SHEIGHT - SWIDTH//wfc.SIZE_X *wfc.SIZE_Y
    offsetx = SWIDTH/wfc.SIZE_X
    offsety = offsetx
    collisionslist = [None]*len(TILE_TYPES)
    for y in range(wfc.SIZE_Y):
        for x in range(wfc.SIZE_X): 
            newtile = tile(x*offsetx,start_y+(y*offsety),map[y][x])
            map[y][x] = newtile
            if newtile.ID == wfc.TILE_ID["O_WALL"] or newtile.ID == wfc.TILE_ID["VOID"] or newtile.ID == wfc.TILE_ID["ENTER"]:
                newitem = tilelist()
                newitem.tile = newtile
                if newtile.ID == wfc.TILE_ID["ENTER"]:
                    newtile.collbox = pygame.Rect.move(newtile.collbox, 0, STILES[1])
                    print(newtile.collbox)
                collisionslist[TILE_TYPES["impass"]] = addtolist(collisionslist[TILE_TYPES["impass"]], newitem)
            elif newtile.ID == wfc.TILE_ID["HOLY"]:
                newitem = tilelist()
                newitem.tile = newtile
                collisionslist[TILE_TYPES["heal"]] = addtolist(collisionslist[TILE_TYPES["heal"]], newitem)
            elif newtile.ID == wfc.TILE_ID["ROCK"]:
                newitem = tilelist()
                newitem.tile = newtile
                collisionslist[TILE_TYPES["destruction"]] = addtolist(collisionslist[TILE_TYPES["destruction"]], newitem)
            elif newtile.ID == wfc.TILE_ID["LAVA"]:
                newitem = tilelist()
                newitem.tile = newtile
                collisionslist[TILE_TYPES["hurt"]] = addtolist(collisionslist[TILE_TYPES["hurt"]], newitem)
            elif newtile.ID == wfc.TILE_ID["EXIT"]:
                newitem = tilelist()
                newtile.collbox = pygame.Rect.move(newtile.collbox, 0, -newtile.size[1]*0.9)
                newitem.tile = newtile
                collisionslist[TILE_TYPES["exit"]] = addtolist(collisionslist[TILE_TYPES["exit"]], newitem)

    return collisionslist 

def draw_map(maplist, mapnum):
        map = maplist[mapnum]
        for x in range(wfc.SIZE_X):
            for y in range(wfc.SIZE_Y):
                win.blit(map[y][x].image, (map[y][x].x,map[y][x].y))
                #if map[y][x].ID == wfc.TILE_ID["O_WALL"] or map[y][x].ID == wfc.TILE_ID["VOID"] : # DEBUG - impass hitbox
                #   pygame.draw.rect(win, (255,0,0), map[y][x].collbox)

def redraw(map_list, map_num, duck):
    draw_map(map_list, map_num)
    duck.draw()
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
        drawtext("Quack Quest", fonts["menubutton"], (255,255,255), win, SWIDTH*0.5, SHEIGHT*0.1)
        start_button = centrebutton(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.45)
        leader_button = centrebutton(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.65)
        
        if start_button.rect.collidepoint((mx, my)):
            if click:
                name_select()
        if leader_button.rect.collidepoint((mx, my)):
            if click:
                leaderboard()

        start_button.filltext("Start Game", fonts["menubutton"], (255,255,255), win)
        leader_button.filltext("Leaderboard", fonts["menubutton"], (255,255,255), win)
        pygame.display.update()

def name_select():
    running = True
    clock.tick(60)
    name = ""
    validname = False
    box = inputbox(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.45)
    progress_button = clickablebutton((box.x + box.width + 25), box.y , (box.height, box.height), button_icons["grey_forward"])
    
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

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) <= 15:
                    name += event.unicode

                if re.search("^\w*$", name) and name != "":
                    validname = True
                    progress_button.icon = button_icons["green_forward"]
                else:
                    validname = False
                    progress_button.icon = button_icons["grey_forward"]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if progress_button.rect.collidepoint((mx, my)):
                if click and validname:
                    game()
                elif click:
                    print("invalid")

        box.filltext(name, fonts["menubutton"], (255,255,255), win)
        progress_button.draw()
        pygame.display.flip()

def leaderboard():
    print("leaderboarding!")


def game():
    map_num = 0
    alive = True
    hasWon = False
    progress = False
    newduck = player()
    GRIDS_LIST, NUM_MAPS = wfc.generate()

    while alive == True and hasWon == False:
        win.fill((0,0,0))
        drawtext("Chamber %s" % str(map_num+1), fonts["chambercard"], (255,255,255), win, SWIDTH//2-300,SHEIGHT//2-100)
        pygame.display.update()

        time.sleep(3)
        progress = dungeon(GRIDS_LIST, map_num, newduck)

        if progress == False:
            alive = False
        else:
            map_num += 1

        if map_num > NUM_MAPS:
            hasWon = True


def dungeon(maplist, map_num, duck):
    clock.tick(15)
    run = True
    wfc.outgrid(maplist[map_num], wfc.SIZE_X, wfc.SIZE_Y)
    collist = conv_tiles_to_classes(maplist[map_num])
    for i in range(wfc.SIZE_X):
        if maplist[map_num][wfc.SIZE_Y-1][i].ID == wfc.TILE_ID["ENTER"]:
            duck.x = maplist[map_num][wfc.SIZE_Y-1][i].x
            duck.y = maplist[map_num][wfc.SIZE_Y-1][i].y
            duck.rect = pygame.Rect(duck.x+STILES[0]//4, duck.y+STILES[0]//4, STILES[0]//2, STILES[1]//2)

    while run:
        if duck.health < 0:
            return False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            duck.move("LEFT", collist)

        elif keys[pygame.K_RIGHT]:
            duck.move("RIGHT", collist)
        elif keys[pygame.K_UP]:
            duck.move("UP", collist)
        elif keys[pygame.K_DOWN]:
            duck.move("DOWN", collist)

        if duck.checkcollide(collist[TILE_TYPES["hurt"]]):
            duck.health -= 0.2
            print(duck.health)
        if duck.checkcollide(collist[TILE_TYPES["heal"]]) and duck.health < 100:
            duck.health += 0.15
            print(duck.health)
        if duck.checkcollide(collist[TILE_TYPES["exit"]]):
            return True

        redraw(maplist, map_num, duck)

if __name__ == "__main__":
    main_menu()

pygame.quit()

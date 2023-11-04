import pygame, sys
import random
import WFC_Test_2 as wfc
import re
import time
import os
from math import ceil

curpath = os.getcwd()

pygame.init()
dispInfObj = pygame.display.Info()  # resolution of screen, for debugging purposes
SWIDTH = dispInfObj.current_w   # width of screen
SHEIGHT = dispInfObj.current_h  # height of screen
SCREEN = (SWIDTH, SHEIGHT)  # width and height stored as tuple
STILES = (SWIDTH//wfc.SIZE_X, SWIDTH//wfc.SIZE_X)   # size of tiles tuple

fontlist = pygame.font.get_fonts()

colours = { # dict with reference 
    "red" : (255,0,0),
    "green" : (0,255,0),
    "black" : (0,0,0),
    "white" : (255,255,255),
    "cyan" : (0,190,255)
}

fonts = {   # dict with fonts
    "menubutton" : pygame.font.SysFont("ebrima", 45),
    "chambercard" : pygame.font.SysFont("algerian", 100)
}

button_icons = { # dict with icons for buttons
    "green_forward" : pygame.image.load(curpath+'/assets/GreenArrow.png'),
    "grey_forward"  : pygame.image.load(curpath+'/assets/GreyedGreenArrow.png')
}

misc_assets = { # dict for miscellanious assets
    "background" : pygame.transform.scale(pygame.image.load(curpath+"/assets/background.png"), SCREEN)
    }

TILE_TYPES = {  # IDs for types of tiles (e.g. damage dealing ones)
    "destruction" : 0, 
    "hurt" : 1,
    "impass" : 2,    
    "heal" : 3,
    "exit" : 4
}


tile_icons = [None] * len(wfc.TILE_ID)    
for id in range(len(wfc.TILE_ID)):      # loads tile assets and associates them with the correct ID
    tile_icons[id] =  pygame.image.load(curpath+'/assets/TILE_%s_placeholder.png' % id)

win = pygame.display.set_mode(SCREEN)

pygame.display.set_caption("very cool epic game for cool people")

clock = pygame.time.Clock()

### UTILITIES ###

def addtolist(head, new):
    if head == None:
        return new
    new.next = head
    return new

def removefromlist(head, target):
    if head == target: 
        return head.next
    temp = head
    while temp != None:
        prev = temp
        temp = temp.next
        if temp == target:
            prev.next = temp.next
            return head
    return head

def outlist(head):
    temp = head
    while temp != None:
        print(temp.tile.ID, temp.tile.x, temp.tile.y, temp.tile.collbox)
        temp = temp.next

def drawtext(text, font, colour, screen, x, y): # general func displays text 
    object = font.render(text, 1, colour)
    textrect = object.get_rect()
    textrect.topleft = (x, y)
    screen.blit(object, textrect)

### CLASSES ###

class  centrebutton:    # class defining a rectangle button at the centre of the screen
    def __init__(self, width, height, y):
        self.width = width
        self.height = height
        self.x = (SWIDTH-self.width)//2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def filltext(self, text, font, colour, win):    # fills centrebutton objetc with given text
        pygame.draw.rect(win, colours["red"], self.rect)
        drawtext(text, font, colour, win, self.x+self.width*0.5-(len(text)*12), (self.y)+self.height//5)
    

class inputbox(centrebutton):   # creates a box inwhich player inputted text is displayed
    def filltext(self, text, font, colour, win):
        pygame.draw.rect(win, colours["red"], self.rect)
        drawtext(text, font, colour, win, self.x+30, (self.y)+self.height//5)

class clickablebutton:  # defines a button which can be clicked on
    def __init__(self, x, y, size, icon): 
        self.x = x
        self.y = y
        self.size = size
        self.icon = pygame.transform.scale(icon, self.size) 
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self):
        self.icon = pygame.transform.scale(self.icon, self.size) 
        win.blit(self.icon, (self.x, self.y))
    
class tile:     # defines properties of any given tiles
    def __init__(self, x, y, ID):
        self.ID = ID
        self.x = x
        self.y = y
        self.size = STILES
        self.image = pygame.transform.scale(tile_icons[self.ID], self.size) 
        self.collbox = pygame.Rect(self.x, self.y, self.size[0], self.size[1]) 

class tilelist: # linked list which contains tiles
    def __init__(self):
        self.tile = None
        self.next = None

class projlist:
    def __init__(self):
        self.proj = None
        self.next = None

class entity:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.sVel = 0
        self.size = STILES
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.icon = None
        self.direction = "UP"

    def checkcollide(self, tiletype):
                temp = tiletype
                while temp != None:
                    docollide = self.rect.colliderect(temp.tile.collbox)
                    if docollide:
                        return docollide
                    temp = temp.next
                return False

    def draw(self):
            win.blit(pygame.transform.scale(self.icon, self.size), (self.x,self.y))
            pygame.draw.rect(win, colours["red"], self.rect) # DEBUG - HITBOX

class projectile(entity):
    def __init__(self, vel, direction, size, damage, icon, x, y):
        super().__init__()
        self.x = x 
        self.y = y
        self.vel = vel
        self.icon = None
        self.direction = direction 
        self.damage = damage
        self.icon = icon
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

class sentient(entity):
    def __init__(self):
        super().__init__()
        self.projList = None
        self.projSize = (16,16)
        self.pVel = 5
        self.damage = 10
        self.pIcon = None
        self.attackspeed = 1

    def fire(self):
        newProj = projectile(self.pVel, self.direction, self.projSize, self.damage, self.pIcon, self.x + self.size[0]/2 - self.projSize[0], self.y + self.size[1]/2 - self.projSize[1])
        newItem = projlist()
        newItem.proj = newProj
        self.projList = addtolist(self.projList, newItem)
    
    def checkprojcollide(self, tiletype, projectile):
        temp = tiletype
        while temp != None:
            docollide = projectile.rect.colliderect(temp.tile.collbox)
            if docollide:
                return docollide
            temp = temp.next
        return False

    def moveproj(self, col_list):
        temp = self.projList
        while temp != None: 
            match temp.proj.direction:
                case "UP":
                    temp.proj.y -= temp.proj.vel
                    temp.proj.rect = pygame.Rect.move(temp.proj.rect, 0, -temp.proj.vel) 
                case "DOWN":
                    temp.proj.y += temp.proj.vel
                    temp.proj.rect = pygame.Rect.move(temp.proj.rect, 0, temp.proj.vel)
                case "LEFT":
                    temp.proj.x -= temp.proj.vel
                    temp.proj.rect = pygame.Rect.move(temp.proj.rect, -temp.proj.vel, 0)
                case "RIGHT":
                    temp.proj.x += temp.proj.vel
                    temp.proj.rect = pygame.Rect.move(temp.proj.rect, temp.proj.vel, 0)

            if self.checkprojcollide(col_list[TILE_TYPES["impass"]], temp.proj):
                self.projList = removefromlist(self.projList, temp.proj)
                print("hit!")
            else:
                temp.proj.draw()
            temp = temp.next

    def refresh(self, col_list):
        self.moveproj(col_list)
        self.draw()

class player(sentient):
    def __init__(self):
        super().__init__()
        self.sVel = 1
        self.maxhealth = 1000
        self.health = self.maxhealth
        self.icons = {
            "UP" : pygame.image.load(curpath+'/assets/Duck_UP.png'),
            "DOWN" : pygame.image.load(curpath+'/assets/Duck_DOWN.png'),
            "LEFT" : pygame.image.load(curpath+'/assets/Duck_LEFT.png'),
            "RIGHT" : pygame.image.load(curpath+'/assets/Duck_RIGHT.png')
        }
        self.rect = pygame.Rect(self.x+STILES[0]//4, self.y+STILES[0]//4, STILES[0]//2, STILES[1]//2)
        self.pVel = 15
        self.pIcon = pygame.image.load(curpath+'/assets/Duck_RIGHT.png')

    def move(self, newdir, col_list):
        self.direction = newdir
        if self.direction == "UP":
            self.y -= self.sVel
            self.rect = pygame.Rect.move(self.rect, 0, -self.sVel)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.y += self.sVel
                self.rect = pygame.Rect.move(self.rect, 0, self.sVel)

        elif self.direction == "DOWN":
            self.y += self.sVel
            self.rect = pygame.Rect.move(self.rect, 0, self.sVel) 
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.y -= self.sVel
                self.rect = pygame.Rect.move(self.rect, 0, -self.sVel) 

        elif self.direction == "LEFT":
            self.x -= self.sVel
            self.rect = pygame.Rect.move(self.rect, -self.sVel, 0)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.x += self.sVel
                self.rect = pygame.Rect.move(self.rect, self.sVel, 0) 
            
        elif self.direction == "RIGHT":
            self.x += self.sVel
            self.rect = pygame.Rect.move(self.rect, self.sVel, 0)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]) or self.checkcollide(col_list[TILE_TYPES["destruction"]]):
                self.x -= self.sVel
                self.rect = pygame.Rect.move(self.rect, -self.sVel, 0) 
    
    def draw(self):
        self.icon = self.icons[self.direction]
        super().draw()
        

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
                if map[y][x].ID == wfc.TILE_ID["O_WALL"] or map[y][x].ID == wfc.TILE_ID["VOID"] : # DEBUG - impass hitbox
                   pygame.draw.rect(win, colours["red"], map[y][x].collbox)

def draw_hud(mapnum, duck, start_time):
    pygame.draw.rect(win, colours["black"], pygame.Rect(0,0, SWIDTH, SHEIGHT*0.3))
    drawtext("Chamber %s" % (mapnum+1), fonts["menubutton"], colours["white"], win, 0, 0)
    curtime = round(time.time() - start_time, 2)
    drawtext(str(curtime), fonts["menubutton"], colours["white"], win, 0, SHEIGHT*0.05)

    ratio = duck.health/duck.maxhealth
    pygame.draw.rect(win, colours["red"], (SWIDTH*0.7, SHEIGHT*0.05, SWIDTH*0.25, SHEIGHT*0.05))
    pygame.draw.rect(win, colours["green"], (SWIDTH*0.7, SHEIGHT*0.05, SWIDTH*0.25*ratio, SHEIGHT*0.05))  
    drawtext("%s/%s" % (ceil(duck.health/10), duck.maxhealth//10), fonts["menubutton"], colours["white"], win, SWIDTH*0.7, 0)

def redraw(map_list, map_num, duck, start_time, col_list):
    draw_hud(map_num, duck, start_time)
    draw_map(map_list, map_num)
    duck.refresh(col_list)
    pygame.display.update()

def main_menu():
    clock.tick(15)
    running = True
    win.blit(misc_assets["background"], (0,0))

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
                    

        drawtext("Quack Quest", fonts["menubutton"], colours["white"], win, SWIDTH*0.5, SHEIGHT*0.1)
        start_button = centrebutton(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.45)
        leader_button = centrebutton(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.65)
        
        if start_button.rect.collidepoint((mx, my)):
            if click:
                name_select()
        if leader_button.rect.collidepoint((mx, my)):
            if click:
                leaderboard()

        start_button.filltext("Start Game", fonts["menubutton"], colours["white"], win)
        leader_button.filltext("Leaderboard", fonts["menubutton"], colours["white"], win)
        pygame.display.update()

def name_select():
    running = True
    clock.tick(60)
    name = ""
    validname = False
    box = inputbox(SWIDTH*0.3, SHEIGHT*0.1, SHEIGHT*0.45)
    progress_button = clickablebutton((box.x + box.width + 25), box.y , (box.height, box.height), button_icons["grey_forward"])
    win.blit(misc_assets["background"], (0,0))
    while running:
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if progress_button.rect.collidepoint((mx, my)):
                if click and validname:
                    game()
                elif click:
                    print("invalid")
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) <= 15 and event.key != pygame.K_RETURN:
                    name += event.unicode

                if re.search("^\w*$", name) and name != "":
                    validname = True
                    progress_button.icon = button_icons["green_forward"]
                else:
                    validname = False
                    progress_button.icon = button_icons["grey_forward"]

        box.filltext(name, fonts["menubutton"], colours["white"], win)
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
    win.fill(colours["black"])
    drawtext("Loading...", fonts["chambercard"], (255,255,255), win, SWIDTH//2-300,SHEIGHT//2-100)
    pygame.display.update()
    time.sleep(0.5)
    GRIDS_LIST, NUM_MAPS = wfc.generate()
    start_time = time.time()

    while alive == True and hasWon == False:
        win.fill(colours["black"])
        drawtext("Chamber %s" % str(map_num+1), fonts["chambercard"], (255,255,255), win, SWIDTH//2-300,SHEIGHT//2-100)
        pygame.display.update()

        time.sleep(3)
        progress = dungeon(GRIDS_LIST, map_num, newduck, start_time)

        if progress == False:
            alive = False
        elif map_num+1 == NUM_MAPS:
            hasWon = True
        else:
            map_num += 1
    print("yippe!")

        

def dungeon(maplist, map_num, duck, start_time):
    clock.tick(15)
    run = True
    collist = conv_tiles_to_classes(maplist[map_num])
    prevtime = 0
    for i in range(wfc.SIZE_X):
        if maplist[map_num][wfc.SIZE_Y-1][i].ID == wfc.TILE_ID["ENTER"]:
            duck.x = maplist[map_num][wfc.SIZE_Y-1][i].x
            duck.y = maplist[map_num][wfc.SIZE_Y-1][i].y
            duck.rect = pygame.Rect(duck.x+STILES[0]//4, duck.y+STILES[0]//4, STILES[0]//2, STILES[1]//2)

    while run:
        if duck.health <= 0:
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

        if keys[pygame.K_SPACE]:
            newtime = time.time()
            if newtime-prevtime > duck.attackspeed:
                prevtime = newtime
                duck.fire()

        if duck.checkcollide(collist[TILE_TYPES["hurt"]]):
            duck.health -= 2
        if duck.checkcollide(collist[TILE_TYPES["heal"]]) and duck.health < duck.maxhealth:
            duck.health += 1
        if duck.checkcollide(collist[TILE_TYPES["exit"]]):
            return True

        redraw(maplist, map_num, duck, start_time,collist)

if __name__ == "__main__":
    main_menu()

pygame.quit()

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
S_WIDTH = dispInfObj.current_w   # width of screen
S_HEIGHT = dispInfObj.current_h  # height of screen
SCREEN = (S_WIDTH, S_HEIGHT)  # width and height stored as tuple
STILES = (S_WIDTH//wfc.SIZE_X, S_WIDTH//wfc.SIZE_X)   # size of tiles tuple

clock = pygame.time.Clock()
clock.tick(60)

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
    "grey_forward"  : pygame.image.load(curpath+'/assets/GreyedGreenArrow.png'),
    "base_rect" : pygame.image.load(curpath+'/assets/button_back.png')
    }

misc_assets = { # dict for miscellanious assets
    "background" : pygame.transform.scale(pygame.image.load(curpath+"/assets/background.png"), SCREEN),
    "chamber_card" : pygame.transform.scale(pygame.image.load(curpath+"/assets/card_background.png"), SCREEN),
    "hearts" : pygame.image.load(curpath+"/assets/health.png"),
    "logo": pygame.image.load(curpath+"/assets/logo.png") 
    }

TILE_TYPES = {  # IDs for types of tiles (e.g. damage dealing ones)
    "hurt" : 0,
    "impass" : 1,    
    "heal" : 2,
    "exit" : 3,
    "summon" : 4
}


tile_icons = [None] * len(wfc.TILE_ID)    
for id in range(len(wfc.TILE_ID)):      # loads tile assets and associates them with the correct ID
    tile_icons[id] =  pygame.image.load(curpath+'/assets/TILE_%s.png' % id)

win = pygame.display.set_mode(SCREEN)

pygame.display.set_caption("Quack Quest")

pygame.mixer.music.load(curpath+"/assets/bgm.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

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
        print(temp.tile.ID, temp.tile.x, temp.tile.y, temp.tile.rect)
        temp = temp.next

def drawtext(text, font, colour, screen, x, y): # general func displays text 
    object = font.render(text, 1, colour)
    textrect = object.get_rect()
    textrect.topleft = (x, y)
    screen.blit(object, textrect)

### CLASSES ###

class score_record:
    def __init__(self, name, score, time):
        self.name = name
        self.score = score
        self.time = time

class  centrebutton:    # class defining a rectangle button at the centre of the screen
    def __init__(self, width, height, y):
        self.width = width
        self.height = height
        self.x = (S_WIDTH-self.width)//2
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.image = button_icons["base_rect"]
        self.text = "Enter Name"

    def filltext(self, text, font, colour, win):    # fills centrebutton objetc with given text
        win.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
        drawtext(text, font, colour, win, self.x+self.width*0.5-(len(text)*12), (self.y)+self.height//5)
    

class inputbox(centrebutton):   # creates a box inwhich player inputted text is displayed
    def filltext(self, text, font, colour, win):
        if self.text != "Enter Name" or text != "":
            self.text = text
        win.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x, self.y))
        drawtext(self.text, font, colour, win, self.x+30, (self.y)+self.height//5)

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
    
class tile(pygame.sprite.Sprite):     # defines properties of any given tiles
    def __init__(self, x, y, ID):
        super().__init__()
        self.ID = ID
        self.x = x
        self.y = y
        self.size = STILES
        self.image = pygame.transform.scale(tile_icons[self.ID], self.size) 
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1]) 


class entity(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.sVel = 0
        self.size = STILES
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.icon = None
        self.direction = "UP"

    def checkcollide(self, tiletype):
        for tile in tiletype:
            docollide = self.rect.colliderect(tile.rect)
            if docollide:
                return docollide, tile
        return False

    def draw(self):
            win.blit(pygame.transform.scale(self.icon, self.size), (self.x,self.y))
            #pygame.draw.rect(win, colours["red"], self.rect) # DEBUG - HITBOX

class projectile(entity):
    def __init__(self, vel, direction, size, damage, icon, x, y):
        super().__init__()
        self.x = x 
        self.y = y
        self.vel = vel
        self.direction = direction 
        self.damage = damage
        self.icon = icon
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

class sentient(entity):
    def __init__(self):
        super().__init__()
        self.maxhealth = 100
        self.health = self.maxhealth
        self.projList = pygame.sprite.Group()
        self.projSize = (16,16)
        self.pVel = 5
        self.damage = 10
        self.pIcon = pygame.image.load(curpath+'/assets/projectile.png')
        self.attackspeed = 1
        self.count = 0
        self.breaks = 0
        self.animation_cycle = 0.5
        self.last_anim = 0

    def change_hp(self, change):
        if self.health <= self.maxhealth:
            self.health += change
            if self.health > self.maxhealth: 
                self.health = self.maxhealth


    def fire(self):
        newProj = projectile(self.pVel, self.direction, self.projSize, self.damage, self.pIcon, self.x + self.size[0]/2 - self.projSize[0]/2, self.y + self.size[1]/2 - self.projSize[1]/2)
        self.projList.add(newProj)
    
    def checkprojcollide(self, tiletype, projectile):
        docollide = False
        for tile in tiletype:
            docollide = projectile.rect.colliderect(tile.rect)
            if docollide:
                return docollide, tile
        return docollide, None

    def move(self, newdir, col_list):
        self.direction = newdir
        new_move_time = time.time()
        if new_move_time - self.last_anim >= self.animation_cycle:
            self.count += 1
            self.last_anim = new_move_time

        if self.direction == "UP":
            self.y -= self.sVel
            self.rect = pygame.Rect.move(self.rect, 0, -self.sVel)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]):
                self.y += self.sVel
                self.rect = pygame.Rect.move(self.rect, 0, self.sVel)

        elif self.direction == "DOWN":
            self.y += self.sVel
            self.rect = pygame.Rect.move(self.rect, 0, self.sVel) 
            if self.checkcollide(col_list[TILE_TYPES["impass"]]):
                self.y -= self.sVel
                self.rect = pygame.Rect.move(self.rect, 0, -self.sVel) 

        elif self.direction == "LEFT":
            self.x -= self.sVel
            self.rect = pygame.Rect.move(self.rect, -self.sVel, 0)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]):
                self.x += self.sVel
                self.rect = pygame.Rect.move(self.rect, self.sVel, 0) 
            
        elif self.direction == "RIGHT":
            self.x += self.sVel
            self.rect = pygame.Rect.move(self.rect, self.sVel, 0)
            if self.checkcollide(col_list[TILE_TYPES["impass"]]):
                self.x -= self.sVel
                self.rect = pygame.Rect.move(self.rect, -self.sVel, 0) 

    def moveproj(self, col_list):
        for entity in self.projList:
            match entity.direction:
                case "UP":
                    entity.y -= entity.vel
                    entity.rect = pygame.Rect.move(entity.rect, 0, -entity.vel) 
                case "DOWN":
                    entity.y += entity.vel
                    entity.rect = pygame.Rect.move(entity.rect, 0, entity.vel)
                case "LEFT":
                    entity.x -= entity.vel
                    entity.rect = pygame.Rect.move(entity.rect, -entity.vel, 0)
                case "RIGHT":
                    entity.x += entity.vel
                    entity.rect = pygame.Rect.move(entity.rect, entity.vel, 0)

            hascollided, hittile = self.checkprojcollide(col_list[TILE_TYPES["impass"]], entity)
            entity.draw()

            if hascollided:
                entity.kill()
                if hittile.ID == wfc.TILE_ID["ROCK"]:
                    hittile.remove(col_list[TILE_TYPES["impass"]])
                    hittile.ID = wfc.TILE_ID["FLOOR"]
                    hittile.image = pygame.transform.scale(tile_icons[hittile.ID], hittile.size)
                    self.breaks += 1

    def refresh(self, col_list):
        self.moveproj(col_list)
        self.draw()

class enemy(sentient):
    def __init__(self):
        super().__init__()
        self.time_since_last_attack = 0
        self.path_update_time = 1
        self.time_since_last_path = 0

    def pathfind(self, duck_x, duck_y):
        diff_x = duck_x - self.x 
        diff_y = duck_y - self.y - 100
        if abs(diff_x) > abs(diff_y):
            if diff_x > 0:
                self.direction = "RIGHT"
            else:
                self.direction = "LEFT"
        else:
            if diff_y > 0:
                self.direction = "DOWN"
            else:
                self.direction = "UP"

    def do_hits(self, duck):
        collided, hit_proj = self.checkprojcollide(duck.projList, self)
        if collided:
            hit_proj.kill()
            self.change_hp(-duck.damage)
            if self.health <= 0:
                self.kill()
                duck.slays += 1
                duck.slays_in_chamber += 1

    def refresh(self, col_list, duck):
        self.do_hits(duck)
        self.moveproj(col_list)
        self.move(self.direction, col_list)
        firetime = time.time()
        path_time = time.time()

    
        if path_time - self.time_since_last_path >= self.path_update_time:
            self.time_since_last_path = path_time
            self.pathfind(duck.x, duck.y)

        if firetime - self.time_since_last_attack >= self.attackspeed:
                    self.time_since_last_attack = firetime
                    self.fire()

        self.icon = self.icons[self.direction][self.count % 2]
        self.draw()

class spider(enemy):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x+self.size[0]//4, self.y+self.size[1]//4, self.size[0]//2, self.size[1]//2)
        self.icons = {
            "UP" : [pygame.image.load(curpath+'/assets/spider_UP_1.png'), pygame.image.load(curpath+'/assets/spider_UP_2.png')],
            "DOWN" : [pygame.image.load(curpath+'/assets/spider_DOWN_1.png'), pygame.image.load(curpath+'/assets/spider_DOWN_2.png')],
            "LEFT" : [pygame.image.load(curpath+'/assets/spider_LEFT_1.png'), pygame.image.load(curpath+'/assets/spider_LEFT_2.png')],
            "RIGHT" : [pygame.image.load(curpath+'/assets/spider_RIGHT_1.png'), pygame.image.load(curpath+'/assets/spider_RIGHT_2.png')]
        }
        self.attackspeed = 1
        self.pVel = 15
        self.sVel = 2
        self.damage = 50
        self.health = 25
        self.animation_cycle = 0.25

class player(sentient):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.sVel = 5
        self.maxhealth = 1000
        self.health = self.maxhealth
        self.icons = {
            "UP" : [pygame.image.load(curpath+'/assets/Duck_UP_1.png'), pygame.image.load(curpath+'/assets/Duck_UP_2.png')],
            "DOWN" : [pygame.image.load(curpath+'/assets/Duck_DOWN_1.png'), pygame.image.load(curpath+'/assets/Duck_DOWN_2.png')],
            "LEFT" : [pygame.image.load(curpath+'/assets/Duck_LEFT_1.png'), pygame.image.load(curpath+'/assets/Duck_LEFT_2.png')],
            "RIGHT" : [pygame.image.load(curpath+'/assets/Duck_RIGHT_1.png'), pygame.image.load(curpath+'/assets/Duck_RIGHT_2.png')]
        }
        self.rect = pygame.Rect(self.x+self.size[0]//4, self.y+self.size[0]//4, self.size[1]//2, self.size[1]//2)
        self.pVel = 10
        self.pIcon = pygame.image.load(curpath+'/assets/projectile.png')
        self.attackspeed = 0.5
        self.slays = 0
        self.animation_cycle = 0.25

    def do_hits(self, enemy):
        collided, hit_proj = self.checkprojcollide(enemy.projList, self)
        if collided:
            hit_proj.kill()
            self.change_hp(-enemy.damage)

    def refresh(self, col_list, enemies):
        for enemy in enemies:
            self.do_hits(enemy)

        self.icon = self.icons[self.direction][self.count % 2]
        super().refresh(col_list)

def conv_tiles_to_classes(map):
    start_y = S_HEIGHT - S_WIDTH//wfc.SIZE_X *wfc.SIZE_Y
    offsetx = S_WIDTH/wfc.SIZE_X
    offsety = offsetx
    collisionslist = [None] * len(TILE_TYPES)

    for i in range(len(TILE_TYPES)):
        collisionslist[i] = pygame.sprite.Group()
    all_tiles = pygame.sprite.Group()
   
    for y in range(wfc.SIZE_Y):
        for x in range(wfc.SIZE_X): 
            newtile = tile(x*offsetx,start_y+(y*offsety),map[y][x])
            map[y][x] = newtile
            if newtile.ID == wfc.TILE_ID["O_WALL"] or newtile.ID == wfc.TILE_ID["VOID"] or newtile.ID == wfc.TILE_ID["ENTER"] or newtile.ID == wfc.TILE_ID["ROCK"]:
                if newtile.ID == wfc.TILE_ID["ENTER"]:
                    newtile.rect = pygame.Rect.move(newtile.rect, 0, STILES[1])
                collisionslist[TILE_TYPES["impass"]].add(newtile)

            elif newtile.ID == wfc.TILE_ID["HOLY"]:
                collisionslist[TILE_TYPES["heal"]].add(newtile)

            elif newtile.ID == wfc.TILE_ID["LAVA"]:
                collisionslist[TILE_TYPES["hurt"]].add(newtile)

            elif newtile.ID == wfc.TILE_ID["EXIT"]:
                newtile.rect = pygame.Rect.move(newtile.rect, 0, -newtile.size[1]*0.8)
                collisionslist[TILE_TYPES["exit"]].add(newtile)

            elif newtile.ID == wfc.TILE_ID["SPAWNER"]:
                collisionslist[TILE_TYPES["summon"]].add(newtile)
            all_tiles.add(newtile)

    return collisionslist, all_tiles

def read_from_csv(file_path, num_lines):
    f = open(file_path, "r")
    data = []

    if num_lines == -1:
        list_info = f.read().split("\n")
    else:
        list_info = [None] * num_lines
        for i in range(num_lines):
            list_info[i] = f.readline()

    for i in range(len(list_info)):
        record_items = list_info[i].split(",")
        new_record = score_record(record_items[0], record_items[1], record_items[2])
        data.append(new_record)

    f.close()
    return data

def write_to_csv(file_path, record):
    with open(file_path, "a") as f:
        info = record.name+","+str(record.score)+","+str(record.time)+"\n"

        f.write(info)


def generate_enemy(enemy_group, spawners):
    selection = random.randint(0, 0)
    num_of_spawners = len(spawners.sprites())
    if num_of_spawners == 0:
        return

    spawner_num = random.randint(0, num_of_spawners - 1)
    count = 0

    for selected_spawner in spawners:
       if count == spawner_num:
           spawner = selected_spawner
           break
       count += 1

    match selection:
        case 0:
            new_enemy = spider(spawner.x, spawner.y)
        case _:
            print("failed")

    enemy_group.add(new_enemy)

def draw_map(maplist, mapnum):
    map = maplist[mapnum]
    for x in range(wfc.SIZE_X):
        for y in range(wfc.SIZE_Y):
            win.blit(map[y][x].image, (map[y][x].x,map[y][x].y))
            #if map[y][x].ID == wfc.TILE_ID["O_WALL"] or map[y][x].ID == wfc.TILE_ID["VOID"] : # DEBUG - impass hitbox
                #pygame.draw.rect(win, colours["red"], map[y][x].rect)

def draw_hud(mapnum, duck, start_time, cur_enemies, max_enemies):
    pygame.draw.rect(win, colours["black"], pygame.Rect(0,0, S_WIDTH, S_HEIGHT*0.3))    # fill in background of HUD with black

    win.blit(pygame.transform.scale(misc_assets["chamber_card"], (0.15*S_WIDTH, 0.112*S_HEIGHT)), (0,0))    # draw background of chamber+time UI
    drawtext("Chamber: %s" % (mapnum+1), fonts["menubutton"], colours["white"], win, 15, 2)     # write chamber number

    curtime = round(time.time() - start_time, 2)
    drawtext("Time: %s" % curtime, fonts["menubutton"], colours["white"], win, 15, S_HEIGHT*0.05)   # write current time

    ratio = duck.health/duck.maxhealth      
    pygame.draw.rect(win, colours["black"], (S_WIDTH*0.7, 0, S_WIDTH*0.3, S_HEIGHT))    # draw black background to health display
    pygame.draw.rect(win, colours["red"], (S_WIDTH*0.7, 0, S_WIDTH*0.3*ratio, S_HEIGHT))    # draw red overlay to health display
    win.blit(pygame.transform.scale(misc_assets["hearts"], (S_WIDTH*0.3, S_HEIGHT*0.112)), (S_WIDTH*0.7,0))     # draw transparent heart asset 

    win.blit(pygame.transform.scale(misc_assets["chamber_card"], (0.2*S_WIDTH, 0.112*S_HEIGHT)), (S_WIDTH*0.15,0))      # draw background to enemies slain UI element
    drawtext("%s/%s enemies slain" % (duck.slays_in_chamber, max_enemies), fonts["menubutton"], colours["white"], win, S_WIDTH*0.16, S_HEIGHT*0.015)    # draw number of enemies slain

def update_enemies(enemies, duck, col_list):
    for entity in enemies:
        entity.refresh(col_list, duck)

def redraw(map_list, map_num, duck, start_time, col_list, all_tiles, enemies, cur_enemies, max_enemies):
    draw_hud(map_num, duck, start_time, cur_enemies, max_enemies)
    draw_map(map_list, map_num)
    update_enemies(enemies, duck, col_list)
    duck.refresh(col_list, enemies)
    pygame.display.flip()

def main_menu():
    while True:
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        start_button = centrebutton(S_WIDTH*0.3, S_HEIGHT*0.1, S_HEIGHT*0.45)
        leader_button = centrebutton(S_WIDTH*0.3, S_HEIGHT*0.1, S_HEIGHT*0.65)
        
        if start_button.rect.collidepoint((mx, my)):
            if click:
                name_select()
        if leader_button.rect.collidepoint((mx, my)):
            if click:
                leaderboard()

        win.blit(misc_assets["background"], (0,0))
        win.blit(pygame.transform.scale_by(misc_assets["logo"], 2.5), (S_WIDTH*0.375, S_HEIGHT*0.075))
        start_button.filltext("Start Game", fonts["menubutton"], colours["white"], win)
        leader_button.filltext("Leaderboard", fonts["menubutton"], colours["white"], win)
        pygame.display.update()

def name_select():
    running = True
    name = ""
    validname = False
    box = inputbox(S_WIDTH*0.3, S_HEIGHT*0.1, S_HEIGHT*0.45)
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
                    running = game(name)
                    
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
    top_n = 3
    top_players = read_from_csv(curpath+"/board.csv", top_n)
    running = True
    win.blit(misc_assets["background"], (0,0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        for i in range(top_n):
            drawtext(top_players[i].name, fonts["menubutton"], colours["white"], win, S_WIDTH*0.35, 50+50*i)
        pygame.display.flip()

def game(name):
    map_num = 0
    alive = True
    hasWon = False
    progress = False
    newduck = player()
    newduck.name = name
    win.fill(colours["black"])
    drawtext("Loading...", fonts["chambercard"], (255,255,255), win, S_WIDTH//2-300,S_HEIGHT//2-100)
    pygame.display.update()
    time.sleep(0.5)
    GRIDS_LIST, NUM_MAPS = wfc.generate()
    start_time = time.time()

    while alive == True and hasWon == False:
        win.blit(misc_assets["chamber_card"], (0,0))
        drawtext("Chamber %s" % str(map_num+1), fonts["chambercard"], (255,255,255), win, S_WIDTH//2-300,S_HEIGHT//2-100)
        pygame.display.update()

        time.sleep(3)
        progress = dungeon(GRIDS_LIST, map_num, newduck, start_time)

        if progress == False:
            alive = False
        elif map_num+1 == NUM_MAPS:
            hasWon = True
        else:
            map_num += 1

    if hasWon:
        final_time = time.time() - start_time
        victory(newduck, final_time)

    return False
    

def dungeon(maplist, map_num, duck, start_time):
    run = True
    collist, all_tiles = conv_tiles_to_classes(maplist[map_num])
    prevtime = 0
    cur_enemies = 0
    enemies = pygame.sprite.Group()
    count = 0
    duck.slays_in_chamber = 0

    if len(collist[TILE_TYPES["summon"]].sprites()) == 0:
        max_enemies = 0
    else:
        max_enemies = random.randint(2, 4) + map_num

    for tile in all_tiles:
        if tile.ID == wfc.TILE_ID["ENTER"]:
            duck.x = tile.x
            duck.y = tile.y
            duck.rect = pygame.Rect(duck.x+duck.size[0]//4, duck.y+duck.size[1]//4, duck.size[0]//2, duck.size[1]//2)


    while run:
        if duck.health <= 0:
            return False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

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
            if newtime-prevtime >= duck.attackspeed:
                prevtime = newtime
                duck.fire()

        if duck.checkcollide(collist[TILE_TYPES["hurt"]]):  
            duck.change_hp(-6)  # LAVA DAMAGE
        if duck.checkcollide(collist[TILE_TYPES["heal"]]):
            duck.change_hp(3)  # WATER HEALING
        if duck.checkcollide(collist[TILE_TYPES["exit"]]):
            return True

        if count % 25 == 0 and random.randint(0,5) == 3 and cur_enemies < max_enemies:  # spawn enemy
            generate_enemy(enemies, collist[TILE_TYPES["summon"]])
            cur_enemies += 1

        count += 1
        redraw(maplist, map_num, duck, start_time, collist, all_tiles, enemies, cur_enemies, max_enemies)

def victory(duck, final_time): 
    slay_points = duck.slays * 50 + 1000
    break_points = duck.breaks * 5 + 250
    time_points = 1000*(2.71**-(final_time/100) + 1)
    sum_points = slay_points + break_points + round(time_points)
    
    new_record = score_record(duck.name, sum_points, final_time)
    write_to_csv(curpath+"/board.csv", new_record)
    
if __name__ == "__main__":
    main_menu()

pygame.quit()

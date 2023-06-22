import pygame

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True

pygame.init()

win = pygame.display.set_mode((1440, 720))
player_icon = pygame.image.load('./A-Level-NEA-new/assets/PLAYER_placeholder.png')
bg = pygame.image.load('./A-Level-NEA-new/assets/BACKGROUND_placeholder.png')
pygame.display.set_caption("very cool epic game for cool people")

def redraw():
    win.blit(bg, (0,0))
    pygame.display.update()

while run:
    pygame.time.delay(100)
    
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

    win.fill((255, 255, 255))
    pygame.draw.rect(win, (255,0,0), (x, y, width, height))
    redraw()


pygame.quit()
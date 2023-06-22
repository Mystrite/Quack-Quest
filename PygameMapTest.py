import pygame

SWIDTH = 1440
SHEIGHT = 720
SCREEN = (SWIDTH, SHEIGHT)

x = 50
y = 50
vel = 15

run = True

pygame.init()

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

    win.fill((255, 255, 255))
    redraw()


pygame.quit()
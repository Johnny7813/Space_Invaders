import pygame
import itertools
from actor import Actor, Enemy, Laser




# initialise pygame
pygame.init()

# create the game window
screen = pygame.display.set_mode((800,600))
# x goes from left 0  to right 800, but y goes from top 0 to bottom 600

# set window title
pygame.display.set_caption("Space Invaders")
# set window icon
# see flaticon.com  spaceship 32x32,  arcade space 64x64
icon = pygame.image.load("images/ufo.png")
pygame.display.set_icon(icon)

# a pressed key is repeated
pygame.key.set_repeat(1, 20)

# load a background image
background = pygame.image.load("images/background.png")

# player icon
player = Actor("images/player.png", screen, 200, 480, changeX=5, changeY=5)
laser  = Laser("images/laser.png", screen, 200, 480, changeX=0, changeY=4)

# score
score_value = 0
score_font  = pygame.font.Font('freesansbold.ttf', 32)

# array of enemies
enemies = []
for i in range(8):
    enemy = Enemy("images/enemy.png", screen, 20+i*80, 80, changeX=2, changeY=40)
    enemies.append(enemy)
    enemy = Enemy("images/enemy.png", screen, 20 + i * 80, 150, changeX=2, changeY=40)
    enemies.append(enemy)
    enemy = Enemy("images/enemy.png", screen, 20 + i * 80, 220, changeX=2, changeY=40)
    enemies.append(enemy)




# array of lasers
lasers = []
for i in range(5):
    laser = Laser("images/laser.png", screen, 200, 480, changeX=0, changeY=4)
    lasers.append(laser)


# main game loop, everything happens in this loop
start_ticks=pygame.time.get_ticks() #starter tick
running = True
while running:
    # background colour in RGB - this will make the background red
    screen.fill((0, 0, 0))
    # add background image
    screen.blit(background, (0,0))
    # display score
    score = score_font.render("Score:"+str(score_value), True, (255,0,0))
    screen.blit(score, (10, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # some key has been pressed
        if event.type == pygame.KEYDOWN:
            #print("a key has been pressed")
            if event.key == pygame.K_LEFT:
                player.moveLeft()
            elif event.key == pygame.K_RIGHT:
                player.moveRight()
            elif event.key == pygame.K_UP:
                player.moveUp()
            elif event.key == pygame.K_DOWN:
                player.moveDown()
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_SPACE:
                end_ticks = pygame.time.get_ticks()  # end tick
                if (end_ticks - start_ticks) < 200:
                    break
                for l in lasers:
                    if not l.active:
                        l.setInitalPos(player)
                        l.setActive(True)
                        start_ticks = pygame.time.get_ticks()  # starter tick
                        break
        if event.type == pygame.KEYUP:
            pass

    for a in enemies+lasers:
        a.move()

    for (e,l) in itertools.product(enemies, lasers):
        if (not e.active) or (not l.active):
            continue
        if e.isCollision(l):
            l.setActive(False)
            e.setActive(False)
            score_value += 1

    for a in enemies+lasers:
        a.draw()

    player.draw()
    pygame.display.update()


# shutdown pygame
pygame.quit()

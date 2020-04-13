import pygame
import time
from pygame import mixer
import itertools
from actor import Player, Enemy, Laser
import level_data




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

# a pressed key is repeated, with 1ms delay and 20ms interval
#pygame.key.set_repeat(5, 20)

# load a background image
background = pygame.image.load("images/background.png")

# initiate player
player = Player("images/player1.png", screen, 200, 480, changeX=8, changeY=0)

# initiate score and pause
score_value = 0
score_font  = pygame.font.Font('freesansbold.ttf', 32)
pause_font  = pygame.font.Font('freesansbold.ttf', 64)
pause_text  = pause_font.render("Pause", True, (250,250,0))

# initiate sound
volume_increment = 0.1
sound_volume = 0.0
mixer.music.load("sound/background.wav")
mixer.music.set_volume(sound_volume)
mixer.music.play(-1)
laser_sound = mixer.Sound("sound/laser.wav")
laser_sound.set_volume(sound_volume)
explosion_sound = mixer.Sound("sound/exp_01.wav")
explosion_sound.set_volume(sound_volume)

# initiate and load level data
level = 0
[enemies, totalEnemies] = level_data.spawn_enemies(screen, level)

# array of lasers
lasers = []
for i in range(5):
    laser = Laser("images/laser.png", screen, 200, 480, changeX=0, changeY=4)
    lasers.append(laser)

enemiesANDlasers = enemies + lasers
# the ticker is used to ensure that only 1 laser shot can be
# fired in a certain interval
start_ticks=pygame.time.get_ticks() #starter tick

# main game loop, everything happens in this loop


running = True
pause   = False
game_over = False
while running:
    # background colour in RGB - this will make the background red
    #screen.fill((0, 0, 0))
    # add background image
    screen.blit(background, (0,0))
    # display score
    score = score_font.render("Score : "+str(score_value), True, (255,0,0))
    screen.blit(score, (10, 10))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # some key has been pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                sound_volume += volume_increment
                if sound_volume > 1.0:
                    sound_volume = 1.0
                mixer.music.set_volume(sound_volume)
                laser_sound.set_volume(sound_volume)
                explosion_sound.set_volume(sound_volume)
            elif event.key == pygame.K_9:
                sound_volume -= volume_increment
                if sound_volume < 0.0:
                    sound_volume = 0.0
                mixer.music.set_volume(sound_volume)
                laser_sound.set_volume(sound_volume)
                explosion_sound.set_volume(sound_volume)
            elif event.key == pygame.K_LEFT:
                player.nextHorizontalMove(-4)
            elif event.key == pygame.K_RIGHT:
                player.nextHorizontalMove(4)
            elif event.key == pygame.K_UP:
                player.nextVerticalMove(-4)
            elif event.key == pygame.K_DOWN:
                player.nextVerticalMove(4)
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_p:
                pause = True
            elif event.key == pygame.K_SPACE:
                end_ticks = pygame.time.get_ticks()  # end tick
                if (end_ticks - start_ticks) < 200:
                    break
                for l in lasers:
                    if not l.active:
                        l.setInitalPos(player)
                        l.setActive(True)
                        start_ticks = pygame.time.get_ticks()  # starter tick
                        laser_sound.play()
                        break
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.nextHorizontalMove(0)
            elif event.key == pygame.K_RIGHT:
                player.nextHorizontalMove(0)
            elif event.key == pygame.K_UP:
                player.nextVerticalMove(0)
            elif event.key == pygame.K_DOWN:
                player.nextVerticalMove(0)

    # move enemies and lasers
    for a in enemiesANDlasers:
        a.move()

    # collision detection: lasers hit enemies
    for l in lasers:
        if not l.active:
            continue
        for e in enemies:
            if not e.active:
                continue
            if e.isCollision(l):
                l.setActive(False)
                e.setActive(False)
                score_value += 5
                explosion_sound.play()
                totalEnemies -= 1

    # collision of player with an enemy
    for e in enemies:
        if not e.active:
            continue
        if e.isCollision(player):
            running = False
            game_over = True



    for a in enemiesANDlasers:
        a.draw()

    player.move()
    player.draw()

    # user hit pause key
    while pause:
        screen.blit(pause_text, (310, 260))
        pygame.display.update()
        time.sleep(0.2)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause = False


    if totalEnemies <= 0:
        level += 1
        [enemies, totalEnemies] = level_data.spawn_enemies(screen, level)
        enemiesANDlasers = enemies + lasers

    pygame.display.update()

#### end of game ###

# game over screen. only displayed for a few seconds
if game_over:
    # diplay background
    screen.blit(background, (0, 0))
    # display score
    score = score_font.render("Score : " + str(score_value), True, (255, 0, 0))
    screen.blit(score, (330, 340))

    game_over_font = pygame.font.Font('freesansbold.ttf', 80)
    game_over_text = game_over_font.render("Game Over", True, (250, 0, 250))
    screen.blit(game_over_text, (220, 240))

    pygame.display.update()
    time.sleep(3)

# shutdown pygame
pygame.quit()


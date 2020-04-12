import pygame


class Actor:
    def __init__(self, imageFile, startX, startY, changeX=20, changeY=0,  screenSize=[800, 600]):
        self.Pos    = [startX, startY]
        self.Change = [changeX, changeY]
        self.actorImage = pygame.image.load(imageFile)

        self.imgSize    = self.actorImage.get_rect().size
        self.screenSize = screenSize



    # changeX should be a positive value
    def moveLeft(self, changeX = None):
        if not changeX == None:
            self.Pos[0] -= changeX
        else:
            self.Pos[0] -= self.Change[0]

        # make sure the object does not leave the screen
        if self.Pos[0] < 0:
            self.Pos[0] = 0

    # changeX should be a positive value
    def moveRight(self, changeX = None):
        if not changeX == None:
            self.Pos[0] += changeX
        else:
            self.Pos[0] += self.Change[0]
        # make sure the object does not leave the screen
        if self.Pos[0] > (self.screenSize[0] - self.imgSize[0]):
            self.Pos[0] = (self.screenSize[0] - self.imgSize[0])

    # changeX should be a positive value
    def moveDown(self, changeY=None):
        if not changeY == None:
            self.Pos[1] += changeY
        else:
            self.Pos[1] += self.Change[1]

        # make sure the object does not leave the screen
        if self.Pos[1] > (self.screenSize[1] - self.imgSize[1]):
            self.Pos[1] = (self.screenSize[1] - self.imgSize[1])

    # changeX should be a positive value
    def moveUp(self, changeY=None):
        if not changeY == None:
            self.Pos[1] -= changeY
        else:
            self.Pos[1] -= self.Change[1]

        # make sure the object does not leave the screen
        if self.Pos[1] < 0:
            self.Pos[1] = 0


    # draw player
    def draw(self):
        screen.blit(self.actorImage, self.Pos)

    def printInfo(self):
        print("Position: ", self.Pos)



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

# player icon
player = Actor("images/player.png", 200, 480, changeX=5, changeY=5)
enemy  = Actor("images/enemy.png", 200, 150, changeX=2, changeY=2)





# main game loop, everything happens in this loop
running = True
while running:
    # background colour in RGB - this will make the background red
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # some key has been pressed
        if event.type == pygame.KEYDOWN:
            print("a key has been pressed")
            if event.key == pygame.K_LEFT:
                print("the LEFT key has been pressed")
                player.moveLeft()
            elif event.key == pygame.K_RIGHT:
                print("the RIGHT key has been pressed")
                player.moveRight()
            elif event.key == pygame.K_UP:
                print("the RIGHT key has been pressed")
                player.moveUp()
            elif event.key == pygame.K_DOWN:
                print("the RIGHT key has been pressed")
                player.moveDown()
        if event.type == pygame.KEYUP:
            print("a key has been released")

    enemy.moveRight()
    enemy.draw()
    #player.printInfo()
    player.draw()
    pygame.display.update()

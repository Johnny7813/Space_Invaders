import pygame
import math

class Actor:
    collisionConstant = 32.0
    def __init__(self, imageFile, screen,  startX, startY, changeX=20, changeY=0):
        self.pos    = [startX, startY]
        self.change = [changeX, changeY]
        self.actorImage = pygame.image.load(imageFile)
        self.screen = screen

        [iWidth, iHeight] = self.actorImage.get_rect().size
        self.imgSize    = [iWidth, iHeight]
        # centre coordinates of the sprite
        self.center     = [startX + iWidth/2, startY + iWidth/2]

        sHeight = self.screen.get_height()
        sWidth  = self.screen.get_width()
        self.screenSize = [sWidth, sHeight]
        # border left, right, up, down
        self.border = {"left":0, "right": self.screenSize[0]-self.imgSize[0], "up":0, "down":self.screenSize[1]-self.imgSize[1]}
        self.active = True



    # changeX should be a positive value
    def moveLeft(self, changeX = None):
        if not changeX == None:
            self.pos[0] -= changeX
            self.center[0] -= changeX
        else:
            self.pos[0] -= self.change[0]
            self.center[0] -= self.change[0]

        # make sure the object does not leave the screen
        if self.pos[0] < self.border["left"]:
            self.pos[0] = self.border["left"]
            self.center[0] = self.border["left"] + self.imgSize[0]

    # changeX should be a positive value
    def moveRight(self, changeX = None):
        if not changeX == None:
            self.pos[0] += changeX
            self.center[0] += changeX
        else:
            self.pos[0] += self.change[0]
            self.center[0] += self.change[0]
        # make sure the object does not leave the screen
        if self.pos[0] > self.border["right"]:
            self.pos[0] = self.border["right"]
            self.center[0] = self.border["right"] + self.imgSize[0]

    # changeX should be a positive value
    def moveDown(self, changeY=None):
        if not changeY == None:
            self.pos[1] += changeY
            self.center[1] += changeY
        else:
            self.pos[1] += self.change[1]
            self.center[1] += self.change[1]

        # make sure the object does not leave the screen
        if self.pos[1] > self.border["down"]:
            self.pos[1] = self.border["down"]
            self.center[1] += self.border["down"] + self.imgSize[1]

    # changeX should be a positive value
    def moveUp(self, changeY=None):
        if not changeY == None:
            self.pos[1] -= changeY
            self.center[1] -= changeY
        else:
            self.pos[1] -= self.change[1]
            self.center[1] -= self.change[1]

        # make sure the object does not leave the screen
        if self.pos[1] < self.border["up"]:
            self.pos[1] = self.border["up"]
            self.center[1] = self.border["up"] + self.imgSize[1]

    def isCollision(self, actor):
        dx = abs(self.center[0] - actor.center[0])
        dy = abs(self.center[1] - actor.center[1])
        distance = max(dx, dy)
        isCollision = distance<Actor.collisionConstant
        #print("Distance: ", distance)

        return self.active and actor.active and isCollision

    # set actor as active or inactive
    def setActive(self, active):
        self.active = active

    # draw player
    def draw(self):
        if self.active:
            self.screen.blit(self.actorImage, self.pos)

    def printInfo(self):
        print("Position: ", self.pos)


class Enemy(Actor):
    def __init__(self, imageFile, screen, startX, startY, changeX=20, changeY=40):
        super().__init__(imageFile, screen, startX, startY, changeX, changeY)
        #direction of movement
        self.moveToRight = True

    # automatically move the enemy
    def move(self):
        if not self.active:
            return

        if self.moveToRight:
            self.moveRight()
            if self.pos[0] >= self.border["right"]:
                self.pos[1] += self.change[1]
                self.center[1] += self.change[1]
                self.moveToRight = False
        else:
            self.moveLeft()
            if self.pos[0] <= self.border["left"]:
                self.pos[1] += self.change[1]
                self.center[1] += self.change[1]
                self.moveToRight = True

        if self.pos[1] > self.screenSize[1]:
            self.active = False



# Laser of the player space craft
class Laser(Actor):
    def __init__(self, imageFile, screen, startX, startY, changeX=20, changeY=40):
        super().__init__(imageFile, screen, startX, startY, changeX, changeY)
        self.active = False

    # automatically move the enemy
    def move(self):
        if self.active:
            self.pos[1] -= self.change[1]
            self.center[1] -= self.change[1]

        if self.pos[1] <= -self.imgSize[1]:
            self.active = False


    # set initial position by providing an actor
    def setInitalPos(self, Actor):
        posX = Actor.pos[0]
        posY = Actor.pos[1]
        sizeX = Actor.imgSize[0]
        sizeY = Actor.imgSize[1]

        self.pos[0] = posX + sizeX/2 - self.imgSize[0]/2
        self.pos[1] = posY

        self.center[0] = self.pos[0] + self.imgSize[0]/2
        self.center[1] = self.pos[1] + self.imgSize[1]/2

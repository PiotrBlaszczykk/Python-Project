import pygame

class DynamicProp():

    def __init__(self, objectName, objectPosition, imagePath, scale, verticalSpeed, horizontalSpeed, screen):
        #name, postion, path wiadomo, scale - krotka (x, y)
        self.imagePath = imagePath
        self.name = objectName
        self.position = objectPosition
        self.original_appearance = pygame.image.load(self.imagePath)
        self.appearance = pygame.transform.scale(self.original_appearance, scale)
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        self.verticalSpeed = verticalSpeed
        self.horizontalSpeed = horizontalSpeed
        self.screen = screen

        #na potrzeby minigierki dynamic prop może być albo zabójczy - zaberać życie, albo dawać punkty (picie harnolda)
        self.isDeadly = False;

    def setPosition(self, objectPosition):
        self.position = objectPosition
        self.hitbox = self.appearance.get_rect(topleft=self.position)

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def moveHorizontallyLeft(self):
        self.position[0] -= self.horizontalSpeed
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        if self.position[0] < 0:
            self.position[1] = self.screen.get_width()
            self.hitbox = self.appearance.get_rect(topleft=self.position)

    def moveHorizontallyRight(self):
        self.position[0] += self.horizontalSpeed
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        if self.position[0] > self.screen.get_width():
            self.position[1] = 0
            self.hitbox = self.appearance.get_rect(topleft=self.position)
    def moveVerticallyDown(self):
        self.position[1] += self.verticalSpeed
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        if self.position[1] > self.screen.get_height():
            self.position[1] = 0
            self.hitbox = self.appearance.get_rect(topleft=self.position)
    def moveVerticallyUp(self):
        self.position[1] -= self.verticalSpeed
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        if self.position[1] < 0:
            self.position[1] = self.screen.get_height()
            self.hitbox = self.appearance.get_rect(topleft=self.position)
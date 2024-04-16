import pygame

class Pause():

    def __init__(self, objectName, objectPosition):
        self.imagePath = 'grafiki_dump/pauza.png'
        self.name = objectName
        self.position = objectPosition
        self.original_appearance = pygame.image.load(self.imagePath)
        self.appearance = pygame.transform.scale(self.original_appearance, (319, 52))
        self.hitbox = self.appearance.get_rect(topleft=self.position)

    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance


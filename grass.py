import pygame

class Grass():

    def __init__(self, objectName, objectPosition):
        self.imagePath = 'grafiki_dump/grass2.png'
        self.name = objectName
        self.position = objectPosition
        self.original_appearance = pygame.image.load(self.imagePath)
        self.appearance = pygame.transform.scale(self.original_appearance, (1280, 59))
        self.hitbox = self.appearance.get_rect(topleft=self.position)  # Inicjowanie rect

    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance


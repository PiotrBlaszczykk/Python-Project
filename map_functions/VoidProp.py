import pygame

class VoidProp():

    # def __init__(self, objectName, objectPosition, imagePath, scale):
    #     #name, postion, path wiadomo, scale - krotka (x, y)
    #     self.imagePath = imagePath
    #     self.name = objectName
    #     self.position = objectPosition
    #     self.original_appearance = pygame.image.load(self.imagePath)
    #     self.appearance = pygame.transform.scale(self.original_appearance, scale)

    def __init__(self, objectName, objectPosition, imagePath, scale, image_cache):
        # name, postion, path wiadomo, scale - krotka (x, y)
        self.imagePath = imagePath
        self.name = objectName
        self.position = objectPosition
        # self.original_appearance = pygame.image.load(self.imagePath)
        # self.appearance = pygame.transform.scale(self.original_appearance, scale)
        self.appearance = image_cache.get_image(imagePath, scale)


    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance




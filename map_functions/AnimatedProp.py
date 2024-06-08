import pygame
from config import fps_ratio

class AnimatedProp():


    def __init__(self, objectName, objectPosition, imagePath1, imagePath2, scale, image_cache):
        # name, postion, path wiadomo, scale - krotka (x, y)
        self.imagePath1 = imagePath1
        self.imagePath2 = imagePath2
        self.name = objectName
        self.position = objectPosition

        self.image1 = image_cache.get_image(imagePath1, scale)
        self.image2 = image_cache.get_image(imagePath2, scale)

        self.appearance = image_cache.get_image(imagePath1, scale)

        self.ticks_elapsed = 0

    def tick_update(self):

        self.ticks_elapsed += 1

        if self.ticks_elapsed % (240 / fps_ratio) < (120 / fps_ratio):
            self.appearance = self.image1
        else:
            self.appearance = self.image2

        if self.ticks_elapsed == (240 / fps_ratio):
            self.ticks_elapsed = 0

    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance




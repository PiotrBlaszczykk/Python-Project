import pygame
from config import fps_ratio

class DissBlock():

    def __init__(self, objectName, objectPosition, imagePath, scale, image_cache):
        self.imagePath = imagePath
        self.name = objectName
        self.position = objectPosition
        self.appearance = image_cache.get_image(imagePath, scale)
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        self.tick_ellapsed = 0

    def tick_update(self):
        self.tick_ellapsed += 1
        self.hitbox = self.appearance.get_rect(topleft=self.position)


        if self.tick_ellapsed == (200 * fps_ratio):
            self.position[1] += 1000

        elif self.tick_ellapsed == (400 * fps_ratio):
            self.position[1] -= 1000
            self.tick_ellapsed = 0


    def load_image_safe(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Failed to load image {path}: {str(e)}")
            return None  # Or a placeholder image

    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def getHitbox(self):
        return self.hitbox



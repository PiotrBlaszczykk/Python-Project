import pygame

class StaticProp():

    def __init__(self, objectName, objectPosition, imagePath, scale, image_cache):
        #name, postion, path wiadomo, scale - krotka (x, y)
        self.imagePath = imagePath
        self.name = objectName
        self.position = objectPosition
        #self.original_appearance = pygame.image.load(self.imagePath)
        #self.appearance = pygame.transform.scale(self.original_appearance, scale)
        self.appearance = image_cache.get_image(imagePath, scale)
        self.hitbox = self.appearance.get_rect(topleft=self.position)

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



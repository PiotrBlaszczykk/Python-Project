import pygame
from config import fps_ratio

def load_image(path):
    scale = (321, 642)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

#Door nalezy do Interactive Props
class Item():

    def __init__(self, objectName, objectPosition, imagePath, scale, index):
        self.index = index
        self.name = objectName
        self.position = objectPosition

        self.appearance = pygame.image.load(imagePath).convert_alpha()
        self.appearance = pygame.transform.scale(self.appearance, scale)

        self.hitbox = self.appearance.get_rect(topleft=self.position)

        self.ticks_elapsed = 0
        self.shift = 0
        self.direction = 0.5 * fps_ratio


    def spawn_button(self):
        pass
    def tick_update(self, player):

        self.ticks_elapsed += 1

        self.setHitbox()

        self.shift += self.direction
        self.position[1] += self.direction

        if self.shift > 30:
            self.direction *= -1
        elif self.shift < 0:
            self.direction *= -1

        if self.hitbox.colliderect(player.hitbox):
            player.items[self.index] = True
            print("KOLIZJA")
            self.position[1] += 1000

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def getHitbox(self):
        return self.hitbox

    def setHitbox(self):
        self.hitbox = self.appearance.get_rect(topleft=self.position)




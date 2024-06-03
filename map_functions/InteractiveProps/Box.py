import pygame
from config import fps_ratio

def load_image(path):
    scale = (188, 314)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

#Box nalezy do Interactive Props
class Box():

    def __init__(self, objectName, objectPosition):

        self.type = "box"  #przesuwany static prop
        self.idle = load_image("grafiki_dump/Box_0.png")
        self.interacting_1 = load_image("grafiki_dump/Box_E1.png")
        self.interacting_2 = load_image("grafiki_dump/Box_E2.png")
        self.name = objectName
        self.position = objectPosition

        self.appearance = self.idle

        self.hitbox = pygame.Rect(self.position[0], self.position[1] + 120, 188, 194)
        self.interaction_hitbox = pygame.Rect(self.position[0] - 45, self.position[1] + 125, 258, 194)
        self.colliding = False
        self.pushed = False

        self.ticks_elapsed = 0


    def move(self, x):
        self.position[0] += x

    def tick_update(self, player):

        self.ticks_elapsed += 1

        self.setHitbox()

        if not self.pushed:
            if self.interaction_hitbox.colliderect(player.hitbox):
                self.colliding = True
            else:
                self.colliding = False

            if self.colliding:
                if self.ticks_elapsed % (240 / fps_ratio) < (120 / fps_ratio):
                    self.appearance = self.interacting_1
                else:
                    self.appearance = self.interacting_2
            else:
                self.appearance = self.idle

            if self.ticks_elapsed == (240 / fps_ratio):
                self.ticks_elapsed = 0
        else:
            self.appearance = self.idle

    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def getHitbox(self):
        return self.hitbox

    def setHitbox(self):
        self.hitbox = pygame.Rect(self.position[0], self.position[1] + 120, 188, 194)
        self.interaction_hitbox = pygame.Rect(self.position[0] - 45, self.position[1] + 125, 258, 194)




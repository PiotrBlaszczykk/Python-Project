import pygame
from config import fps_ratio

def load_image(path):
    scale = (387, 354)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

#Door nalezy do Interactive Props
class Vent():

    def __init__(self, objectName, objectPosition, destination):
        self.type = "warp"  #różne typy, warp - po wcisnieciu E przenosimy sie do innej lokacji
        self.idle = load_image("grafiki_dump/vent_0.png")
        self.interacting_1 = load_image("grafiki_dump/vent_E1.png")
        self.interacting_2 = load_image("grafiki_dump/vent_E2.png")
        self.name = objectName
        self.position = objectPosition

        self.appearance = self.idle

        self.hitbox = pygame.Rect(self.position[0] + 10, self.position[1] + 20, 210, 138)
        self.destination = destination
        self.colliding = False

        self.ticks_elapsed = 0


    def spawn_button(self):
        pass
    def tick_update(self, player):

        self.ticks_elapsed += 1

        self.setHitbox()

        if self.hitbox.colliderect(player.hitbox):
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



    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def getHitbox(self):
        return self.hitbox

    def setHitbox(self):
        self.hitbox = pygame.Rect(self.position[0] + 40, self.position[1] + 180, 210, 138)




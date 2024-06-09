import pygame
from config import fps_ratio

def load_image(path):
    scale = (150, 64)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

#Door nalezy do Interactive Props
class Button():

    def __init__(self, objectName, objectPosition, index):
        self.type = "button"  #różne typy, warp - po wcisnieciu E przenosimy sie do innej lokacji
        self.off = load_image("grafiki_dump/button_off.png")
        self.on = load_image("grafiki_dump/button_pressed.png")
        # self.interacting_1 = load_image("grafiki_dump/door1_E1.png")
        # self.interacting_2 = load_image("grafiki_dump/door1_E2.png")
        self.name = objectName
        self.position = objectPosition

        self.appearance = self.off

        self.hitbox = self.appearance.get_rect(topleft=self.position)
        self.colliding = False

        self.ticks_elapsed = 0
        self.pressed = False
        self.index = index


    def tick_update(self, player):

        self.ticks_elapsed += 1

        self.setHitbox()

        if self.hitbox.colliderect(player.hitbox):
            self.colliding = True
        else:
            self.colliding = False

        if self.pressed:
            self.appearance = self.on
        else:
            self.appearance = self.off


        # if self.colliding:
        #     if self.ticks_elapsed % (240 / fps_ratio) < (120 / fps_ratio):
        #         self.appearance = self.interacting_1
        #     else:
        #         self.appearance = self.interacting_2
        # else:
        #     self.appearance = self.idle
        #
        # if self.ticks_elapsed == (240 / fps_ratio):
        #     self.ticks_elapsed = 0



    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def getHitbox(self):
        return self.hitbox

    def setHitbox(self):
        self.hitbox = self.appearance.get_rect(topleft=self.position)




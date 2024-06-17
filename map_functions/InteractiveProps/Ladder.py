import pygame
from config import fps_ratio

def load_image(path):
    scale = (190, 105)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

#Door nalezy do Interactive Props
class Ladder():

    def __init__(self, objectName, objectPosition, destination):
        self.type = "warp"  #różne typy, warp - po wcisnieciu E przenosimy sie do innej lokacji
        self.appearance = load_image("grafiki_dump/ladder.png")
        self.name = objectName
        self.position = objectPosition

        self.hitbox = pygame.Rect(self.position[0], self.position[1] + 50, 190, 105)
        self.destination = destination
        self.colliding = False



    def spawn_button(self):
        pass
    def tick_update(self, player):


        self.setHitbox()

        if self.hitbox.colliderect(player.hitbox):
            self.colliding = True
        else:
            self.colliding = False




    def setPosition(self, objectPosition):
        self.position = objectPosition

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def getHitbox(self):
        return self.hitbox

    def setHitbox(self):
        self.hitbox = pygame.Rect(self.position[0], self.position[1] -60, 190, 105)

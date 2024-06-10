import pygame
from config import fps_ratio

def load_image(path):
    scale = (576, 423)
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, scale)
    return image

class ExitDoor():

    def __init__(self, objectName, objectPosition, destination):
        self.type = "exit_door"
        self.closed = load_image("grafiki_dump/exit_door_closed.png")
        self.open_image = load_image("grafiki_dump/exit_door_open.png")
        self.interacting_1 = load_image("grafiki_dump/exit_door_E1.png")
        self.interacting_2 = load_image("grafiki_dump/exit_door_E2.png")
        self.name = objectName
        self.position = objectPosition

        self.appearance = self.closed
        self.open = False

        self.hitbox = pygame.Rect(self.position[0] + 86, self.position[1] + 350, 170, 300)
        self.destination = destination
        self.colliding = False

        self.ticks_elapsed = 0


    def check_if_game_finished(self, player):
        for item in player.items:
            if not item:
                return False

        self.open = True
        return True

    def tick_update(self, player):

        self.check_if_game_finished(player)
        self.ticks_elapsed += 1

        self.setHitbox()

        if self.hitbox.colliderect(player.hitbox):
            self.colliding = True
        else:
            self.colliding = False

        if self.colliding and self.open:
            if self.ticks_elapsed % (240 / fps_ratio) < (120 / fps_ratio):
                self.appearance = self.interacting_1
            else:
                self.appearance = self.interacting_2
        elif self.open:
            self.appearance = self.open_image
        else:
            self.appearance = self.closed

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
        self.hitbox = pygame.Rect(self.position[0] + 198, self.position[1] + 120, 180, 300)




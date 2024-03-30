import pygame

class Player():
    def __init__(self, playerName, playerPosition, imagePath):
        self.name = playerName
        self.position = playerPosition
        self.appearance = pygame.image.load(imagePath)
        self.inventory = []
        self.player_movement = [False, False, False, False]
    def setPosition(self, playerPosition):
        self.position = playerPosition

    def tickUpdate(self):
        self.position[1] += (self.player_movement[1] - self.player_movement[0]) * 5
        self.position[0] += (self.player_movement[3] - self.player_movement[2]) * 5

    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance


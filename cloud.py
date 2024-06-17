import pygame
import math

class Cloud():
    def __init__(self, size, position, speed, screen_width):
        self.image = pygame.image.load("menu/cloud_transparent.png")
        self.image = pygame.transform.scale(self.image, size)
        self.position = position
        self.move_speed = speed
        self.screen_width = screen_width
    def move(self):
        self.position[0] += self.move_speed
        if self.position[0] > self.screen_width:
            self.position[0] = -self.image.get_width()

    def getPosition(self):
        return self.position
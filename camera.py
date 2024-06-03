import sys
import pygame
from player import Player
import math
from maps import *
from cloud import Cloud

class Camera():
    def __init__(self, map_objects):
        self.static_props = map_objects[0]
        self.void_props = map_objects[1]
        self.dynamic_objects = map_objects[2]
        self.interactive_props = map_objects[3]
        self.background_props = map_objects[4]
        self.horizontalVelocity = 0
        self.verticalVelocity = 0
        self.isPlayerBlocked = False

    def setVerticalVelocity(self, value):
        self.verticalVelocity = value
    def setHorizontalVelocity(self, value):
        self.horizontalVelocity = value

    def move(self):

        for object in self.static_props:
            object.position[0] += self.horizontalVelocity
            object.hitbox = object.appearance.get_rect(topleft=object.position)

        for object in self.void_props:
            object.position[0] += self.horizontalVelocity

        for object in self.dynamic_objects:
            object.position[0] += self.horizontalVelocity
            object.hitbox = object.appearance.get_rect(topleft=object.position)

        for object in self.interactive_props:
            object.position[0] += self.horizontalVelocity
            object.hitbox = object.getHitbox()

        for object in self.background_props:
            object.position[0] += (self.horizontalVelocity * 0.25)



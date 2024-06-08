import sys
import pygame
from player import Player
import math
from maps import *
from cloud import Cloud

class Camera():
    def __init__(self, map_objects):
        self.static_props = map_objects["static_props"]
        self.void_props = map_objects["void_props"]
        self.dynamic_props = map_objects["dynamic_props"]
        self.interactive_props = map_objects["interactive_props"]
        self.background_props = map_objects["background_props"]
        self.animated_props = map_objects["animated_props"]
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

        for object in self.animated_props:
            object.position[0] += self.horizontalVelocity

        for object in self.dynamic_props:
            object.position[0] += self.horizontalVelocity
            object.hitbox = object.appearance.get_rect(topleft=object.position)

        for object in self.interactive_props:
            object.position[0] += self.horizontalVelocity
            object.hitbox = object.getHitbox()

        for object in self.background_props:
            object.position[0] += (self.horizontalVelocity * 0.25)



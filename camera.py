import sys
import pygame
from player import Player
import math
from grass import Grass
from map import Map
from cloud import Cloud
from deska import Deska
from kolumna import Kolumna
from pauza import Pause

class Camera():
    def __init__(self, map_objects):
        self.objects_to_move = map_objects
        self.horizontalVelocity = 0
        self.verticalVelocity = 0
        self.isPlayerBlocked = False

    def setVerticalVelocity(self, value):
        self.verticalVelocity = value
    def setHorizontalVelocity(self, value):
        self.horizontalVelocity = value

    def move(self):
        for object in self.objects_to_move:
            object.position[0] += self.horizontalVelocity
            object.position[1] += self.verticalVelocity
            object.hitbox = object.appearance.get_rect(topleft=object.position)


import os
import json
import pygame

from map_functions.ImageCache import ImageCache
from map_functions.StaticProp import StaticProp
from map_functions.VoidProp import VoidProp
from map_functions.InteractiveProps.Door import Door

class MapLoader():
    def __init__(self, screen):
        self.screen = screen
        self.ImageCache = ImageCache()
        #objects: [StaticProps, VoidProps, DyamicProps, InteractiveProps, Spawn]

    def loadMap(self, directory):
        self.map_objects = []
        jsonPath = os.path.join(directory, "data.json")
        with open(jsonPath, 'r') as file:
            self.map = json.load(file)

        graphicsDirectory = os.path.join(directory, "graphics")

        if "BackgroundColor" in self.map:
            bg_color = self.map.get('BackgroundColor', {})
            self.background_color = (
                bg_color.get('r', 0),
                bg_color.get('g', 0),
                bg_color.get('b', 0)
            )
        else:
            self.background_color = (255, 255, 255)

        self.spawn = [0, 0]
        if "Spawn" in self.map:
            spawn_info = self.map.get('Spawn', {})
            self.spawn[0] = spawn_info.get('x', 420)
            self.spawn[1] = spawn_info.get('y', 0)


        self.static_props = []
        if 'StaticProps' in self.map:
            for obj in self.map['StaticProps']:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath = os.path.join(graphicsDirectory, obj['imagePath'])
                #new_object = StaticProp(obj['name'], position, imagePath, scale)
                new_object = StaticProp(obj['name'], position, imagePath, scale, self.ImageCache)
                self.static_props.append(new_object)

        self.void_props = []
        if 'VoidProps' in self.map:
            for obj in self.map['VoidProps']:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath = os.path.join(graphicsDirectory, obj['imagePath'])
                new_object = VoidProp(obj['name'], position, imagePath, scale, self.ImageCache)
                self.void_props.append(new_object)

        self.interactive_props = []

        self.doors = []
        if 'Warps' in self.map:
            for obj in self.map['Warps']:
                position = [obj['position']['x'], obj['position']['y']]
                destination = obj['destination']
                new_object = Door(obj['name'], position, destination)
                self.interactive_props.append(new_object)


        self.dynamic_props = []                     #do edycji, tymczasowe żeby się program kompilował

        self.map_objects.append(self.static_props)
        self.map_objects.append(self.void_props)
        self.map_objects.append(self.dynamic_props)
        self.map_objects.append(self.interactive_props)

        self.map_objects.append(self.spawn)
        return self.map_objects


    def render(self):


        self.screen.fill(self.background_color)
        for obj in self.void_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.static_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.interactive_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        # for obj in self.interactive_props:
        #     pygame.draw.rect(self.screen, (255, 0, 0), obj.hitbox, 10)
        #do debugowania


    def resetAttributes(self):
        self.map_objects = []
        self.void_props = []
        self.map = None
        self.static_props = []
        self.void_props = []

    def loadMisc(self, passedClass):
        self.resetAttributes()
        passedClass.render()



import os
import json
import pygame

from map_functions.ImageCache import ImageCache
from map_functions.StaticProp import StaticProp
from map_functions.VoidProp import VoidProp
from map_functions.InteractiveProps.Door import Door
from map_functions.InteractiveProps.Box import Box
from map_functions.InteractiveProps.BoxBig import BoxBig
from map_functions.BackgroundProp import BackgroundProp
from map_functions.AnimatedProp import AnimatedProp
from map_functions.InteractiveProps.Ladder import Ladder
from map_functions.InteractiveProps.Vent import Vent
from map_functions.DissBlock import DissBlock
from map_functions.Item import Item

class MapLoader():
    def __init__(self, screen):
        self.screen = screen
        self.ImageCache = ImageCache()
        #objects: [StaticProps, VoidProps, DyamicProps, InteractiveProps, Spawn]

    def loadMap(self, directory):
        self.map_objects = {}
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

        #self.doors = []
        if 'Warps' in self.map:
            for obj in self.map['Warps']:
                position = [obj['position']['x'], obj['position']['y']]
                destination = obj['destination']
                if obj['type'] == 'door':
                    new_object = Door(obj['name'], position, destination)
                elif obj['type'] == 'ladder':
                    new_object = Ladder(obj['name'], position, destination)
                elif obj['type'] == 'vent':
                    new_object = Vent(obj['name'], position, destination)
                self.interactive_props.append(new_object)

        if "Boxes" in self.map:
            for obj in self.map['Boxes']:
                position = [obj['position']['x'], obj['position']['y']]
                variant = obj['variant']
                new_object = Box(obj['name'], position) if variant == "normal" else BoxBig(obj['name'], position)
                self.interactive_props.append(new_object)

        self.background_props = []
        if "BackgroundProps" in self.map:
            for obj in self.map['BackgroundProps']:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath = os.path.join(graphicsDirectory, obj['imagePath'])
                new_object = BackgroundProp(obj['name'], position, imagePath, scale, self.ImageCache)
                self.background_props.append(new_object)

        self.animated_props = []
        if "AnimatedProps" in self.map:
            for obj in self.map['AnimatedProps']:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath1 = os.path.join(graphicsDirectory, obj['imagePath1'])
                imagePath2 = os.path.join(graphicsDirectory, obj['imagePath2'])
                new_object = AnimatedProp(obj['name'], position, imagePath1, imagePath2, scale, self.ImageCache)
                self.animated_props.append(new_object)

        self.diss_blocks = []
        if "DissBlocks" in self.map:
            for obj in self.map['DissBlocks']:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath = os.path.join(graphicsDirectory, obj['imagePath'])
                new_object = DissBlock(obj['name'], position, imagePath, scale, self.ImageCache, obj['start'])
                self.diss_blocks.append(new_object)


        self.items = []
        if "Items" in self.map:
            for obj in self.map['Items']:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath = os.path.join(graphicsDirectory, obj['imagePath'])
                index = obj['index']
                new_object = Item(obj['name'], position, imagePath, scale, index)
                self.items.append(new_object)



        self.dynamic_props = []                     #do edycji, tymczasowe żeby się program kompilował

        # self.map_objects.append(self.static_props)
        # self.map_objects.append(self.void_props)
        # self.map_objects.append(self.dynamic_props)
        # self.map_objects.append(self.interactive_props)
        # self.map_objects.append(self.background_props)

        # self.map_objects.append(self.spawn)

        self.map_objects["static_props"] = self.static_props
        self.map_objects["void_props"] = self.void_props
        self.map_objects["dynamic_props"] = self.dynamic_props
        self.map_objects["interactive_props"] = self.interactive_props
        self.map_objects["background_props"] = self.background_props
        self.map_objects["spawn"] = self.spawn
        self.map_objects["animated_props"] = self.animated_props
        self.map_objects["diss_blocks"] = self.diss_blocks
        self.map_objects["items"] = self.items

        return self.map_objects


    def render(self):


        self.screen.fill(self.background_color)

        for obj in self.background_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.void_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.animated_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.static_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.diss_blocks:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.interactive_props:
            self.screen.blit(obj.getAppearance(), obj.getPosition())

        for obj in self.items:
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
        self.diss_blocks =[]
        self.background_props =[]
        self.animated_props =[]
        self.interactive_props =[]

    def loadMisc(self, passedClass):
        self.resetAttributes()
        passedClass.render()



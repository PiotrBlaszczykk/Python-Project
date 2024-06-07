import os
import json
import random
import pygame
from map_functions.DynamicProp import DynamicProp
from map_functions.ImageCache import ImageCache
from map_functions.StaticProp import StaticProp
from map_functions.VoidProp import VoidProp
from config import fps, fps_ratio
import sys
from camera import Camera


class minigame_falling_blocks:
    def __init__(self, screen, clock, player, motherClass):
        self.screen = screen
        self.health = 3
        self.score = 0
        self.clock = clock
        self.static_props = []
        self.dynamic_props = []
        self.map = None
        self.dynamic_elements_amount = 2
        self.player = player
        self.camera = None
        self.map_objects = {}
        self.motherClass = motherClass
        self.loadMap()

    def loadMap(self):
        self.ImageCache = ImageCache()
        with open('minigames/falling_blocks/data.json', 'r') as file:
            self.map = json.load(file)
            static_elements = self.map["static_props"]
            for obj in static_elements:
                position = [obj['position']['x'], obj['position']['y']]
                scale = (obj['scale']['x'], obj['scale']['y'])
                imagePath = obj['imagePath']
                new_object = StaticProp(obj['name'], position, imagePath, scale, self.ImageCache)
                self.static_props.append(new_object)
                self.map_objects.append(self.static_props)

            for i in range(self.dynamic_elements_amount):
                self.dynamicElementGenerate()
            self.map_objects.append([]) #temporary until we fill void elements
            self.map_objects.append(self.dynamic_props)
            self.map_objects.append([]) #zeby sie nie wykruszylo, bo dodalem interactive props
            self.map_objects.append([])  # tak samo dla background props
            self.camera = Camera(self.map_objects)

            self.map


    def dynamicElementGenerate(self):
        x = random.randint(0, self.screen.get_width())
        y = random.randint(0, self.screen.get_height())
        position = [x, y]
        horizontal_speed = random.randint(1, 4)
        vertical_speed = random.randint(1, 4)
        imagePath = 'minigames/falling_blocks/graphics/grass1.png'
        scale_x = random.randint(20, 80)
        scale_y = random.randint(10, 50)
        scale = (scale_x, scale_y)

        element = DynamicProp("falling block", position, imagePath, scale, vertical_speed, horizontal_speed, self.screen)
        self.dynamic_props.append(element)


    def checkColision(self, dynamic_el):
        objects_start_x = dynamic_el.getPosition()[0]
        objects_end_x = dynamic_el.getPosition()[0] + dynamic_el.getAppearance().get_width()
        objects_start_y = dynamic_el.getPosition()[1]
        objects_end_y = dynamic_el.getPosition()[1] + dynamic_el.getAppearance().get_height()

        players_start_x = self.player.getPosition()[0]
        players_end_x = self.player.getPosition()[0] + self.player.getAppearance().get_width()
        players_start_y = self.player.getPosition()[1]
        players_end_y = self.player.getPosition()[1] + self.player.getAppearance().get_height()


        vertical_overlap = (objects_start_y > players_start_y and objects_start_y < players_end_y)
        horizontal_overlap = ((objects_start_x > players_start_x and objects_start_x < players_end_x) or (objects_end_x < players_end_x and objects_end_x > objects_start_x))
        # if (objects_start_y > players_start_y and
        #         objects_start_y < players_end_y):
        #     if(objects_start_x > players_start_x and objects_start_x < players_end_x or
        #     objects_end_x < players_end_x and objects_end_x > objects_start_x):
        #         return True
        if vertical_overlap and horizontal_overlap:
            return True

        return False

    def render(self):
        is_over = False
        while True:
            self.screen.fill((68, 15, 104))
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:

                    self.motherClass.reloadMap("maps/test2")
                    self.motherClass.run()
                    is_over = True
                    break

                    # R key is pressed
                    # Your code for handling R key press goes here

                elif keys[pygame.K_t]:

                    self.motherClass.reloadMap("maps/test1")
                    self.motherClass.run()
                    is_over = True
                    break

                self.player.movement(event, self.camera)
            if is_over == True:
                self.motherClass.reloadMap("maps/test1")
                self.motherClass.run()
                break


            self.player.tick_update(self.static_props, self.camera)

            for static_el in self.static_props:
                self.screen.blit(static_el.getAppearance(), static_el.getPosition())

            for dynamic_el in self.dynamic_props:
                if(self.checkColision(dynamic_el)):
                    is_over = True
                    break
                dynamic_el.moveVerticallyDown()
                self.screen.blit(dynamic_el.getAppearance(), dynamic_el.getPosition())

            self.clock.tick(fps)
            pygame.display.update()


import os
import json
import random
import pygame
from map_functions.DynamicProp import DynamicProp
from map_functions.ImageCache import ImageCache
from map_functions.MapLoader import MapLoader
from map_functions.StaticProp import StaticProp
from map_functions.VoidProp import VoidProp
from config import fps, fps_ratio
import sys
from camera import Camera
import time


class minigame_lights:
    def __init__(self, screen, clock, player, motherClass):
        self.screen = screen
        self.clock = clock
        self.static_props = []
        self.void_props = []
        self.player = player
        self.camera = None
        self.map_objects = {}
        self.motherClass = motherClass
        self.mapLoader = MapLoader(self.screen)
        self.solution = [1,0,0,0,1]
        self.curr_number = [0,0,0,0,0]
        self.diodeOffs = []
        self.diodeOns = []
        self.buttonOffs = []
        self.buttonPressed = []
        self.loadMap()

    def loadMap(self):
        self.ImageCache = ImageCache()
        self.map_objects = self.mapLoader.loadMap("minigames/lights")
        self.static_props = self.map_objects["static_props"]
        self.void_props = self.map_objects["void_props"]
        self.interactive_props = self.map_objects["interactive_props"]

        self.buttons = []
        for obj in self.map_objects["interactive_props"]:
            if obj.type == "button":
                self.buttons.append(obj)

        for object in self.static_props:
            if object.name == "diodeOff":
                self.diodeOffs.append(object)
            elif object.name == "diodeOn":
                self.diodeOns.append(object)
            elif object.name == "buttonOff":
                self.buttonOffs.append(object)
            elif object.name == "buttonPressed":
                self.buttonPressed.append(object)


        self.camera = Camera(self.map_objects)

    def check_solution(self):
        n = len(self.solution)
        flag = True
        for i in range(n):
            if self.solution[i] != self.curr_number[i]:
                flag = False
                break
        return flag

    def updateDiode(self, diodeNum):
        if self.curr_number[diodeNum] == 0:
            self.curr_number[diodeNum] = 1
        else:
            self.curr_number[diodeNum] = 0

    def checkButtonColision(self, button):

        if self.player.hitbox.colliderect(button.hitbox):
            return True
        else:
            return False



    def render(self):
        while True:
            self.screen.fill((68, 15, 104))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:

                    for button in self.buttons:
                        if self.checkButtonColision(button):
                            self.updateDiode(button.index)

                    # for i in range(len(self.solution)):
                    #     if self.checkButtonColision(self.buttonOffs[i]):
                    #         self.updateDiode(i)

                self.player.movement(event, self.camera)
            pygame.draw.rect(self.screen, (255, 0, 0), self.player.hitbox, 10)

            self.player.tick_update(self.static_props, self.camera, self.map_objects["interactive_props"], self.map_objects["diss_blocks"])

            for void_el in self.void_props:
                self.screen.blit(void_el.getAppearance(), void_el.getPosition())

            for obj in self.buttons:
                self.screen.blit(obj.getAppearance(), obj.getPosition())

            for static_el in self.static_props:
                if static_el.name == "diodeOn" or static_el.name == "diodeOff":
                    continue
                self.screen.blit(static_el.getAppearance(), static_el.getPosition())
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())

            for i in range(len(self.solution)):
                currDiodeOff = self.diodeOffs[i]
                currDiodeOn = self.diodeOns[i]
                currButtonOff = self.buttonOffs[i]
                currButtonPressed = self.buttonPressed[i]

                if self.curr_number[i] == 1:
                    self.screen.blit(currDiodeOn.getAppearance(), currDiodeOn.getPosition())
                    self.screen.blit(currButtonPressed.getAppearance(), currButtonPressed.getPosition())
                    pygame.draw.rect(self.screen, (255, 0, 0), currDiodeOn.hitbox, 10)
                    pygame.draw.rect(self.screen, (255, 0, 0), currButtonPressed.hitbox, 10)
                else:
                    self.screen.blit(currDiodeOff.getAppearance(), currDiodeOff.getPosition())
                    self.screen.blit(currButtonOff.getAppearance(), currButtonOff.getPosition())
                    pygame.draw.rect(self.screen, (255, 0, 0), currDiodeOff.hitbox, 10)
                    pygame.draw.rect(self.screen, (255, 0, 0), currButtonOff.hitbox, 10)

            if self.check_solution():
                time.sleep(1)
                self.motherClass.reloadMap("maps/test1")
                self.motherClass.run()
                return True

            self.clock.tick(fps)
            pygame.display.update()

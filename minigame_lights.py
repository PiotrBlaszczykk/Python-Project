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
        self.completed = False
        self.loadMap()
        player.position[1] = 400

    def loadMap(self):
        self.ImageCache = ImageCache()
        self.map_objects = self.mapLoader.loadMap("minigames/lights")
        self.static_props = self.map_objects["static_props"]
        self.void_props = self.map_objects["void_props"]
        self.kebab = self.map_objects["items"][0]

        self.kebab.hide()

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
        players_start_x = self.player.getPosition()[0]
        players_end_x = self.player.getPosition()[0] + self.player.getAppearance().get_width()

        button_start_x = button.getPosition()[0]
        button_end_x = button.getPosition()[0] + button.getAppearance().get_width()

        if players_start_x < button_end_x and players_end_x > button_start_x:
            return True
        else:
            return False


    def drawGame(self, flag):
        for i in range(len(self.solution)):
            currDiodeOff = self.diodeOffs[i]
            currDiodeOn = self.diodeOns[i]
            currButtonOff = self.buttonOffs[i]
            currButtonPressed = self.buttonPressed[i]

            if self.curr_number[i] == 1:
                self.screen.blit(currDiodeOn.getAppearance(), currDiodeOn.getPosition())
                self.screen.blit(currButtonPressed.getAppearance(), currButtonPressed.getPosition())
            else:
                self.screen.blit(currDiodeOff.getAppearance(), currDiodeOff.getPosition())
                self.screen.blit(currButtonOff.getAppearance(), currButtonOff.getPosition())


    def render(self):
        counter = 0;
        while True:
            self.screen.fill((68, 15, 104))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    for i in range(len(self.buttonOffs)):
                        if counter >= 1:
                            counter = 0
                            break
                        if self.checkButtonColision(self.buttonOffs[i]):
                            self.updateDiode(i)
                            counter += 1
                            break

                self.player.movement(event, self.camera)
            self.player.tick_update(self.static_props, self.camera, self.map_objects["interactive_props"], self.map_objects["diss_blocks"])
            self.kebab.tick_update(self.player)

            if self.player.hitbox.colliderect(self.kebab.hitbox) and self.completed:
                print("item collected")
                self.motherClass.starting_map = "maps/floor2"
                self.motherClass.run()

            for static_el in self.static_props:
                if static_el.name == "buttonOff" or static_el.name == "buttonPressed" or static_el.name == "diodeOn" or static_el.name == "diodeOff":
                    continue
                self.screen.blit(static_el.getAppearance(), static_el.getPosition())
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())
            self.screen.blit(self.kebab.getAppearance(), self.kebab.getPosition())

            self.drawGame(False)

            if self.check_solution() and not self.completed:
                # for i in range(120):
                #     self.drawGame(True)
                #     self.clock.tick(fps)
                #     pygame.display.update()
                self.completed = True
                self.kebab.show()
                # self.motherClass.reloadMap("maps/test1")
                # self.motherClass.run()
                # return True

            self.clock.tick(fps)
            pygame.display.update()
import os
import json
import random
import pygame
from map_functions.DynamicProp import DynamicProp
from map_functions.ImageCache import ImageCache
from map_functions.MapLoader import MapLoader
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
        self.void_props = []
        self.dynamic_elements_amount = 2
        self.player = player
        self.camera = None
        self.map_objects = {}
        self.motherClass = motherClass
        self.mapLoader = MapLoader(self.screen)
        self.counter = 0 #potrzebne do spawnowania elementów
        self.completed = False
        self.loadMap()
        self.paused = False
        self.completed = False

        self.item_collected = False

    def loadMap(self):
        self.ImageCache = ImageCache()
        self.map_objects = self.mapLoader.loadMap("minigames/falling_blocks")
        self.static_props = self.map_objects["static_props"]
        self.void_props = self.map_objects["void_props"]
        self.map_objects["dynamic_props"] = self.dynamic_props
        self.items = self.map_objects["items"]

        self.heart = pygame.image.load("minigames/falling_blocks/graphics/full_heart.png")
        self.heart = pygame.transform.scale(self.heart, (80, 80))

        self.harnas = pygame.image.load("minigames/falling_blocks/graphics/harnas.png")
        self.harnas = pygame.transform.scale(self.harnas, (60, 80))

        self.ruskacz = self.map_objects["items"][0]
        self.ruskacz.hide()


        self.camera = Camera(self.map_objects)

    def dynamicElementGenerate(self):
        is_beer = False
        beer_or_deadly = random.randint(0, 10)
        if beer_or_deadly <=2:
            is_beer = True

        x = random.randint(0, self.screen.get_width())
        y = 0
        position = [x, y]
        horizontal_speed = random.randint(1, 4)
        vertical_speed = random.randint(1, 4)
        if is_beer == False:
            imagePath = 'grafiki_dump/dwa_zero.png'
            scale_x = 62 * 2
            scale_y = 41 * 2
        else:
            imagePath = 'grafiki_dump/harnas.png'
            scale_x = 15 * 4
            scale_y = 24 * 4
        scale = (scale_x, scale_y)

        element = DynamicProp("falling block", position, imagePath, scale, vertical_speed, horizontal_speed, self.screen)
        if is_beer == False:
            element.isDeadly = True
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


        horizontal_overlap = (objects_start_x < players_end_x and objects_end_x > players_start_x)
        vertical_overlap = (objects_start_y < players_end_y and objects_end_y > players_start_y)

        if horizontal_overlap and vertical_overlap:
            return True

        return False

    def remove_fallen_element(self, dynamic_el):
        objects_start_y = dynamic_el.getPosition()[1]
        objects_end_y = dynamic_el.getPosition()[1] + dynamic_el.getAppearance().get_height()
        if objects_end_y >= self.screen.get_height() - 20:
            self.dynamic_props.remove(dynamic_el)

    def show_items(self):

        items = self.player.items

        if items[0]:
            image = pygame.image.load("items/ruskacz.png").convert_alpha()
        else:
            image = pygame.image.load("items/ruskacz_blank.png").convert_alpha()
        image = pygame.transform.scale(image, (67, 147))
        image_rect = image.get_rect(center = (380, 100))
        self.screen.blit(image, image_rect)

        if items[1]:
            image = pygame.image.load("items/marlboro.png").convert_alpha()
        else:
            image = pygame.image.load("items/marlboro_blank.png").convert_alpha()
        image = pygame.transform.scale(image, (63, 120))
        image_rect = image.get_rect(center = (490, 100))
        self.screen.blit(image, image_rect)

        if items[2]:
            image = pygame.image.load("items/trzy_zero.png").convert_alpha()
        else:
            image = pygame.image.load("items/trzy_zero_blank.png").convert_alpha()
        image = pygame.transform.scale(image, (118, 76))
        image_rect = image.get_rect(center = (620, 100))
        self.screen.blit(image, image_rect)

        if items[3]:
            image = pygame.image.load("items/kebab.png").convert_alpha()
        else:
            image = pygame.image.load("items/kebab_blank.png").convert_alpha()
        image = pygame.transform.scale(image, (107, 87))
        image_rect = image.get_rect(center = (750, 100))
        self.screen.blit(image, image_rect)

        if items[4]:
            image = pygame.image.load("items/vifon.png").convert_alpha()
        else:
            image = pygame.image.load("items/vifon_blank.png").convert_alpha()
        image = pygame.transform.scale(image, (93, 123))
        image_rect = image.get_rect(center = (880, 100))
        self.screen.blit(image, image_rect)



    def render(self):
        is_over = False
        successfull = False
        heart_position_y = 10
        heart_position_x = 10
        harnas_position_y = 100
        harnas_position_x = 10

        self.pause_button = pygame.image.load("grafiki_dump/pauza.png").convert_alpha()
        self.pause_button = pygame.transform.scale(self.pause_button, (471, 78))
        self.pause_button_rect = self.pause_button.get_rect(
            center=(640, 360))


        while True:
            self.screen.fill((152, 217, 234))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True

                keys = pygame.key.get_pressed()

                if not self.paused:
                    self.player.movement(event, self.camera)

            if is_over == True:
                self.motherClass.reloadMap("maps/floor4")
                self.motherClass.run()
                break

            for void_el in self.void_props:
                self.screen.blit(void_el.getAppearance(), void_el.getPosition())

            for static_el in self.static_props:
                self.screen.blit(static_el.getAppearance(), static_el.getPosition())
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())

            for obj in self.items:
                self.screen.blit(obj.getAppearance(), obj.getPosition())

            for i in range(self.health):
                self.screen.blit(self.heart, [self.heart.get_width() * i + 5, heart_position_y])

            for i in range(self.score):
                self.screen.blit(self.harnas, [self.harnas.get_width() * i + 5, harnas_position_y])

            for dynamic_el in self.dynamic_props:
                self.screen.blit(dynamic_el.getAppearance(), dynamic_el.getPosition())


            if not self.paused:

                if self.player.hitbox.colliderect(self.ruskacz.hitbox) and self.completed:
                    self.item_collected = True
                    print("item collected")
                    self.motherClass.reloadMap("maps/floor4")
                    self.motherClass.run()
                    return successfull

                self.player.tick_update(self.static_props, self.camera, self.map_objects["interactive_props"], self.map_objects["diss_blocks"])

                self.ruskacz.tick_update(self.player)

                for dynamic_el in self.dynamic_props:
                    if(self.checkColision(dynamic_el)):
                        if(dynamic_el.isDeadly == True):
                            self.health -= 1
                            self.dynamic_props.remove(dynamic_el)
                            if self.health <= 0:
                                is_over = True
                                successfull = False
                                self.motherClass.reloadMap("maps/floor4")
                                self.motherClass.run()
                                return successfull
                            break
                        else:
                            self.score+=1
                            if self.score >= 10 and not self.completed:
                                self.successfull = True
                                self.completed = True
                                self.ruskacz.show()


                            print(self.score)
                            self.dynamic_props.remove(dynamic_el)

                    self.remove_fallen_element(dynamic_el)
                    dynamic_el.moveVerticallyDown()

                if self.counter >= 120 and self.completed == False:
                    self.counter = 0
                    self.dynamicElementGenerate()

                self.counter += 1


            else:
                # pauza
                self.screen.blit(self.pause_button, self.pause_button_rect)
                keys = pygame.key.get_pressed()
                self.show_items()

            self.clock.tick(fps)
            pygame.display.update()


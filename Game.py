import sys
import pygame

from minigame_lights import minigame_lights
from player import Player
import math
from cloud import Cloud
from camera import Camera
from Menu import Menu
from minigame_falling_blocks import minigame_falling_blocks

from map_functions.MapLoader import MapLoader



from config import fps, fps_ratio
class Game:

    def __init__(self, player):

        pygame.init()
        pygame.display.set_caption('Escape from D17')
        self.player = player
        self.screen = pygame.display.set_mode((1280, 720))
        self.mapLoader = MapLoader(self.screen)
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen, self.clock, self)
        self.falling_blocks = minigame_falling_blocks(self.screen, self.clock, self.player, self)
        self.paused = False

        self.starting_map = "maps/easter_egg"


    def showMenu(self):
        self.mapLoader.loadMisc(self.menu)

    def show_falling_blocks(self):
        self.falling_blocks = minigame_falling_blocks(self.screen, self.clock, self.player, self)
        self.mapLoader.loadMisc(self.falling_blocks)

    def show_lights(self):
        self.minigame_lights = minigame_lights(self.screen, self.clock, self.player, self)
        self.mapLoader.loadMisc(self.minigame_lights)

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


    def reloadMap(self, mapFile):


        self.map_objects = self.mapLoader.loadMap(mapFile)
        self.static_props = self.map_objects["static_props"]
        self.void_props = self.map_objects["void_props"]
        self.dynamic_props = self.map_objects["dynamic_props"]
        self.interactive_props = self.map_objects["interactive_props"]
        self.background_props = self.map_objects["background_props"]
        self.player.position = self.map_objects["spawn"]
        self.animated_props = self.map_objects["animated_props"]
        self.diss_blocks = self.map_objects["diss_blocks"]
        self.items = self.map_objects["items"]
        self.camera = Camera(self.map_objects)
        self.current_map = mapFile

        if self.player.pushing:
            self.player.stop_pushing()

        self.boxes = []

        for obj in self.interactive_props:
            if obj.type == "box":
                self.boxes.append(obj)

    def run(self):

        self.ticks_ellapsed = 0

        self.pause_button = pygame.image.load("grafiki_dump/pauza.png").convert_alpha()
        self.pause_button = pygame.transform.scale(self.pause_button, (471, 78))
        # self.pause_button_rect = self.pause_button.get_rect(
        #     center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.pause_button_rect = self.pause_button.get_rect(
            center=(640, 360))


        self.reloadMap(self.starting_map)


        while True:

            self.mapLoader.render()
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())
            self.e_pressed = False

            # pygame.draw.rect(self.screen, (255, 0, 0), self.player.hitbox, 10)

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
                if keys[pygame.K_r]:

                    self.items[0].show()

                    # R key is pressed
                    # Your code for handling R key press goes here

                elif keys[pygame.K_t]:

                    self.items[0].hide()

                elif keys[pygame.K_e]:

                    self.e_pressed = True

                elif keys[pygame.K_u]:
                    self.show_falling_blocks()
                    break

                elif keys[pygame.K_z]:
                    self.show_lights()
                    break


                if not self.paused:
                    self.player.movement(event, self.camera)

            if not self.paused:

                self.player.tick_update(self.static_props, self.camera, self.boxes, self.diss_blocks)

                if self.player.position[1] > 900:
                    self.reloadMap(self.current_map)

                for obj in self.interactive_props:

                    obj.tick_update(self.player)
                    if obj.colliding and self.e_pressed:
                        if obj.type == "warp" and not self.player.pushing:
                            self.reloadMap(obj.destination)
                        elif obj.type == "warp_misc" and not self.player.pushing:
                            destination = obj.destination
                            if destination == 1:
                                self.show_falling_blocks()
                            if destination == 2:
                                self.show_lights()
                            break


                        elif obj.type == "box":
                            if not self.player.pushing:
                                self.player.start_pushing(obj)

                            elif obj is self.player.moving_object:
                                self.player.stop_pushing()

                for obj in self.animated_props:
                    obj.tick_update()

                for obj in self.diss_blocks:
                    obj.tick_update()

                for obj in self.items:
                    obj.tick_update(self.player)

                self.ticks_ellapsed += 1

            else:
                #pauza
                self.screen.blit(self.pause_button, self.pause_button_rect)
                keys = pygame.key.get_pressed()
                self.show_items()
                if keys[pygame.K_q]:
                    if self.player.pushing:
                        self.player.stop_pushing()
                    self.reloadMap(self.current_map)
                    self.paused = False

            self.clock.tick(fps)
            pygame.display.update()




if __name__ == "__main__":
    curr_player = Player('player1', [420, 0])
    game_instance = Game(curr_player)
    game_instance.showMenu()


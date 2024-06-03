import sys
import pygame
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


    def showMenu(self):
        self.mapLoader.loadMisc(self.menu)

    def show_falling_blocks(self):
        self.mapLoader.loadMisc(self.falling_blocks)

    def reloadMap(self, mapFile):


        self.map_objects = self.mapLoader.loadMap(mapFile)
        self.static_props = self.map_objects[0]
        self.void_props = self.map_objects[1]
        #self.dynamic_props = self.map_objects[2]
        self.interactive_props = self.map_objects[3]
        self.background_props = self.map_objects[4]
        self.player.position = self.map_objects[-1]
        self.camera = Camera(self.map_objects)

        self.boxes = []

        for obj in self.interactive_props:
            if obj.type == "box":
                self.boxes.append(obj)

    def run(self):

        self.ticks_ellapsed = 0

        self.pause_button = pygame.image.load("grafiki_dump/pauza.png")
        self.pause_button = pygame.transform.scale(self.pause_button, (471, 78))
        self.pause_button_rect = self.pause_button.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))


        # self.static_props = self.mapLoader.loadMap("maps/test2")
        # self.camera = Camera(self.static_props)

        self.reloadMap("maps/floor4")


        while True:

            self.mapLoader.render()
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())
            self.e_pressed = False

            #pygame.draw.rect(self.screen, (255, 0, 0), self.player.hitbox, 10)

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

                    self.reloadMap("maps/test2")

                    # R key is pressed
                    # Your code for handling R key press goes here

                elif keys[pygame.K_t]:

                    self.reloadMap("maps/test1")

                elif keys[pygame.K_e]:

                    self.e_pressed = True

                elif keys[pygame.K_u]:
                    self.show_falling_blocks()
                    break


                if not self.paused:
                    self.player.movement(event, self.camera)

            if not self.paused:

                self.player.tick_update(self.static_props, self.camera, self.boxes)

                for obj in self.interactive_props:
                    obj.tick_update(self.player)
                    if obj.colliding and self.e_pressed:
                        if obj.type == "warp":
                            self.reloadMap(obj.destination)

                        elif obj.type == "box":
                            if not self.player.pushing:
                                self.player.start_pushing(obj)

                            else:
                                self.player.stop_pushing()
            else:
                self.screen.blit(self.pause_button, self.pause_button_rect)

            self.clock.tick(fps)
            self.ticks_ellapsed += 1
            pygame.display.update()




if __name__ == "__main__":
    curr_player = Player('player1', [420, 0])
    game_instance = Game(curr_player)
    game_instance.showMenu()


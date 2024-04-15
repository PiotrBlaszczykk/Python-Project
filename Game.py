import sys
import pygame
from player import Player
import math
from grass import Grass
from map import Map
from cloud import Cloud
from deska import Deska
from kolumna import Kolumna

import time

from config import fps, fps_ratio
class Game:
    def __init__(self, player, grass, deska1, deska2, deska3, kolumna):
        pygame.init()
        pygame.display.set_caption('Escape from D17')
        self.player = player
        self.grass = grass
        self.deska1 = deska1
        self.deska2 = deska2
        self.deska3 = deska3
        self.kolumna = kolumna
        # self.screen = pygame.display.set_mode((840, 680))
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()


    def showMenu(self):
        playButton = pygame.image.load("menu/play_Button_transparent.png")
        playButton = pygame.transform.scale(playButton, (200, 150))
        button_width = playButton.get_width()
        button_height = playButton.get_height()
        cloud1 = Cloud([100, 100], [0, 100], 0.8, self.screen.get_width())
        cloud2 = Cloud([150, 150], [20, 150], 1, self.screen.get_width())
        cloud3 = Cloud([80, 80], [80, 300], 1.5, self.screen.get_width())
        cloud4 = Cloud([200, 200], [10, 350], 0.7, self.screen.get_width())
        cloud5 = Cloud([90, 90], [200, 300], 0.9, self.screen.get_width())
        cloud6 = Cloud([100, 100], [250, 380], 1.2, self.screen.get_width())
        clouds = [cloud1, cloud2, cloud3, cloud4, cloud5, cloud6]



        gameLogo = pygame.image.load("menu/logo_transparent.png")
        gameLogo = pygame.transform.scale(gameLogo, (350, 300))

        screen_width, screen_height = self.screen.get_size()

        playButtonPosition = [(screen_width - playButton.get_width()) / 2,
                              (screen_height - playButton.get_height()) / 2 + 50]
        gameLogoPosition = [(screen_width - gameLogo.get_width()) / 2 + 20,
                            (screen_height - gameLogo.get_height()) / 2 - 150]

        counter = 0
        #counter_flag = False
        while True:
            sine_movement = math.sin(counter) * 0.7

            """if counter <= 15 and counter_flag == False:
                playButtonPosition[1] += 0.25
                gameLogoPosition[1] += 0.25
                counter += 0.25
            if counter > 15:                                        This version makes the logo and button move always at the same speed.
                counter_flag = True                                 For now I've done sinus movement so its smoother.
            if counter > 0 and counter_flag == True :
                playButtonPosition[1] -= 0.25
                gameLogoPosition[1] -= 0.25
                counter -= 0.25
            if counter <= 0:
                counter_flag = False"""

            playButtonPosition[1] += sine_movement
            gameLogoPosition[1] += sine_movement
            counter += 0.02
            for i in range(6):
                clouds[i].move()

            self.screen.fill((68, 15, 104))
            for i in range(6):
                self.screen.blit(clouds[i].image, (clouds[i].position[0], clouds[i].position[1]))
            self.screen.blit(gameLogo, (gameLogoPosition[0], gameLogoPosition[1]))
            self.screen.blit(playButton, (playButtonPosition[0], playButtonPosition[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (playButtonPosition[0] <= mouse_x <= playButtonPosition[0] + button_width and
                            playButtonPosition[1] <= mouse_y <= playButtonPosition[1] + button_height):
                        self.run()
                        break
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):

        while True:
            self.screen.fill((14, 219, 248))

            self.screen.blit(self.player.getAppearance(), self.player.getPosition())

            self.screen.blit(self.grass.getAppearance(), self.grass.getPosition())

            self.screen.blit(self.deska1.getAppearance(), self.deska1.getPosition())
            self.screen.blit(self.deska2.getAppearance(), self.deska2.getPosition())
            self.screen.blit(self.deska3.getAppearance(), self.deska3.getPosition())
            self.screen.blit(self.kolumna.getAppearance(), self.kolumna.getPosition())

            self.player.tick_update([self.grass, self.deska1, self.deska2, self.deska3, self.kolumna])

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.player.movement(event)

            pygame.display.update()
            self.clock.tick(fps)



curr_player = Player('player1', [0, 0], 'main character/main character looking right.jpg')
grass = Grass('grass', [0, 664])

deska1 = Deska('deska1', [700, 580])
deska2 = Deska('deska2', [200, 500])
deska3 = Deska('deska3', [1000, 420])

kolumna = Kolumna('kolumna', [1196, -208])

# deska4 = Deska('deska4', [200, 500])
# deska5 = Deska('deska5', [200, 500])


game_instance = Game(curr_player, grass, deska1, deska2, deska3, kolumna)
game_instance.showMenu()
#game_instance.run()


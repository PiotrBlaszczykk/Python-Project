import sys
import pygame
import math
from cloud import Cloud


class Menu:
    def __init__(self, screen, clock, motherClass):
        self.screen = screen
        self.clock = clock
        self.motherClass = motherClass

    def render(self):
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
        # counter_flag = False
        while True:
            sine_movement = math.sin(counter) * 0.7
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
                        self.motherClass.run()
                        break
            pygame.display.flip()
            self.clock.tick(60)
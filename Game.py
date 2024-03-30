import sys
import pygame
from player import Player
from map import Map
class Game:
    def __init__(self, player):
        pygame.init()
        pygame.display.set_caption('Escape from D17')
        self.player = player
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.playButton = pygame.image.load("menu/play Button.jpg")
        self.playButton = pygame.transform.scale(self.playButton, (200, 150))
        self.playButtonPosition = [210, 150]
        self.button_width, self.button_height = self.playButton.get_size()


    def showMenu(self):
        while True:

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.playButton, (self.playButtonPosition[0], self.playButtonPosition[1]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (self.playButtonPosition[0] <= mouse_x <= self.playButtonPosition[0] + self.button_width and
                            self.playButtonPosition[1] <= mouse_y <= self.playButtonPosition[1] + self.button_height):
                        self.run()
                        break
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))
            self.player.tickUpdate()
            self.screen.blit(self.player.getAppearance(), self.player.getPosition())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.player_movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.player.player_movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.player.player_movement[2] = True
                    if event.key == pygame.K_RIGHT:
                        self.player.player_movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.player.player_movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.player.player_movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.player.player_movement[2] = False
                    if event.key == pygame.K_RIGHT:
                        self.player.player_movement[3] = False

            pygame.display.update()
            self.clock.tick(60)

curr_player = Player('player1', [0, 0], 'main character/main character looking right.jpg')
game_instance = Game(curr_player)
game_instance.showMenu()
#game_instance.run()


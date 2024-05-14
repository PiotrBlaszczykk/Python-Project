import pygame
from config import fps_ratio
import os
from map_functions.ImageCache import ImageCache
from player_details.playerImages import PlayerImages

from enum import Enum

class PlayerState(Enum):
    STANDING_RIGHT = 1
    STANDING_LEFT = 2
    AIRBORNE_RIGHT = 3
    AIRBORNE_LEFT = 4
    MOVING_RIGHT = 5
    MOVING_LEFT = 6
    # STANDING_RIGHT2 = 7
    # STANDING_LEFT2 = 8
    # MOVING_RIGHT2 = 9
    # MOVING_LEFT2 = 10

class Player():
    def __init__(self, playerName, playerPosition):
        self.name = playerName
        self.position = playerPosition

        # self.appearance = pygame.image.load("MCgraphics/MC_standing_R_1.png")
        # self.hitbox = self.appearance.get_rect(topleft=self.position)
        #self.inventory = []

        self.player_movement = [False, False, False, False]  #0-up, 1-down, 2-left, 3-right

        self.vertical_velocity = 0
        self.horizontal_velocity = 0

        #stałe * fps_ratio, przyspiesznia * fps_ratio ^ 2
        self.max_horizontal_velocity = 5 * fps_ratio
        self.gravity = 0.3 * (fps_ratio**2)
        self.friction = 0.15 * (fps_ratio**2)
        self.speed_up = 1.8 * (fps_ratio**2)
        self.max_vertical_velocity = 7 * fps_ratio
        self.min_vertical_velocity = -10 * fps_ratio

        self.ticks_elapsed = 0
        # self.change_outfit1 = 180
        # self.change_outfit2 = 100

        self.airborne = True

        self.images = PlayerImages()

        self.appearance = self.images.Moving_left1
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        # self.hitbox = pygame.Rect(self.position[0] + 18, self.position[1] + 9, 102, 144)

        self.playerState = PlayerState.STANDING_RIGHT
        self.last_move_was_right = True

    def update_appearance(self):

        if self.playerState == PlayerState.AIRBORNE_RIGHT:
            self.appearance = self.images.Airborne_right

        elif self.playerState == PlayerState.AIRBORNE_LEFT:
            self.appearance = self.images.Airborne_left

        elif self.playerState == PlayerState.STANDING_RIGHT:
            if self.ticks_elapsed % 170 < 85:
                self.appearance = self.images.Standing_right1
            else:
                self.appearance = self.images.Standing_right2

        elif self.playerState == PlayerState.STANDING_LEFT:
            if self.ticks_elapsed % 170 < 85:
                self.appearance = self.images.Standing_left1
            else:
                self.appearance = self.images.Standing_left2

        elif self.playerState == PlayerState.MOVING_RIGHT:
            if self.ticks_elapsed % 80 < 40:
                self.appearance = self.images.Moving_right1
            else:
                self.appearance = self.images.Moving_right2

        elif self.playerState == PlayerState.MOVING_LEFT:
            if self.ticks_elapsed % 80 < 40:
                self.appearance = self.images.Moving_left1
            else:
                self.appearance = self.images.Moving_left2

    def setPosition(self, playerPosition):
        self.position = playerPosition

    def apply_gravity(self, camera):

        if self.airborne:

            self.vertical_velocity += self.gravity

            if self.vertical_velocity > self.max_vertical_velocity:
                self.vertical_velocity = self.max_vertical_velocity
            #camera.setVerticalVelocity(-self.vertical_velocity)

            self.position[1] += self.vertical_velocity



    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def tick_update(self, static_props, camera):

        self.ticks_elapsed += 1

        # if self.ticks_elapsed > self.change_outfit1:
        #     self.ticks_elapsed = 0
        #
        # if self.ticks_elapsed > self.change_outfit1:
        #     self.ticks_elapsed = 0

        #ZWAŻKA NA KOLEJNOŚĆ!

        #self.position[0] = int(self.position[0])
        self.position[0] = 640
        self.position[1] = int(self.position[1])
        #w celu synchronizacji hitboxa z pozycja
        self.hitbox.topleft = self.position



        if self.player_movement[2]:  # Ruch w lewo
            self.horizontal_velocity -= self.speed_up
            self.last_move_was_right = False
            self.playerState = PlayerState.MOVING_LEFT
            if self.horizontal_velocity < -self.max_horizontal_velocity:
                self.horizontal_velocity = -self.max_horizontal_velocity
            camera.setHorizontalVelocity(-self.horizontal_velocity)

        elif self.player_movement[3]:  # Ruch w prawo
            self.horizontal_velocity += self.speed_up
            self.last_move_was_right = True
            self.playerState = PlayerState.MOVING_RIGHT
            if self.horizontal_velocity > self.max_horizontal_velocity:
                self.horizontal_velocity = self.max_horizontal_velocity
            camera.setHorizontalVelocity(- self.horizontal_velocity)

        else:
            #hamowanie
            if abs(self.horizontal_velocity) > 0.1 * fps_ratio:
                if self.horizontal_velocity >= 0:
                    self.horizontal_velocity -= self.friction
                    camera.setHorizontalVelocity(-self.horizontal_velocity)
                else:
                    self.horizontal_velocity += self.friction
                    camera.setHorizontalVelocity(-self.horizontal_velocity)

            else:
                self.horizontal_velocity = 0
                camera.setHorizontalVelocity(0)

        self.apply_gravity(camera)
        self.handle_collisions(static_props, camera)


        if self.horizontal_velocity == 0:
            if self.last_move_was_right:
                self.playerState = PlayerState.STANDING_RIGHT

            else:
                self.playerState = PlayerState.STANDING_LEFT

        if self.airborne:
            if self.horizontal_velocity > 0:
                self.playerState = PlayerState.AIRBORNE_RIGHT

            elif self.horizontal_velocity < 0:
                self.playerState = PlayerState.AIRBORNE_LEFT

            else:

                if self.last_move_was_right:
                    self.playerState = PlayerState.AIRBORNE_RIGHT
                else:
                    self.playerState = PlayerState.AIRBORNE_LEFT


        self.update_appearance()

        #self.position[0] += self.horizontal_velocity
        if not camera.isPlayerBlocked:
            camera.move()


    def jump(self):

        if not self.airborne:
            self.airborne = True
            self.position[1] -= 10
            self.vertical_velocity = -12 * fps_ratio



    def movement(self, event, camera):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.player_movement[2] = True
                self.player_movement[3] = False
            elif event.key == pygame.K_RIGHT:
                self.player_movement[3] = True
                self.player_movement[2] = False

            if event.key == pygame.K_UP:
                self.jump()

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.player_movement[2] = False
            elif event.key == pygame.K_RIGHT:
                self.player_movement[3] = False

        #hotfix z kamera
        self.flag = False

    def handle_collision(self, object, camera):

        #hitbox[ position[0], position[1], szerokosc, wysokosc]
        #funkcja handle_collision zwróci True, jeśli kolizja polega na tym, że
        #gracz stoi na ziemi, w przeciwnym wypadku zwraca False
        #jest to po to by dobrze ustalić paramentr airborne

        #kolizje poziome
        if object.hitbox.colliderect(self.hitbox[0] + 2*self.horizontal_velocity, self.hitbox[1], self.hitbox[2], self.hitbox[3]):
            self.horizontal_velocity = 0
            self.flag = True

        else:
            camera.isPlayerBlocked = False


        #kolizje pionowe
        if object.hitbox.colliderect(self.hitbox[0], self.hitbox[1] + self.vertical_velocity, self.hitbox[2], self.hitbox[3]):
            # + vertical velocity po to, żeby hitbox gracza nie wjechał wewnątrz hiboxu obiektu

            print("hit")
            if self.vertical_velocity >= 0 and self.airborne:
                #kolizja spadając
                self.vertical_velocity = 0
                self.position[1] = (object.hitbox.top - self.hitbox[3])
                return True

            elif self.vertical_velocity < 0:
                self.vertical_velocity = 0
                self.position[1] = (object.hitbox.bottom)
                return False

        elif object.hitbox.colliderect(self.hitbox[0], self.hitbox[1] + 5, self.hitbox[2], self.hitbox[3]):
            return True

        else:
            return False

    def handle_collisions(self, static_props, camera):

        #funkcja handle_collision zwróci True, jeśli kolizja polega na tym, że
        #gracz stoi na ziemi, w przeciwnym wypadku zwraca False
        #jest to po to by dobrze ustalić paramentr airborne

        self.airborne = True
        self.flag = False
        camera.isPlayerBlocked = False
        for obj in static_props:

            if self.handle_collision(obj, camera):
                self.airborne = False

        self.hitbox.topleft = self.position
        if self.flag:
            camera.isPlayerBlocked = True


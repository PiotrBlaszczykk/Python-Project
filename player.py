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
    PUSHING_RIGHT = 8
    PUSHING_LEFT = 9

class Player():
    def __init__(self, playerName, playerPosition):
        self.name = playerName
        self.position = playerPosition

        self.items = [False for _ in range(5)]

        self.player_movement = [False, False, False, False]  #0-up, 1-down, 2-left, 3-right

        self.vertical_velocity = 0
        self.horizontal_velocity = 0

        #stałe * fps_ratio, przyspiesznia * fps_ratio ^ 2
        self.max_horizontal_velocity = 5 * fps_ratio
        self.max_pushing_velocity = 2.5 * fps_ratio
        self.gravity = 0.3 * (fps_ratio**2)
        self.friction = 0.15 * (fps_ratio**2)
        self.speed_up = 1.8 * (fps_ratio**2)
        self.max_vertical_velocity = 7 * fps_ratio
        self.min_vertical_velocity = -10 * fps_ratio

        self.ticks_elapsed = 0

        self.airborne = True
        self.pushing = False
        self.moving_object = None

        self.images = PlayerImages()

        self.appearance = self.images.Moving_left1
        self.hitbox = pygame.Rect(self.position[0] + 15, self.position[1], 108, 162)

        self.playerState = PlayerState.STANDING_RIGHT
        self.last_move_was_right = True

    def update_appearance(self):


        if self.playerState == PlayerState.AIRBORNE_RIGHT:
            self.appearance = self.images.Airborne_right

        elif self.playerState == PlayerState.AIRBORNE_LEFT:
            self.appearance = self.images.Airborne_left

        elif self.playerState == PlayerState.STANDING_RIGHT:
            if self.ticks_elapsed % (170 / fps_ratio) < (85 / fps_ratio):
                self.appearance = self.images.Standing_right1
            else:
                self.appearance = self.images.Standing_right2

        elif self.playerState == PlayerState.STANDING_LEFT:
            if self.ticks_elapsed % (170 / fps_ratio) < (85 / fps_ratio):
                self.appearance = self.images.Standing_left1
            else:
                self.appearance = self.images.Standing_left2

        elif self.playerState == PlayerState.MOVING_RIGHT:
            if self.ticks_elapsed % (80 / fps_ratio) < (40 / fps_ratio):
                self.appearance = self.images.Moving_right1
            else:
                self.appearance = self.images.Moving_right2

        elif self.playerState == PlayerState.MOVING_LEFT:
            if self.ticks_elapsed % (80 / fps_ratio) < (40 / fps_ratio):
                self.appearance = self.images.Moving_left1
            else:
                self.appearance = self.images.Moving_left2

        elif self.playerState == PlayerState.PUSHING_RIGHT:

            if self.horizontal_velocity == 0:
                self.appearance = self.images.Pushing_Right_idle

            else:
                if self.ticks_elapsed % (80 / fps_ratio) < (40 / fps_ratio):
                    self.appearance = self.images.Pushing_Right_1
                else:
                    self.appearance = self.images.Pushing_Right_2

        elif self.playerState == PlayerState.PUSHING_LEFT:

            if self.horizontal_velocity == 0:
                self.appearance = self.images.Pushing_Left_idle

            else:
                if self.ticks_elapsed % (80 / fps_ratio) < (40 / fps_ratio):
                    self.appearance = self.images.Pushing_Left_1
                else:
                    self.appearance = self.images.Pushing_Left_2



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

    def start_pushing(self, obj):
        self.moving_object = obj
        obj.pushed = True
        self.pushing = True

        if self.last_move_was_right:
            self.playerState= PlayerState.PUSHING_RIGHT
        else:
            self.playerState = PlayerState.PUSHING_LEFT


    def stop_pushing(self):
        self.pushing = False
        self.moving_object.pushed = False
        self.moving_object = None

        if self.playerState == PlayerState.PUSHING_RIGHT:
            self.playerState = PlayerState.STANDING_RIGHT
        else:
            self.playerState = PlayerState.STANDING_LEFT

        self.horizontal_velocity = 0

    def tick_update(self, static_props, camera, boxes, diss_blocks):

        self.ticks_elapsed += 1
        if self.ticks_elapsed == 1360: #NWW 170 i 80
            self.ticks_elapsed = 0

        #ZWAŻKA NA KOLEJNOŚĆ!

        self.position[0] = 640
        self.position[1] = int(self.position[1])

        if self.pushing:
            if self.playerState == PlayerState.PUSHING_RIGHT:
                self.hitbox = pygame.Rect(self.position[0] + 15, self.position[1], 290, 162)
            else:
                self.hitbox = pygame.Rect(self.position[0] - 170, self.position[1], 290, 162)
        else:
            self.hitbox = pygame.Rect(self.position[0] + 15, self.position[1], 108, 162)

        if self.player_movement[2]:  # Ruch w lewo

            if not self.pushing:
                self.horizontal_velocity -= self.speed_up
                self.last_move_was_right = False
                self.playerState = PlayerState.MOVING_LEFT
            elif self.playerState == PlayerState.PUSHING_LEFT:
                self.horizontal_velocity -= (self.speed_up * 0.5)
                self.last_move_was_right = False


            if self.horizontal_velocity < -self.max_horizontal_velocity:
                self.horizontal_velocity = -self.max_horizontal_velocity

            if self.pushing and self.horizontal_velocity < self.max_pushing_velocity:
                self.horizontal_velocity = -self.max_pushing_velocity

            camera.setHorizontalVelocity(-self.horizontal_velocity)

        elif self.player_movement[3]:  # Ruch w prawo

            if not self.pushing:
                self.horizontal_velocity += self.speed_up
                self.last_move_was_right = True
                self.playerState = PlayerState.MOVING_RIGHT
            elif self.playerState == PlayerState.PUSHING_RIGHT:
                self.horizontal_velocity += (self.speed_up * 0.5)
                self.last_move_was_right = True


            if self.horizontal_velocity > self.max_horizontal_velocity:
                self.horizontal_velocity = self.max_horizontal_velocity

            if self.pushing and self.horizontal_velocity > self.max_pushing_velocity:
                self.horizontal_velocity = self.max_pushing_velocity

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

        self.handle_collisions(static_props, camera, boxes, diss_blocks)


        if not self.pushing:

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

        if self.pushing:
            self.moving_object.move(self.horizontal_velocity)


        self.update_appearance()

        if not camera.isPlayerBlocked:
            camera.move()


    def jump(self):

        if not self.airborne:
            self.airborne = True
            self.position[1] -= 10
            self.vertical_velocity = -12 * fps_ratio



    def movement(self, event, camera):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and self.playerState != PlayerState.PUSHING_RIGHT:
                self.player_movement[2] = True
                self.player_movement[3] = False
            elif event.key == pygame.K_RIGHT and self.playerState != PlayerState.PUSHING_LEFT:
                self.player_movement[3] = True
                self.player_movement[2] = False

            if event.key == pygame.K_UP and not self.pushing:
                self.jump()

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.player_movement[2] = False
            elif event.key == pygame.K_RIGHT:
                self.player_movement[3] = False

        #hotfix z kamera
        self.flag = False

    def handle_collision(self, object, camera):

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

    def handle_collisions(self, static_props, camera, boxes, diss_blocs):

        #funkcja handle_collision zwróci True, jeśli kolizja polega na tym, że
        #gracz stoi na ziemi, w przeciwnym wypadku zwraca False
        #jest to po to by dobrze ustalić paramentr airborne

        self.airborne = True
        self.flag = False
        camera.isPlayerBlocked = False
        for obj in static_props:

            if self.handle_collision(obj, camera):
                self.airborne = False

        for obj in diss_blocs:

            if self.handle_collision(obj, camera):
                self.airborne = False

        if not self.pushing:
            for obj in boxes:

                if self.handle_collision(obj, camera):
                    self.airborne = False

        else:
            for obj in boxes:
                if self.moving_object is not obj:
                    self.handle_collision(obj, camera)

        self.hitbox.topleft = self.position
        if self.flag:
            camera.isPlayerBlocked = True


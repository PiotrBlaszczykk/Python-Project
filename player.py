import pygame
from config import fps_ratio
class Player():
    def __init__(self, playerName, playerPosition, imagePath):
        self.name = playerName
        self.position = playerPosition
        self.appearance = pygame.image.load(imagePath)
        self.hitbox = self.appearance.get_rect(topleft=self.position)
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

        self.airborne = True

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

        #ZWAŻKA NA KOLEJNOŚĆ!

        #self.position[0] = int(self.position[0])
        self.position[0] = 640
        self.position[1] = int(self.position[1])
        #w celu synchronizacji hitboxa z pozycja
        self.hitbox.topleft = self.position


        if self.player_movement[2]:  # Ruch w lewo
            self.horizontal_velocity -= self.speed_up
            if self.horizontal_velocity < -self.max_horizontal_velocity:
                self.horizontal_velocity = -self.max_horizontal_velocity
            camera.setHorizontalVelocity(-self.horizontal_velocity)

        elif self.player_movement[3]:  # Ruch w prawo
            self.horizontal_velocity += self.speed_up
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


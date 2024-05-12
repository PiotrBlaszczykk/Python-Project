import pygame
from config import fps_ratio
from player_details.animation_enum import State

class Player():
    def __init__(self, playerName, playerPosition, imagePath):
        self.name = playerName
        self.position = playerPosition
        self.appearance = pygame.image.load(imagePath)
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        #self.inventory = []
        self.player_movement = [False, False, False, False]

        self.state = State.IDLE_RIGHT

        self.vertical_velocity = 0
        self.horizontal_velocity = 0

        #stałe * fps_ratio, przyspiesznia * fps_ratio ^ 2
        self.max_horizontal_velocity = 7 * fps_ratio
        self.gravity = 0.3 * (fps_ratio**2)
        self.friction = 0.2 * (fps_ratio**2)
        self.speed_up = 1.8 * (fps_ratio**2)
        self.max_vertical_velocity = 7 * fps_ratio
        self.min_vertical_velocity = -10 * fps_ratio

        self.airborne = True

        self.ticks_since_last_frame = 0
        self.ticks_per_frame = 10  # Liczba ticków między zmianami klatek

    def load_images(self, imagePath):
        self.images = {
            State.IDLE_LEFT: [pygame.image.load(f"{imagePath}/standing_l1.png"),
                              pygame.image.load(f"{imagePath}/standing_l2.png")],
            State.IDLE_RIGHT: [pygame.image.load(f"{imagePath}/standing_r1.png"),
                               pygame.image.load(f"{imagePath}/standing_r2.png")]
        }

    def setPosition(self, playerPosition):
        self.position = playerPosition

    def apply_gravity(self):

        if self.airborne:

            self.vertical_velocity += self.gravity

            if self.vertical_velocity > self.max_vertical_velocity:
                self.vertical_velocity = self.max_vertical_velocity

            self.position[1] += self.vertical_velocity


    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def tick_update(self, objects):

        #ZWAŻKA NA KOLEJNOŚĆ!

        self.position[0] = int(self.position[0])
        self.position[1] = int(self.position[1])
        #w celu synchronizacji hitboxa z pozycja
        self.hitbox.topleft = self.position


        if self.player_movement[2]:  # Ruch w lewo
            self.horizontal_velocity -= self.speed_up
            if self.horizontal_velocity < -self.max_horizontal_velocity:
                self.horizontal_velocity = -self.max_horizontal_velocity

        elif self.player_movement[3]:  # Ruch w prawo
            self.horizontal_velocity += self.speed_up
            if self.horizontal_velocity > self.max_horizontal_velocity:
                self.horizontal_velocity = self.max_horizontal_velocity

        else:
            #hamowanie
            if abs(self.horizontal_velocity) > 0.2 * fps_ratio:
                if self.horizontal_velocity >= 0:
                    self.horizontal_velocity -= self.friction
                else:
                    self.horizontal_velocity += self.friction

            else:
                self.horizontal_velocity = 0

        self.apply_gravity()
        self.handle_collisions(objects)

        self.position[0] += self.horizontal_velocity

        #animacja
        self.update_animation()

    def jump(self):

        if not self.airborne:
            self.airborne = True
            #self.position[1] -= 10
            self.vertical_velocity = -12 * fps_ratio

    def update_state(self):
        if self.player_movement[2]:  # Ruch w lewo
            self.state = State.MOVING_LEFT
        elif self.player_movement[3]:  # Ruch w prawo
            self.state = State.MOVING_RIGHT
        else:
            # Załóżmy, że jest to stan spoczynku
            if self.state in [State.MOVING_LEFT, State.IDLE_LEFT]:
                self.state = State.IDLE_LEFT
            else:
                self.state = State.IDLE_RIGHT

    def update_animation(self):
        self.ticks_since_last_frame += 1  # Inkrementuj licznik ticków
        if self.ticks_since_last_frame >= self.ticks_per_frame:
            self.current_frame = (self.current_frame + 1) % len(self.images[self.state])
            self.appearance = self.images[self.state][self.current_frame]
            self.ticks_since_last_frame = 0  # Resetuj licznik ticków

    def movement(self, event):

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


    def handle_collision(self, object):

        #hitbox[ position[0], position[1], szerokosc, wysokosc]
        #funkcja handle_collision zwróci True, jeśli kolizja polega na tym, że
        #gracz stoi na ziemi, w przeciwnym wypadku zwraca False
        #jest to po to by dobrze ustalić paramentr airborne

        #kolizje poziome
        if object.hitbox.colliderect(self.hitbox[0] + self.horizontal_velocity, self.hitbox[1], self.hitbox[2], self.hitbox[3]):
            self.horizontal_velocity = 0


        #kolizje pionowe
        if object.hitbox.colliderect(self.hitbox[0], self.hitbox[1] + self.vertical_velocity, self.hitbox[2], self.hitbox[3]):
            # + vertical velocity po to, żeby hitbox gracza nie wjechał wewnątrz hiboxu obiektu

            print("hit")
            if self.vertical_velocity >= 0:
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

    def handle_collisions(self, objects):

        #funkcja handle_collision zwróci True, jeśli kolizja polega na tym, że
        #gracz stoi na ziemi, w przeciwnym wypadku zwraca False
        #jest to po to by dobrze ustalić paramentr airborne

        self.airborne = True
        for obj in objects:

            if self.handle_collision(obj):
                self.airborne = False

        self.hitbox.topleft = self.position


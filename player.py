import pygame

class Player():
    def __init__(self, playerName, playerPosition, imagePath):
        self.name = playerName
        self.position = playerPosition
        self.appearance = pygame.image.load(imagePath)
        self.hitbox = self.appearance.get_rect(topleft=self.position)
        #self.inventory = []
        self.player_movement = [False, False, False, False]
        self.vertical_velocity = 0
        self.horizontal_velocity = 0
        self.max_horizontal_velocity = 4
        self.gravity = 0.3
        self.friction = 0.15
        self.speed_up = 1.8
        self.max_vertical_velocity = 5
        self.min_vertical_velocity = -10
        self.airborne = True

    def setPosition(self, playerPosition):
        self.position = playerPosition

    def apply_gravity(self):

        if self.airborne:

            if self.vertical_velocity < self.max_vertical_velocity:
                self.vertical_velocity += self.gravity

            self.position[1] += self.vertical_velocity


    def getPosition(self):
        return self.position

    def getAppearance(self):
        return self.appearance

    def tick_update(self, objects):
        self.hitbox.topleft = self.position
        self.handle_collisions(objects)
        self.apply_gravity()

        if self.player_movement[2]:  # Ruch w lewo
            if self.horizontal_velocity > -self.max_horizontal_velocity:
                self.horizontal_velocity -= self.speed_up

        elif self.player_movement[3]:  # Ruch w prawo
            if self.horizontal_velocity < self.max_horizontal_velocity:
                self.horizontal_velocity += self.speed_up
        else:
            # Zastosowanie tarcia do zatrzymywania gracza, gdy żaden klawisz nie jest naciskany
            if abs(self.horizontal_velocity) > 0.1:
                if self.horizontal_velocity >= 0:
                    self.horizontal_velocity -= self.friction
                else:
                    self.horizontal_velocity += self.friction

            else:
                self.horizontal_velocity = 0

        self.position[0] += self.horizontal_velocity


    def stop_vertical(self):
        self.vertical_velocity = 0
        self.airborne = False

    def jump(self):

        if not self.airborne:
            self.airborne = True
            self.position[1] -= 7
            # hotfix, trzeba dopracować aby "nie wchodził" rozpedzony w hitbox innego obiektu
            self.vertical_velocity -= 10


    def movement(self, event):

        if event.type == pygame.KEYDOWN:
            print(f"Key down: {pygame.key.name(event.key)}")
            if event.key == pygame.K_LEFT:
                self.player_movement[2] = True
                self.player_movement[3] = False
            elif event.key == pygame.K_RIGHT:
                self.player_movement[3] = True
                self.player_movement[2] = False

            if event.key == pygame.K_UP:
                self.jump()

        elif event.type == pygame.KEYUP:
            print(f"Key up: {pygame.key.name(event.key)}")
            if event.key == pygame.K_LEFT:
                self.player_movement[2] = False
            elif event.key == pygame.K_RIGHT:
                self.player_movement[3] = False


    def handle_collisions(self, objects):

        for obj in objects:
            if self.hitbox.colliderect(obj.hitbox):
                self.airborne = False
                self.vertical_velocity = 0
                #print(f"Collision at: {self.position[1]}")


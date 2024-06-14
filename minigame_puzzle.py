import random
import pygame

class PuzzlePiece:
    def __init__(self, image, position, rect, solvedPosition):
        self.image = image
        self.position = position
        self.rect = rect
        self.solvedPosition = solvedPosition

class minigame_puzzle:
    def __init__(self, screen, clock, motherClass):
        self.screen = screen
        self.clock = clock
        self.motherClass = motherClass
        self.load_image()
        self.pieces_solution = []
        self.selected_piece = None
        self.target_area_rect = pygame.Rect((screen.get_width() - self.image_width) // 2,
                                            (screen.get_height() - self.image_height) // 2,
                                            self.image_width, self.image_height)
        self.create_pieces()

    def load_image(self):
        self.image = pygame.image.load('minigames/puzzle/graphics/logo AGH do gry.png')
        self.image = pygame.transform.scale(self.image, (500, 500))
        self.image_width, self.image_height = self.image.get_size()

    def check_solution(self):
        for piece in self.pieces:
            if piece.solvedPosition != piece.position:
                return False
        return True

    def create_pieces(self):
        self.pieces = []
        divider = 2
        piece_width = self.image_width // divider
        piece_height = self.image_height // divider
        self.piece_width, self.piece_height = piece_width, piece_height

        all_positions = [(self.target_area_rect.x + x * piece_width, self.target_area_rect.y + y * piece_height)
                         for y in range(divider) for x in range(divider)]

        for row in range(divider):
            for col in range(divider):
                x = col * piece_width
                y = row * piece_height
                piece_image = self.image.subsurface((x, y, piece_width, piece_height))
                position = (self.target_area_rect.x + x, self.target_area_rect.y + y)
                solvedPosition = (self.target_area_rect.x + x, self.target_area_rect.y + y)
                rect = pygame.Rect(position[0], position[1], piece_width, piece_height)
                self.pieces.append(PuzzlePiece(piece_image, position, rect, solvedPosition))

        random.shuffle(all_positions)
        for idx, piece in enumerate(self.pieces):
            new_position = all_positions[idx]
            piece.rect.topleft = new_position
            piece.position = new_position

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_down(event)

            self.screen.fill((255, 255, 255))
            self.draw_target_area()
            self.draw_pieces()
            pygame.display.flip()
            self.clock.tick(60)

            if self.check_solution():
                print("Puzzle Solved!")
                self.motherClass.player.items[4] = True
                running = False
        else:
            return True
    def handle_mouse_button_down(self, event):
        for piece in self.pieces:
            if piece.rect.collidepoint(event.pos):
                self.selected_piece = piece
                break

    def handle_key_down(self, event):
        if self.selected_piece:
            if event.key == pygame.K_UP:
                self.move_piece(self.selected_piece, 0, -self.piece_height)
            elif event.key == pygame.K_DOWN:
                self.move_piece(self.selected_piece, 0, self.piece_height)
            elif event.key == pygame.K_LEFT:
                self.move_piece(self.selected_piece, -self.piece_width, 0)
            elif event.key == pygame.K_RIGHT:
                self.move_piece(self.selected_piece, self.piece_width, 0)

    def move_piece(self, piece, dx, dy):
        new_x = piece.rect.x + dx
        new_y = piece.rect.y + dy
        new_rect = piece.rect.move(dx, dy)

        for other_piece in self.pieces:
            if other_piece != piece and new_rect.colliderect(other_piece.rect):
                return

        piece.rect.x = new_x
        piece.rect.y = new_y
        piece.position = (new_x, new_y)

    def draw_target_area(self):
        border_thickness = 10
        outer_rect = self.target_area_rect.inflate(border_thickness * 2, border_thickness * 2)
        pygame.draw.rect(self.screen, (200, 200, 200), outer_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.target_area_rect)

    def draw_pieces(self):
        for piece in self.pieces:
            self.screen.blit(piece.image, piece.rect.topleft)
            if piece == self.selected_piece:
                pygame.draw.rect(self.screen, (255, 0, 0), piece.rect, 3)


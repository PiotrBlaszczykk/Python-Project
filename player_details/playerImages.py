import pygame

def load_image(path):
    scale = (138, 162)
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, scale)
    return image

class PlayerImages():

    def __init__(self):

        self.Standing_right1 = load_image("MCgraphics/MC_standing_R_1.png")
        self.Standing_left1 = load_image("MCgraphics/MC_standing_L_1.png")
        self.Airborne_right = load_image("MCgraphics/MC_jumping_R.png")
        self.Airborne_left = load_image("MCgraphics/MC_jumping_L.png")
        self.Moving_right1 = load_image("MCgraphics/MC_walking_R_1.png")
        self.Moving_left1 = load_image("MCgraphics/MC_walking_L_1.png")
        self.Standing_right2 = load_image("MCgraphics/MC_standing_R_2.png")
        self.Standing_left2 = load_image("MCgraphics/MC_standing_L_2.png")
        self.Moving_right2 = load_image("MCgraphics/MC_walking_R_2.png")
        self.Moving_left2 = load_image("MCgraphics/MC_walking_L_2.png")

        self.Pushing_Right_idle = load_image("MCgraphics/MC_pushing_R_idle.png")
        self.Pushing_Left_idle = load_image("MCgraphics/MC_pushing_L_idle.png")
        self.Pushing_Right_1 = load_image("MCgraphics/MC_pushing_R_1.png")
        self.Pushing_Right_2 = load_image("MCgraphics/MC_pushing_R_2.png")
        self.Pushing_Left_1 = load_image("MCgraphics/MC_pushing_L_1.png")
        self.Pushing_Left_2 = load_image("MCgraphics/MC_pushing_L_2.png")


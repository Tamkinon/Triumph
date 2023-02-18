import pygame
pygame.font.init()
tile_size = 48
screen_width = 1920
screen_height = 1080
score_font = pygame.font.Font("assets/Pixeltype.ttf", 85)
time_font = pygame.font.Font("assets/Pixeltype.ttf", 60)


class GameStates:
    TITLE_SCREEN = 'title'
    ANIMATION = 'animation'
    GAMEPLAY = 'gaming'

import pygame


class TitleAnimation:
    ANIMATION = []
    for i in range(1, 13):
        image = pygame.image.load(f'assets/title_animation/title_animation{i}.png').convert_alpha()
        ANIMATION.append(image)

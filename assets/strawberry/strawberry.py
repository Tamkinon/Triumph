import pygame


class Strawberry(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/strawberry/strawberry.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

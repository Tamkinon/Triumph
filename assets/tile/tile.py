import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft=pos)


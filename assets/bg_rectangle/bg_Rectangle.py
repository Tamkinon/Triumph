import pygame
import random


class BgRectangle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((random.randrange(100, 500, 1), random.randrange(30, 60, 1)))
        self.image.fill((29, 43, 83))
        self.rect = self.image.get_rect(midright=(576, random.randrange(196, 884, 1)))
        self.vel = random.randrange(7, 13, 1)

    def update(self):
        self.rect.x += self.vel
        if self.rect.left > 1344:
            self.kill()

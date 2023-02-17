import pygame
import random


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        random.seed(pos[0] + pos[1])
        self.flipX = random.choice([True, False])
        self.flipY = random.choice([True, False])
        self.image = pygame.image.load('assets/particle/particle_1.png')
        self.image = pygame.transform.flip(self.image, self.flipX, self.flipY)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.index = 0
        self.update()

    def update(self):
        self.index += 1
        if self.index % 5 == 0:
            self.rect.x += 6
        if self.index == 10:
            self.image = pygame.image.load('assets/particle/particle_2.png')
            self.image = pygame.transform.flip(self.image, self.flipX, self.flipY)
        elif self.index == 20:
            self.image = pygame.image.load('assets/particle/particle_3.png')
            self.image = pygame.transform.flip(self.image, self.flipX, self.flipY)
        elif self.index == 30:
            self.kill()

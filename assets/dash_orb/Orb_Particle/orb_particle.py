import pygame


class OrbParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/dash_orb/Orb_Particle/orb_particle_1.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.index = 0
        self.update()

    def update(self):
        self.index += 1
        if self.index == 10:
            self.image = pygame.image.load('assets/dash_orb/Orb_Particle/orb_particle_2.png')
        elif self.index == 20:
            self.image = pygame.image.load('assets/dash_orb/Orb_Particle/orb_particle_3.png')
        elif self.index == 30:
            self.kill()

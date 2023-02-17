import pygame


class DeathParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/death_particle/death_particle1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (366, 366))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.index = 1

    def update(self):
        self.index += 0.5
        if self.index <= 8:
            if self.index % 1 == 0:
                self.image = pygame.image.load('assets/death_particle/death_particle{}.png'.format(int(self.index)))
                self.image = pygame.transform.scale(self.image, (366, 366))
        else:
            self.kill()


class SpawnParticle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/death_particle/death_particle8.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (366, 366))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.index = 1

    def update(self):
        self.index += 0.5
        if self.index <= 8:
            if self.index % 1 == 0:
                self.image = pygame.image.load('assets/death_particle/death_particle{}.png'.format(9 - int(self.index)))
                self.image = pygame.transform.scale(self.image, (366, 366))
        else:
            self.kill()
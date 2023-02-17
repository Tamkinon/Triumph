import pygame


class DashOrb(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.state = 1
        self.time = 0
        self.image = pygame.image.load("assets/dash_orb/orb_on.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if self.state == 0:
            self.image = pygame.image.load("assets/dash_orb/orb_off.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
            self.time += 1
        else:
            self.image = pygame.image.load("assets/dash_orb/orb_on.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
        if self.time == 180:
            self.state = 1
            self.time = 0

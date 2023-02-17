import pygame


class SpikeDown(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/spike/spike_down.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class SpikeLeft(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/spike/spike_left.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class SpikeRight(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/spike/spike_right.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class SpikeUp(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/spike/spike_up.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

import pygame


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/flag/flag1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (96, 48))
        self.rect = self.image.get_rect(topleft=pos)
        self.index = 0
        self.touched = False

    def update(self):
        self.index += 1
        if self.index % 30 == 0:
            self.image = pygame.image.load('assets/flag/flag3.png')
            self.image = pygame.transform.scale(self.image, (96, 48))
        elif self.index % 20 == 0:
            self.image = pygame.image.load('assets/flag/flag2.png')
            self.image = pygame.transform.scale(self.image, (96, 48))
        elif self.index % 10 == 0:
            self.image = pygame.image.load('assets/flag/flag1.png')
            self.image = pygame.transform.scale(self.image, (96, 48))

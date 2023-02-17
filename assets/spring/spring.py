import pygame


class Spring(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/spring/spring.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.state = 1
        self.time = 0

    def update(self):
        if self.state == 0:
            self.image = pygame.image.load("assets/spring/spring_down.png").convert_alpha()
            self.time += 1
        else:
            self.image = pygame.image.load("assets/spring/spring.png").convert_alpha()
        if self.time == 26:
            self.state = 1
            self.time = 0

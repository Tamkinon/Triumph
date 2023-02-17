import pygame


class VanishBox(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.state = 0
        self.time = 0
        self.time_start = -1
        self.image = pygame.image.load("assets/vanish_box/vanish_box_0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        if self.state == 0:
            if self.time_start >= 0:
                self.time_start += 1
                if self.time_start == 5:
                    self.image = pygame.image.load("assets/vanish_box/vanish_box_1.png").convert_alpha()
                    self.image = pygame.transform.scale(self.image, (48, 48))
                elif self.time_start == 10:
                    self.image = pygame.image.load("assets/vanish_box/vanish_box_2.png").convert_alpha()
                    self.image = pygame.transform.scale(self.image, (48, 48))
                elif self.time_start == 15:
                    self.image = pygame.image.load("assets/vanish_box/vanish_box_3.png").convert_alpha()
                    self.image = pygame.transform.scale(self.image, (48, 48))
                elif self.time_start > 20:
                    self.image = pygame.image.load("assets/vanish_box/vanish_box_0.png").convert_alpha()
                    self.image = pygame.transform.scale(self.image, (48, 48))
        else:
            self.time += 1
        if self.time == 10:
            self.image = pygame.image.load("assets/vanish_box/vanish_box_breaking_1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
        elif self.time == 20:
            self.image = pygame.image.load("assets/vanish_box/vanish_box_breaking_2.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
        elif self.time == 30:
            self.state = 2
            self.image.set_alpha(0)
        if self.time == 120:
            self.state = 0
            self.image = pygame.image.load("assets/vanish_box/vanish_box_0.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (48, 48))
            self.image.set_alpha(255)
            self.time = 0
            self.time_start = 0

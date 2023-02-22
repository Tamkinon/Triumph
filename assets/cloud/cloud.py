import pygame


class Cloud(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.state = 0
        self.image = pygame.image.load("assets/cloud/cloud.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (96, 48))
        self.rect = self.image.get_rect(topleft=pos)
        self.vel = 3 * direction

    def update(self):
        self.rect.x += self.vel
        if self.rect.left > 1344:
            self.rect.right = 576
        elif self.rect.right < 576:
            self.rect.left = 1344

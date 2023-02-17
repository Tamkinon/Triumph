import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.index = 1
        self.image = pygame.image.load('assets/strawberry/score/score{}.png'.format(self.index)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos

    def update(self):
        self.index += 0.5
        if self.index <= 30:
            if self.index % 1 == 0:
                self.image = pygame.image.load('assets/strawberry/score/score{}.png'.format(int(self.index))).convert_alpha()
        else:
            self.kill()

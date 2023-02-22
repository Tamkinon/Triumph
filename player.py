import pygame
from pygame import mixer
import assets

pygame.init()
screen = pygame.display.set_mode((1280, 704))

img_red_run_0_or_idle = pygame.image.load('assets/player/run/idle_right.png').convert_alpha()
img_red_run_1 = pygame.image.load('assets/player/run/run_right_1.png').convert_alpha()
img_red_run_2_or_jump = pygame.image.load('assets/player/run/jump_right.png').convert_alpha()
img_red_run_3 = pygame.image.load('assets/player/run/run_right_2.png').convert_alpha()
img_red_wall = pygame.image.load('assets/player/wall_right.png').convert_alpha()
img_blue_jump = pygame.image.load('assets/player/blue_jump_right.png').convert_alpha()
img_blue_wall = pygame.image.load('assets/player/blue_wall_right.png').convert_alpha()
img_jump = pygame.image.load('assets/player/jump.png').convert_alpha()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.particles = pygame.sprite.Group()
        self.image = img_red_run_0_or_idle
        self.red_animation = [img_red_run_0_or_idle, img_red_run_1, img_red_run_2_or_jump, img_red_run_3]
        self.animation_index = 0
        self.animate_time = 0
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.rect.Rect(self.rect.left, self.rect.top + 24, 48, 24)
        self.facing = 'right'
        self.on_wall = 'right'
        self.near_wall = False
        self.dashing = False
        self.wall_jumping = False
        self.can_dash = True
        self.dash_index = 0
        self.dash_inc = 1
        self.wall_jump_index = 0
        self.wall_jump_time = 13
        self.wall_slide_index = 0
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.gravity = 0.9
        self.terminal_velocity = 10
        self.key_x = False
        self.key_c = False
        self.can_jump = True
        self.alive = True
        self.on_cloud = False
        self.on_cloud_vel = 0

    def animate(self):
        animation_cooldown = 8

        if not self.can_jump and not self.can_dash and self.terminal_velocity == 3:
            self.image = pygame.transform.flip(img_blue_wall, self.on_wall == 'left', False)
        elif not self.can_jump and self.can_dash and self.terminal_velocity == 3:
            self.image = pygame.transform.flip(img_red_wall, self.on_wall == 'left', False)
        elif not self.can_jump and not self.can_dash:
            self.image = pygame.transform.flip(img_blue_jump, self.facing == 'left', False)
        elif (not self.can_jump or 0.9 != self.direction.y != 0) and self.can_dash:
            self.image = pygame.transform.flip(img_jump, self.facing == 'left', False)
        else:
            if self.direction.x != 0:
                self.image = pygame.transform.flip(self.red_animation[self.animation_index], self.direction.x < 0,
                                                   False)
                self.animate_time += 1
                self.animation_index = self.animate_time // animation_cooldown
                if self.animation_index == 4:
                    self.animation_index = 0
                    self.animate_time = 0
            else:
                self.image = pygame.transform.flip(img_red_run_0_or_idle, self.facing == 'left', False)
                self.animation_index = 0
                self.animate_time = 0

    def inc_dash(self):
        self.dash_index += self.dash_inc
        if self.dash_index >= 10:
            if self.direction.y != 0:
                self.direction.y = self.direction.y / abs(self.direction.y) * 10
            self.dashing = False
            self.dash_index = 0
            if self.direction.x > 0:
                self.direction.x = 1
            elif self.direction.x < 0:
                self.direction.x = -1

    def inc_wall_jump(self):
        self.wall_jump_index += 1
        if self.wall_jump_index >= self.wall_jump_time:
            self.wall_jumping = False
            self.direction.y = -5
            self.wall_jump_index = 0

    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.dashing and not self.wall_jumping:
            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing = "left"
            else:
                self.direction.x = 0
            if self.key_c and (self.terminal_velocity == 3 or self.near_wall) and 0.9 != self.direction.y != 0:
                walljump_sound = mixer.Sound('assets/sfx/sfx2.wav')
                walljump_sound.set_volume(0.15)
                walljump_sound.play()
                self.key_c = False
                self.wall_jumping = True
                self.wall_jump_index = 0
                if self.on_wall == 'right':
                    self.wall_jump_left()
                    self.on_wall = 'left'
                    self.facing = 'left'
                else:
                    self.wall_jump_right()
                    self.on_wall = 'right'
                    self.facing = 'right'
            if self.key_c and self.can_jump and (self.direction.y == 0 or self.direction.y == 0.9):
                self.particles.add(assets.Particle(self.rect.midleft))
                jump_sound = mixer.Sound('assets/sfx/sfx1.wav')
                jump_sound.set_volume(0.15)
                jump_sound.play()
                self.key_c = False
                self.jump(-14)
                self.can_jump = False
            if self.key_x and self.can_dash:
                dash_sound = mixer.Sound('assets/sfx/sfx3.wav')
                dash_sound.set_volume(0.15)
                dash_sound.play()
                self.key_x = False
                up = keys[pygame.K_UP]
                down = keys[pygame.K_DOWN]
                right = keys[pygame.K_RIGHT]
                left = keys[pygame.K_LEFT]
                self.dash_index = 0
                self.dashing = True
                self.can_dash = False
                self.can_jump = False
                if up and not down and right and not left:
                    self.dash_up_right()
                elif up and not down and not right and left:
                    self.dash_up_left()
                elif not up and down and right and not left:
                    self.dash_down_right()
                elif not up and down and not right and left:
                    self.dash_down_left()
                elif up and not down and not right and not left:
                    self.dash_up()
                elif not up and down and not right and not left:
                    self.dash_down()
                elif not up and not down and right and not left:
                    self.dash_right()
                elif not up and not down and not right and left:
                    self.dash_left()
                else:
                    if self.facing == "right":
                        self.dash_right()
                    else:
                        self.dash_left()
            else:
                if self.key_x:
                    self.particles.add(assets.Particle(self.rect.topleft))
                    self.key_x = False

    def apply_gravity(self):
        if not self.dashing and not self.wall_jumping:
            self.direction.y += self.gravity
        if self.direction.y > self.terminal_velocity and not self.dashing:
            self.direction.y = self.terminal_velocity
        self.hitbox.y += self.direction.y

    def jump(self, speed):
        self.direction.y = speed

    def dash_up(self):
        self.jump(-12)

    def dash_down(self):
        self.jump(12)

    def dash_right(self):
        self.direction.x = 3
        self.direction.y = 0

    def dash_left(self):
        self.direction.x = -3
        self.direction.y = 0

    def dash_up_right(self):
        self.direction.x = 2
        self.direction.y = 0
        self.jump(-10)

    def dash_down_right(self):
        self.direction.x = 2
        self.direction.y = 0
        self.jump(10)

    def dash_up_left(self):
        self.direction.x = -2
        self.direction.y = 0
        self.jump(-10)

    def dash_down_left(self):
        self.direction.x = -2
        self.direction.y = 0
        self.jump(10)

    def wall_jump_right(self):
        self.wall_jump_index = 0
        self.direction.x = 1.5
        self.direction.y = 0
        self.jump(-7)

    def wall_jump_left(self):
        self.wall_jump_index = 0
        self.direction.x = -1.25
        self.direction.y = 0
        self.jump(-7)

    def update(self):
        if self.alive:
            self.rect.bottomleft = self.hitbox.bottomleft
            self.get_input()
        if self.on_cloud:
            self.hitbox.x += self.direction.x * self.speed + self.on_cloud_vel
        else:
            self.hitbox.x += self.direction.x * self.speed

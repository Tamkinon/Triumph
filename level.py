import pygame
from pygame import mixer
from settings import tile_size
from player import Player
import assets
import random


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.springs = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.orbs = pygame.sprite.Group()
        self.vanish_boxes = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.strawberries = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.flag = pygame.sprite.GroupSingle()
        self.clouds = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.game_state = 0
        self.player_spawn = ()
        self.completed = False
        self.death_time = 30
        self.strawberry_collected = False
        self.setup_level(level_data)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                if cell == 'X':
                    if col_index * tile_size == 0 and row_index * tile_size == 0:
                        top = True
                        left = True
                        right = row[1] == 'X'
                        bottom = layout[1][0] == 'X'
                    elif col_index * tile_size == 768 - tile_size and row_index * tile_size == 0:
                        top = True
                        right = True
                        left = row[-2] == 'X'
                        bottom = layout[1][-1] == 'X'
                    elif col_index * tile_size == 0 and row_index * tile_size == 768 - tile_size:
                        bottom = True
                        left = True
                        top = layout[-2][0] == 'X'
                        right = row[1] == 'X'
                    elif col_index * tile_size == 768 - tile_size and row_index * tile_size == 768 - tile_size:
                        bottom = True
                        right = True
                        top = layout[-2][-1] == 'X'
                        left = row[-2] == 'X'
                    elif row_index * tile_size == 0:
                        top = True
                        bottom = layout[1][col_index] == 'X'
                        right = row[col_index + 1] == 'X'
                        left = row[col_index - 1] == 'X'
                    elif row_index * tile_size == 768 - tile_size:
                        bottom = True
                        top = layout[-2][col_index] == 'X'
                        right = row[col_index + 1] == 'X'
                        left = row[col_index - 1] == 'X'
                    elif col_index * tile_size == 0:
                        left = True
                        right = row[1] == 'X'
                        top = layout[row_index - 1][0] == 'X'
                        bottom = layout[row_index + 1][0] == 'X'
                    elif col_index * tile_size == 768 - tile_size:
                        right = True
                        left = row[-2] == 'X'
                        top = layout[row_index - 1][-1] == 'X'
                        bottom = layout[row_index + 1][-1] == 'X'
                    else:
                        top = layout[row_index - 1][col_index] == 'X'
                        bottom = layout[row_index + 1][col_index] == 'X'
                        right = row[col_index + 1] == 'X'
                        left = row[col_index - 1] == 'X'
                    if not top and not bottom and not right and not left:
                        image = 'assets/tile/tile_single.png'
                    elif not top and bottom and right and left:
                        image = 'assets/tile/tile_top.png'
                    elif top and not bottom and right and left:
                        image = 'assets/tile/tile_bottom.png'
                    elif top and bottom and not right and left:
                        image = 'assets/tile/tile_right.png'
                    elif top and bottom and right and not left:
                        image = 'assets/tile/tile_left.png'
                    elif not top and bottom and not right and left:
                        image = 'assets/tile/tile_top_right.png'
                    elif top and not bottom and not right and left:
                        image = 'assets/tile/tile_bottom_right.png'
                    elif top and not bottom and right and not left:
                        image = 'assets/tile/tile_bottom_left.png'
                    elif not top and bottom and right and not left:
                        image = 'assets/tile/tile_top_left.png'
                    elif not top and not bottom and right and left:
                        image = 'assets/TIle/tile_top_bottom.png'
                    elif top and bottom and not right and not left:
                        image = 'assets/tile/tile_right_left.png'
                    elif not top and bottom and not right and not left:
                        image = 'assets/tile/tile_not_bottom.png'
                    elif not top and not bottom and not right and left:
                        image = 'assets/tile/tile_not_left.png'
                    elif top and not bottom and not right and not left:
                        image = 'assets/tile/tile_not_top.png'
                    elif not top and not bottom and right and not left:
                        image = 'assets/tile/tile_not_right.png'
                    else:
                        random.seed(str(col_index) + str(row_index))
                        if random.randint(1, 6) != 1:
                            image = "assets/tile/tile_fill.png"
                        else:
                            image = "assets/tile/tile_fill_1.png"
                    tile = assets.Tile((col_index * tile_size + 576, row_index * tile_size + 156), image)
                    self.tiles.add(tile)
                if cell == 'H':
                    vanish_box = assets.VanishBox((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.vanish_boxes.add(vanish_box)
                if cell == 'P':
                    player_sprite = Player((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.player_spawn = player_sprite.rect.center
                    self.player.add(player_sprite)
                if cell == 'S':
                    spring = assets.Spring((col_index * tile_size + 576, row_index * tile_size + 156 + 18))
                    self.springs.add(spring)
                if cell == '^':
                    spike = assets.SpikeUp((col_index * tile_size + 576, row_index * tile_size + 18 + 156))
                    self.spikes.add(spike)
                if cell == 'V':
                    spike = assets.SpikeDown((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.spikes.add(spike)
                if cell == '<':
                    spike = assets.SpikeLeft((col_index * tile_size + 18 + 576, row_index * tile_size + 156))
                    self.spikes.add(spike)
                if cell == '>':
                    spike = assets.SpikeRight((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.spikes.add(spike)
                if cell == 'O':
                    orb = assets.DashOrb((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.orbs.add(orb)
                if cell == '$':
                    strawberry = assets.Strawberry((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.strawberries.add(strawberry)
                if cell == 'F':
                    flag = assets.Flag((col_index * tile_size + 576, row_index * tile_size + 156))
                    self.flag.add(flag)
                if cell == '{':
                    cloud = assets.Cloud((col_index * tile_size + 576, row_index * tile_size + 156), -1)
                    self.clouds.add(cloud)
                if cell == '}':
                    cloud = assets.Cloud((col_index * tile_size + 576, row_index * tile_size + 156), 1)
                    self.clouds.add(cloud)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        if player.on_cloud:
            player.hitbox.x += player.direction.x * player.speed + player.on_cloud_vel
        else:
            player.hitbox.x += player.direction.x * player.speed
        tile_found = False
        near_tile = False
        keys = pygame.key.get_pressed()
        if player.hitbox.left <= 576:
            player.hitbox.left = 576
            player.direction.x = 0
        elif player.hitbox.right >= 1344:
            player.hitbox.right = 1344
            player.direction.x = 0
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                    tile_found = True
                if player.wall_jumping:
                    player.wall_jump_index = player.wall_jump_time + 1
                if player.on_cloud:
                    if player.direction.x + player.on_cloud_vel < 0:
                        if player.direction.y not in [0, 0.6, -7]:
                            player.wall_slide_index += 1
                            if player.wall_slide_index == 1:
                                self.particles.add(assets.Particle((player.rect.left - player.rect.width / 2, player.rect.top)))
                            elif player.wall_slide_index == 20:
                                player.wall_slide_index = 0
                        player.on_wall = 'left'
                        player.hitbox.left = sprite.rect.right
                    elif player.direction.x + player.on_cloud_vel > 0:
                        if player.direction.y not in [0, 0.6, -7]:
                            player.wall_slide_index += 1
                            if player.wall_slide_index == 1:
                                self.particles.add(assets.Particle(player.rect.midtop))
                            elif player.wall_slide_index == 30:
                                player.wall_slide_index = 0
                        player.on_wall = 'right'
                        player.hitbox.right = sprite.rect.left
                else:
                    if player.direction.x < 0:
                        if player.direction.y not in [0, 0.6, -7]:
                            player.wall_slide_index += 1
                            if player.wall_slide_index == 1:
                                self.particles.add(assets.Particle((player.rect.left - player.rect.width / 2, player.rect.top)))
                            elif player.wall_slide_index == 20:
                                player.wall_slide_index = 0
                        player.on_wall = 'left'
                        player.hitbox.left = sprite.rect.right
                    elif player.direction.x > 0:
                        if player.direction.y not in [0, 0.6, -7]:
                            player.wall_slide_index += 1
                            if player.wall_slide_index == 1:
                                self.particles.add(assets.Particle(player.rect.midtop))
                            elif player.wall_slide_index == 30:
                                player.wall_slide_index = 0
                        player.on_wall = 'right'
                        player.hitbox.right = sprite.rect.left
                player.direction.x = 0
            else:
                if sprite.rect.top < player.hitbox.centery < sprite.rect.bottom and player.hitbox.right == sprite.rect.left:
                    player.on_wall = 'right'
                    near_tile = True
                elif sprite.rect.top < player.hitbox.centery < sprite.rect.bottom and player.rect.left == sprite.rect.right:
                    player.on_wall = 'left'
                    near_tile = True
        for sprite in self.springs.sprites():
            if sprite.rect.colliderect(player.hitbox) and sprite.state == 1:
                self.particles.add(assets.Particle(player.rect.topleft))
                spring_sound = mixer.Sound('assets/sfx/sfx8.wav')
                spring_sound.set_volume(0.15)
                spring_sound.play()
                player.dash_index = 10
                player.wall_jump_index = player.wall_jump_time + 1
                player.jump(-20)
                player.can_jump = False
                player.can_dash = True
                sprite.state = 0
        for sprite in self.spikes.sprites():
            if sprite.rect.colliderect(pygame.Rect(player.rect.left + 3, player.rect.top, 42, 24)):
                self.game_state = 0
        for sprite in self.orbs.sprites():
            if sprite.rect.colliderect(player.rect) and (player.dashing or not player.can_dash) and sprite.state:
                self.particles.add(assets.OrbParticle(sprite.rect.topleft))
                orb_sound = mixer.Sound('assets/sfx/sfx6.wav')
                orb_sound.set_volume(0.15)
                orb_sound.play()
                player.can_dash = True
                sprite.state = 0
        vanish_found = False
        near_vanish = False
        for sprite in self.vanish_boxes.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if sprite.state != 2:
                    if sprite.state == 0:
                        vanish_box_sound = mixer.Sound('assets/sfx/sfx15.wav')
                        vanish_box_sound.set_volume(0.15)
                        vanish_box_sound.play()
                    vanish_found = True
                    player.dash_index = 10
                    player.wall_jump_index = player.wall_jump_time + 1
                    if player.direction.x + player.on_cloud_vel < 0:
                        player.hitbox.left = sprite.rect.right
                    elif player.direction.x + player.on_cloud_vel > 0:
                        player.hitbox.right = sprite.rect.left
                    player.direction.x = 0
                    sprite.state = 1
            else:
                if sprite.state != 2:
                    if (sprite.rect.top < player.hitbox.bottom < sprite.rect.bottom or sprite.rect.top < player.hitbox.top < sprite.rect.bottom) and player.hitbox.right == sprite.rect.left:
                        if sprite.state == 0:
                            vanish_box_sound = mixer.Sound('assets/sfx/sfx15.wav')
                            vanish_box_sound.set_volume(0.15)
                            vanish_box_sound.play()
                        player.on_wall = 'right'
                        sprite.state = 1
                        near_vanish = True
                    elif (sprite.rect.top < player.hitbox.bottom < sprite.rect.bottom or sprite.rect.top < player.hitbox.top < sprite.rect.bottom) and player.hitbox.left == sprite.rect.right:
                        if sprite.state == 0:
                            vanish_box_sound = mixer.Sound('assets/sfx/sfx15.wav')
                            vanish_box_sound.set_volume(0.15)
                            vanish_box_sound.play()
                        player.on_wall = 'left'
                        sprite.state = 1
                        near_vanish = True
        for sprite in self.strawberries:
            if sprite.rect.colliderect(player.rect):
                strawberry_sound = mixer.Sound('assets/sfx/sfx13.wav')
                strawberry_sound.set_volume(0.15)
                strawberry_sound.play()
                self.strawberry_collected = True
                self.scores.add(assets.Score(sprite.rect.midtop))
                sprite.kill()
        if self.flag and self.flag.sprite.rect.colliderect(player.rect) and not self.flag.sprite.touched:
            self.flag.sprite.touched = True
            flag_sound = mixer.Sound('assets/sfx/sfx55.wav')
            flag_sound.set_volume(0.6)
            flag_sound.play()
        if tile_found or vanish_found:
            player.terminal_velocity = 3
        else:
            player.terminal_velocity = 10
            player.wall_slide_index = 0
        player.near_wall = near_tile or near_vanish

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                player.dash_index = 10
                player.wall_jump_index = player.wall_jump_time + 1
                if player.direction.y > 0:
                    if player.direction.y not in [0, 0.6, 1.2]:
                        if not player.can_dash:
                            can_dash_sound = mixer.Sound('assets/sfx/sfx54.wav')
                            can_dash_sound.set_volume(0.15)
                            can_dash_sound.play()
                        self.particles.add(assets.Particle(player.rect.midleft))
                    player.hitbox.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.near_wall = False
                    player.can_jump = True
                    player.can_dash = True
                elif player.direction.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.direction.y = 0
        for sprite in self.springs.sprites():
            if sprite.rect.colliderect(player.hitbox) and sprite.state == 1:
                self.particles.add(assets.Particle(player.rect.topleft))
                spring_sound = mixer.Sound('assets/sfx/sfx8.wav')
                spring_sound.set_volume(0.15)
                spring_sound.play()
                player.dash_index = 10
                player.wall_jump_index = player.wall_jump_time + 1
                player.jump(-20)
                player.can_jump = False
                player.can_dash = True
                sprite.state = 0
        for sprite in self.spikes.sprites():
            if sprite.rect.colliderect(pygame.Rect(player.rect.left + 3, player.rect.top, 42, 24)):
                self.game_state = 0
        for sprite in self.orbs.sprites():
            if sprite.rect.colliderect(player.hitbox) and (player.dashing or not player.can_dash) and sprite.state:
                self.particles.add(assets.OrbParticle(sprite.rect.topleft))
                orb_sound = mixer.Sound('assets/sfx/sfx6.wav')
                orb_sound.set_volume(0.15)
                orb_sound.play()
                player.can_dash = True
                sprite.state = 0
        for sprite in self.vanish_boxes.sprites():
            if sprite.rect.colliderect(player.hitbox) and sprite.state != 2:
                player.wall_jump_index = player.wall_jump_time + 1
                player.dash_index = 10
                if player.direction.y > 0:
                    if sprite.state == 0:
                        vanish_box_sound = mixer.Sound('assets/sfx/sfx15.wav')
                        vanish_box_sound.set_volume(0.15)
                        vanish_box_sound.play()
                    player.hitbox.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.can_jump = True
                    player.can_dash = True
                    player.dash_index = 0
                    sprite.state = 1
                elif player.direction.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.direction.y = 0
        for sprite in self.strawberries:
            if sprite.rect.colliderect(player.rect):
                strawberry_sound = mixer.Sound('assets/sfx/sfx13.wav')
                strawberry_sound.set_volume(0.15)
                strawberry_sound.play()
                self.strawberry_collected = True
                self.scores.add(assets.Score(sprite.rect.midtop))
                sprite.kill()
        cloud_found = False
        for sprite in self.clouds.sprites():
            if sprite.rect.colliderect(player.hitbox) and sprite.state == 1 and player.direction.y > 0:
                cloud_found = True
                player.dash_index = 10
                player.wall_jump_index = player.wall_jump_time + 1
                if player.direction.y not in [0, 0.6, 1.2]:
                    if not player.can_dash:
                        can_dash_sound = mixer.Sound('assets/sfx/sfx54.wav')
                        can_dash_sound.set_volume(0.15)
                        can_dash_sound.play()
                    self.particles.add(assets.Particle(player.rect.midleft))
                player.hitbox.bottom = sprite.rect.top
                player.direction.y = 0
                player.near_wall = False
                player.can_jump = True
                player.can_dash = True
                player.on_cloud_vel = sprite.vel
            if sprite.rect.top > player.hitbox.centery:
                sprite.state = 1
            else:
                sprite.state = 0
        player.on_cloud = cloud_found
        if self.flag and self.flag.sprite.rect.colliderect(player.rect) and not self.flag.sprite.touched:
            self.flag.sprite.touched = True
            flag_sound = mixer.Sound('assets/sfx/sfx55.wav')
            flag_sound.set_volume(0.6)
            flag_sound.play()

    def run(self):
        self.player.sprite.animate()
        if self.player.sprite.dashing and self.game_state == 1:
            self.player.sprite.inc_dash()
        if self.player.sprite.dash_index % 2 == 0 and 0 != self.player.sprite.dash_index != 10 and self.game_state == 1:
            self.particles.add(assets.Particle(self.player.sprite.rect.topleft))
        self.particles.add(self.player.sprite.particles)
        if self.player.sprite.wall_jumping and self.game_state == 1:
            self.player.sprite.inc_wall_jump()
        for sprite in self.orbs.sprites():
            sprite.update()
        for sprite in self.vanish_boxes.sprites():
            sprite.update()
        for sprite in self.particles.sprites():
            sprite.update()
        for sprite in self.springs.sprites():
            sprite.update()
        for sprite in self.scores.sprites():
            sprite.update()
        for sprite in self.clouds.sprites():
            sprite.update()
        if self.flag:
            self.flag.update()
        if self.player.sprite.rect.top > 924:
            self.game_state = 0
        elif self.player.sprite.rect.centery < 156 and not self.flag:
            self.completed = True
        if self.game_state == 0:
            self.player.sprite.alive = False
            self.death_time += 1
            if self.death_time == 1:
                self.particles.add(assets.DeathParticle(self.player.sprite.rect.center))
            self.player.sprite.image.set_alpha(0)
        else:
            self.player.sprite.alive = True
        self.player.sprite.update()
        self.all_sprites.add(self.clouds)
        self.all_sprites.add(self.orbs)
        self.all_sprites.add(self.tiles)
        self.all_sprites.add(self.vanish_boxes)
        self.all_sprites.add(self.springs)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.spikes)
        self.all_sprites.add(self.particles)
        self.all_sprites.add(self.strawberries)
        self.all_sprites.add(self.scores)
        self.all_sprites.add(self.flag)

        if self.game_state == 1:
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
        self.player.draw(self.display_surface)

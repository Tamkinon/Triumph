import pygame
from pygame import mixer
from settings import *
from levels import levels
from sys import exit
from level import Level
from assets.bg_rectangle.bg_Rectangle import BgRectangle
from assets.title_animation.title_animation import TitleAnimation
from assets.death_particle.death_particle import SpawnParticle

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
level_index = 0
level = Level(levels[level_index], screen)
title_bg = pygame.image.load('assets/titlebg.png').convert_alpha()
title_bg = pygame.transform.scale(title_bg, (768, 768))
console_bg = pygame.image.load('assets/consolebg.png').convert_alpha()
console_bg = pygame.transform.scale(console_bg, (screen_width, screen_height))
mixer.music.load('assets/sfx/menu_mus.wav')
mixer.music.set_volume(0.15)
mixer.music.play(-1)
game_state = GameStates.TITLE_SCREEN


def main():
    global level, level_index, game_state, title_bg
    strawberry = False
    score = 0
    pygame.display.set_caption("Celeste")
    rectangles = pygame.sprite.Group()
    time = 0
    animation_time = 0
    while True:
        time += 1
        if time % 15 == 0:
            rectangles.add(BgRectangle())
            rectangles.add(BgRectangle())
        for rectangle in rectangles.sprites():
            rectangle.update()
        if game_state == GameStates.GAMEPLAY:
            if level.game_state == 0:
                if level.death_time == 1:
                    death_sound = mixer.Sound('assets/sfx/sfx0.wav')
                    death_sound.set_volume(0.15)
                    death_sound.play()
                if level.death_time == 45:
                    level.particles.add(SpawnParticle(level.player_spawn))
                if level.death_time == 60:
                    if level.strawberry_collected:
                        score -= 1
                    level = Level(levels[level_index], screen)
                    level.game_state = 1
                    level.death_time = 0
                    strawberry = False
            else:
                if level.strawberry_collected and not strawberry:
                    score += 1
                    strawberry = True
            if level.completed:
                level_index += 1
                level = Level(levels[level_index], screen)
                strawberry = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        print(score)
                        exit()
                    if event.key == pygame.K_r:
                        game_state = GameStates.TITLE_SCREEN
                    level.player.sprite.key_x = event.key == pygame.K_x
                    level.player.sprite.key_c = event.key == pygame.K_c
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_c:
                        level.player.sprite.key_c = False
                    if event.key == pygame.K_x:
                        level.player.sprite.key_x = False
            screen.fill('black')
            rectangles.draw(screen)
            level.run()
            level.all_sprites.draw(screen)
        elif game_state == GameStates.TITLE_SCREEN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        mixer.music.stop()
                        game_state = GameStates.ANIMATION
                        startup_sound = mixer.Sound('assets/sfx/sfx38.wav')
                        startup_sound.set_volume(0.15)
                        startup_sound.play()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            screen.fill('black')
            screen.blit(title_bg, (576, 156))
        else:
            screen.fill('black')
            animation_time += 1
            if animation_time < 121:
                if animation_time % 10 == 0:
                    title_bg = TitleAnimation.ANIMATION[animation_time // 10 - 1]
                    title_bg = pygame.transform.scale(title_bg, (768, 768))
            else:
                mixer.music.load('assets/sfx/game_mus.wav')
                mixer.music.play(-1)
                game_state = GameStates.GAMEPLAY

            screen.blit(title_bg, (576, 156))
        screen.blit(console_bg, (0, 0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()


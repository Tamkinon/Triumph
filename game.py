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
score_box = pygame.image.load("assets/score_box.png").convert_alpha()
score_box = pygame.transform.scale(score_box, (384, 198))
mixer.music.load('assets/sfx/menu_mus.wav')
mixer.music.set_volume(0.15)
mixer.music.play(-1)
game_state = GameStates.TITLE_SCREEN


def main():
    global level, level_index, game_state, title_bg
    strawberry = False
    deaths = 0
    score = 0
    pygame.display.set_caption("Celeste")
    rectangles = pygame.sprite.Group()
    time = 0
    speed_run_time = 0
    display_time_time = -1
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
                    display_time_time = 0
                    deaths += 1
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
                if level.flag:
                    mixer.music.stop()
                    mixer.music.load('assets/sfx/end_mus.wav')
                    mixer.music.play(-1)
                else:
                    display_time_time = 0
                strawberry = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    if event.key == pygame.K_r:
                        level_index = 0
                        mixer.music.load('assets/sfx/menu_mus.wav')
                        mixer.music.play(-1)
                        game_state = GameStates.TITLE_SCREEN
                        title_bg = TitleAnimation.ANIMATION[0]
                        title_bg = pygame.transform.scale(title_bg, (768, 768))
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
            if display_time_time != -1 and display_time_time < 90:
                display_time_time += 1
                screen.blit(pygame.Surface((176, 38)), (576 + 24, 156 + 24))
                score_surface = time_font.render(frames_to_clock(speed_run_time), 1, 'white')
                screen.blit(score_surface, (576 + 30, 156 + 30))
            else:
                display_time_time = -1
            if level.flag:
                if level.flag.sprite.touched:
                    display_score(score, speed_run_time, deaths)
            else:
                speed_run_time += 1
        elif game_state == GameStates.TITLE_SCREEN:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        mixer.music.stop()
                        game_state = GameStates.ANIMATION
                        animation_time = 0
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
                speed_run_time = 0
                deaths = 0
                score = 0
                mixer.music.load('assets/sfx/game_mus.wav')
                mixer.music.play(-1)
                game_state = GameStates.GAMEPLAY
                level = Level(levels[level_index], screen)
                strawberry = False
            screen.blit(title_bg, (576, 156))
        screen.blit(console_bg, (0, 0))
        pygame.display.update()
        clock.tick(60)


def frames_to_clock(frames):
    sec = frames // 60
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, minutes, sec)


def display_score(score, time, deaths):
    time = frames_to_clock(time)
    screen.blit(score_box, (576 + (768 - 384) / 2, 160))
    score_surface = score_font.render("   X   " + str(score), 1, 'white')
    screen.blit(score_surface, (576 + (768 - 384) / 2 + 90, 160 + 25))
    time_surface = score_font.render("   " + time, 1, 'white')
    screen.blit(time_surface, (576 + (768 - 384) / 2 + 90, 160 + 80))
    deaths_surface = score_font.render("   X   " + str(deaths), 1, 'white')
    screen.blit(deaths_surface, (576 + (768 - 384) / 2 + 90, 160 + 135))


if __name__ == '__main__':
    main()


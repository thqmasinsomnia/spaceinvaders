import pygame
import sys
from pygame.sprite import Group
from pygame import mixer

from settings import Settings
from ship import Ship

import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from highscore import Highscore


def run_game():
    # init game and create screen object
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("SPACE INVADERS")
    screen.fill([255, 255, 255])
    test = pygame.image.load("images/spaceinvaders.png")
    screen.blit(test, [0, 0])
    pygame.display.flip()

    pygame.mixer.music.load('sounds/gamemusic.ogg')
    pygame.mixer.music.play(-1)
    highscore = Highscore(screen)

    print(highscore.get_lowest_score())

    endintro = False
    openhighscore = False
    while endintro == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    endintro = True
                elif event.key == pygame.K_s:
                    endintro = True
                    openhighscore = True

    if openhighscore:
        highscore.show_scores()

        pygame.display.flip()

    while openhighscore == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    openhighscore = False

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    alienbullets = Group()
    aliens = Group()
    aliensb = Group()
    aliensc = Group()
    ufos = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, aliens)
    gf.create_b_fleet(ai_settings, screen, ship, aliensb)
    gf.create_c_fleet(ai_settings, screen, ship, aliensc)
    # Make an alien.

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    gf.create_ufo(ai_settings, screen, ufos)

    while True:



        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, aliensb, aliensc, bullets,
                        alienbullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)
            gf.update_alien_bullets(ai_settings, screen, stats, sb, ship, alienbullets)
            gf.maybe_ufo(ai_settings, screen, ufos)
            gf.update_ufo(ufos)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)
            gf.maybe_shoot(ai_settings, screen, ship, alienbullets, aliens)
            gf.check_alien_bullet_ship_collisions(ai_settings, screen, stats, sb, ship, aliens, aliensb, aliensc,
                                                  bullets, alienbullets)
            gf.check_bullet_ufo_collisions(ai_settings, screen, stats, sb, bullets, ufos)
            if ufos.__len__() > 0:
                for ufo in ufos.copy():
                    ufo.move()
                    if ufo.rect.x > 600:
                        ufos.remove(ufo)
                        print("its gone")

        bullets.update()
        alienbullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        for bullet in alienbullets.copy():
            if bullet.rect.y > 800:
                alienbullets.remove(bullet)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets, play_button,
                         alienbullets, ufos)


run_game()

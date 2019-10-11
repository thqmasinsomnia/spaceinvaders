import pygame
import sys
from pygame.sprite import Group

from settings import Settings
from ship import Ship

import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from high_score import High_score
from bunker import Bunker


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
    high_score = High_score(screen)

    print(high_score.get_lowest_score())

    end_intro = False
    open_high_score = False
    while not end_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    end_intro = True
                elif event.key == pygame.K_s:
                    end_intro = True
                    open_high_score = True

    if open_high_score:
        high_score.show_scores()

        pygame.display.flip()

    while open_high_score:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    open_high_score = False

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

    bunk = Group()

    bunk1 = Bunker(screen)
    bunk1.create_bunker(50, 600)
    bunk.add(bunk1)
    bunk2 = Bunker(screen)
    bunk2.create_bunker(250, 600)
    bunk.add(bunk2)
    bunk3 = Bunker(screen)
    bunk3.create_bunker(450, 600)
    bunk.add(bunk3)

    TC = pygame.mixer.Sound("sounds/TC.ogg")

    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, aliensb, aliensc, bullets,
                        alienbullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets, alienbullets)
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
                    pygame.mixer.Sound.play(TC)
                    if ufo.rect.x > 600:
                        ufos.remove(ufo)
                        pygame.mixer.Sound.stop(TC)
                        print("its gone")

        bullets.update()
        alienbullets.update()

        gf.check_bunker_collisions(bullets, alienbullets, bunk)

        # Get rid of bullets that have disappeared.
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        for bullet in alienbullets.copy():
            if bullet.rect.y > 800:
                alienbullets.remove(bullet)


        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets, play_button,
                         alienbullets, ufos, bunk)


run_game()

import sys

import pygame
from pygame import mixer
import random

from bullet import Bullet
from alien import Alien
from time import sleep
from alienb import AlienB
from ufo import UFO
fpsClock = pygame.time.Clock()

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * (row_number + 2)
    aliens.add(alien)


def create_alienB(ai_settings, screen, aliensb, alienb_number, row_number):
    alienb = AlienB(ai_settings, screen)
    alien_widthb = alienb.rect.width
    alienb.x = alien_widthb + 2 * alien_widthb * alienb_number
    alienb.rect.x = alienb.x
    alienb.rect.y = alienb.rect.height + 2 * alienb.rect.height * row_number
    aliensb.add(alienb)


def create_b_fleet(ai_settings, screen, ship, aliensB):
    row_number = 2
    alien = AlienB(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    for row_number in range(row_number):
        for alien_number in range(number_aliens_x):
            create_alienB(ai_settings, screen, aliensB, alien_number, row_number)


def create_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    row_number = 2

    for row_number in range(row_number):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets):
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisionsb = pygame.sprite.groupcollide(bullets, aliensb, True, True)
    if collisions:
        alien_death = pygame.mixer.Sound("sounds/aliendeath.ogg")
        pygame.mixer.Sound.play(alien_death)
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    elif collisionsb:
        alien_death = pygame.mixer.Sound("sounds/aliendeath.ogg")
        pygame.mixer.Sound.play(alien_death)
        for aliensb in collisionsb.values():
            stats.score += ai_settings.alienb_points * len(aliensb)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens)
        create_b_fleet(ai_settings, screen, ship, aliensb)

    if len(aliensb) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens)
        create_b_fleet(ai_settings, screen, ship, aliensb)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets) < ai_settings.bullets_allowed:
        bullet_sound = pygame.mixer.Sound("sounds/fire.ogg")
        pygame.mixer.Sound.play(bullet_sound)
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, aliensb, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliensb, bullets, mouse_x,
                              mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, aliensb, bullets, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        stats.reset_stats()
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Empty the list of aliens and bullets.
        aliens.empty()
        aliensb.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, aliens)
        create_b_fleet(ai_settings, screen, ship, aliensb)
        ship.center_ship()


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens, aliensb):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens, aliensb)

    for alien in aliensb.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens, aliensb)
            break


def shipdeath(ship):

    shipimgs = ['images/shipexplosion1.png', 'images/shipexplosion2.png', 'images/shipexplosion3.png'
        , 'images/shipexplosion4.png', 'images/shipexplosion5.png', 'images/shipexplosion6.png'
        , 'images/shipexplosion7.png']

    for num in range(7):
        ship.image = pygame.image.load(shipimgs[num])
        ship.blitme()
        fpsClock.tick(1000)


def change_fleet_direction(ai_settings, aliens, aliensb):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in aliensb.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets):
    if stats.ships_left > 0:
        ship_death = pygame.mixer.Sound("sounds/shipdeath.ogg")
        pygame.mixer.Sound.play(ship_death)
        stats.ships_left -= 1
        shipdeath(ship)

        # update scoreboard
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        aliensb.empty()
        bullets.empty()


        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()


        # Pause.
        sleep(.5)
        ship.image = pygame.image.load("images/ship.png")

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets)
            break
    for alien in aliensb.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets):
    check_fleet_edges(ai_settings, aliens, aliensb)
    aliens.update()
    aliensb.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, aliensb, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    sb.show_score()
    aliens.draw(screen)
    aliensb.draw(screen)

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

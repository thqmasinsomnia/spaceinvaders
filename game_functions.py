import random
import sys
from time import sleep

import pygame

from alien import Alien
from alienb import AlienB
from alienbullet import AlienBullet
from alienc import AlienC
from bullet import Bullet
from bunker import Bunker
from high_score import High_score
from ufo import UFO
from bunker import Bunker;

fpsClock = pygame.time.Clock()


def create_alien(si_settings, screen, aliens, alien_number, row_number):
    alien = Alien(si_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * (row_number + 3)
    aliens.add(alien)


def create_alienB(si_settings, screen, aliensb, alienb_number, row_number):
    alienb = AlienB(si_settings, screen)
    alien_widthb = alienb.rect.width
    alienb.x = alien_widthb + 2 * alien_widthb * alienb_number
    alienb.rect.x = alienb.x
    alienb.rect.y = alienb.rect.height + 2 * alienb.rect.height * (row_number + 1)
    aliensb.add(alienb)


def create_alienC(si_settings, screen, aliensc, alien_number, row_number):
    alien = AlienC(si_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliensc.add(alien)


def create_ufo(si_settings, screen, ufos):
    ufo = UFO(si_settings, screen)
    ufo.rect.y = random.randint(50, 200)
    ufos.add(ufo)


def create_c_fleet(si_settings, screen, ship, aliensC):
    row_number = 1
    alien = AlienC(si_settings, screen)
    number_aliens_x = get_number_aliens_x(si_settings, alien.rect.width)
    for row_number in range(row_number):
        for alien_number in range(number_aliens_x):
            create_alienC(si_settings, screen, aliensC, alien_number, row_number)


def create_b_fleet(si_settings, screen, ship, aliensB):
    row_number = 2
    alien = AlienB(si_settings, screen)
    number_aliens_x = get_number_aliens_x(si_settings, alien.rect.width)
    for row_number in range(row_number):
        for alien_number in range(number_aliens_x):
            create_alienB(si_settings, screen, aliensB, alien_number, row_number)


def create_fleet(si_settings, screen, aliens):
    alien = Alien(si_settings, screen)
    number_aliens_x = get_number_aliens_x(si_settings, alien.rect.width)

    row_number = 2

    for row_number in range(row_number):
        for alien_number in range(number_aliens_x):
            create_alien(si_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(si_settings, alien_width):
    available_space_x = si_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def update_alien_bullets(si_settings, screen, stats, sb, ship, alien_bullets):
    alien_bullets.update()
    for bullet in alien_bullets.copy():
        if bullet.rect.y <= 0:
            alien_bullets.remove(bullet)


def update_bullets(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets):
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)


def check_bullet_alien_collisions(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    collisionsb = pygame.sprite.groupcollide(bullets, aliensb, True, True)
    collisionsc = pygame.sprite.groupcollide(bullets, aliensc, True, True)

    if collisions:
        alien_death = pygame.mixer.Sound("sounds/aliendeath.ogg")
        pygame.mixer.Sound.play(alien_death)
        for aliens in collisions.values():
            stats.score += si_settings.alien_points * len(aliens)
            sb.prep_score()
            sb.prep_score()
        check_high_score(stats, sb)
    elif collisionsb:
        alien_death = pygame.mixer.Sound("sounds/aliendeath.ogg")
        pygame.mixer.Sound.play(alien_death)
        for aliensb in collisionsb.values():
            stats.score += si_settings.alienb_points * len(aliensb)
            sb.prep_score()
        check_high_score(stats, sb)
    elif collisionsc:
        alien_death = pygame.mixer.Sound("sounds/aliendeath.ogg")
        pygame.mixer.Sound.play(alien_death)
        for aliensc in collisionsc.values():
            stats.score += si_settings.alienc_points * len(aliensc)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        si_settings.increase_speed()

        stats.level += 1
        sb.prep_level()
        create_fleet(si_settings, screen, aliens)
        create_b_fleet(si_settings, screen, ship, aliensb)
        create_c_fleet(si_settings, screen, ship, aliensc)

    if len(aliensb) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        si_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(si_settings, screen, aliens)
        create_b_fleet(si_settings, screen, ship, aliensb)
        create_c_fleet(si_settings, screen, ship, aliensc)

    if len(aliensc) == 0:
        # Destroy existing bullets and create new fleet.
        bullets.empty()
        si_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()
        create_fleet(si_settings, screen, aliens)
        create_b_fleet(si_settings, screen, ship, aliensb)
        create_c_fleet(si_settings, screen, ship, aliensc)


def check_alien_bullet_ship_collisions(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets,
                                       alien_bullets):
    collisions = pygame.sprite.spritecollideany(ship, alien_bullets)

    if collisions:
        for bullet in alien_bullets:
            alien_bullets.remove(bullet)
        alien_bullets.update()
        ship_hit(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)


def check_keydown_events(event, si_settings, screen, ship, bullets, alien_bullets, aliens):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(si_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_r:
        alien_bullet_shoot(si_settings, screen, ship, alien_bullets, aliens)


def fire_bullet(si_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    if len(bullets) < si_settings.bullets_allowed:
        bullet_sound = pygame.mixer.Sound("sounds/fire.ogg")
        pygame.mixer.Sound.play(bullet_sound)
        new_bullet = Bullet(si_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(si_settings, screen, stats, sb, play_button, ship, aliens, aliensb, aliensc, bullets, alienbullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, si_settings, screen, ship, bullets, alienbullets, aliens)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(si_settings, screen, stats, sb, play_button, ship, aliens, aliensb, aliensc, bullets,
                              mouse_x,
                              mouse_y)


def check_play_button(si_settings, screen, stats, sb, play_button, ship, aliens, aliensb, aliensc, bullets, mouse_x,
                      mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        stats.reset_stats()
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # Reset the game settings.
        si_settings.initialize_dynamic_settings()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Empty the list of aliens and bullets.
        aliens.empty()
        aliensb.empty()
        aliensc.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(si_settings, screen, aliens)
        create_b_fleet(si_settings, screen, ship, aliensb)
        ship.center_ship()


def get_number_rows(si_settings, ship_height, alien_height):
    available_space_y = (si_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(si_settings, aliens, aliensb, aliensc):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(si_settings, aliens, aliensb, aliensc)

    for alien in aliensb.sprites():
        if alien.check_edges():
            change_fleet_direction(si_settings, aliens, aliensb, aliensc)

    for alien in aliensc.sprites():
        if alien.check_edges():
            change_fleet_direction(si_settings, aliens, aliensb, aliensc)
            break


def shipdeath(ship):
    shipimgs = ['images/shipexplosion1.png', 'images/shipexplosion2.png', 'images/shipexplosion3.png'
        , 'images/shipexplosion4.png', 'images/shipexplosion5.png', 'images/shipexplosion6.png'
        , 'images/shipexplosion7.png']

    for num in range(7):
        ship.image = pygame.image.load(shipimgs[num])
        ship.update()
        ship.blitme()
        pygame.display.flip()
        pygame.time.wait(100)


def aliendeath(alien):
    alienimgs = ['images/explosion1a.png', 'images/explosion1b.png', 'images/explosion1c.png', 'images/explosion1d.png']

    for num in range(4):
        alien.image = pygame.image.load(alienimgs[num])
        alien.update()
        alien.blitme()
        pygame.display.flip()
        pygame.time.wait(50)


def change_fleet_direction(si_settings, aliens, aliensb, aliensc):
    for alien in aliens.sprites():
        alien.rect.y += si_settings.fleet_drop_speed
    for alien in aliensb.sprites():
        alien.rect.y += si_settings.fleet_drop_speed
    for alien in aliensc.sprites():
        alien.rect.y += si_settings.fleet_drop_speed
    si_settings.fleet_direction *= -1


def ship_hit(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets):
    if stats.ships_left > 0:
        stats.level = stats.level - 1
        ship_death = pygame.mixer.Sound("sounds/shipdeath.ogg")
        pygame.mixer.Sound.play(ship_death)
        stats.ships_left -= 1
        shipdeath(ship)

        # update scoreboard
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        aliensb.empty()
        aliensc.empty()
        bullets.empty()

        create_fleet(si_settings, screen, aliens)
        ship.center_ship()

        # Pause.
        sleep(.5)
        ship.image = pygame.image.load("images/ship.png")

    else:
        hs = High_score(screen)
        if stats.score > hs.get_lowest_score():
            sus = hs.get_intials()
            hs.add_score(sus, stats.score)
            print(stats.score)

            openhighscore = True
            hs.show_scores()
            pygame.display.flip()

            while openhighscore == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            openhighscore = False

        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)
            break
    for alien in aliensb.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)
            break
    for alien in aliensc.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)
            break


def update_aliens(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets):
    check_fleet_edges(si_settings, aliens, aliensb, aliensc)
    aliens.update()
    aliensb.update()
    aliensc.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets)


def check_bullet_ufo_collisions(si_settings, screen, stats, sb, bullets, ufos):
    collisions = pygame.sprite.groupcollide(bullets, ufos, True, True)
    font = font = pygame.font.Font('freesansbold.ttf', 10);
    whatever = random.randint(500, 2000)
    if collisions:

        for ufo in ufos:
            ufos.remove(ufo)

        stats.score += whatever
        sb.prep_score()
        sb.prep_high_score()
        sb.show_score()


def check_bunker_collisions(bullets, alien_bullets, bunkers):

    for bunker in bunkers:
        for block in bunker.bunker:
            bullet_collisions = shot = pygame.sprite.spritecollideany(block, bullets)
            if bullet_collisions:
                shot = pygame.sprite.spritecollideany(block, bullets)
                if shot:
                    for bullet in bullets:
                        bullets.remove(bullet)
                    block.remove(bunker.bunker)

    for bunker in bunkers:
        for block in bunker.bunker:
            bullet_collisions = shot = pygame.sprite.spritecollideany(block, alien_bullets)
            if bullet_collisions:
                shot = pygame.sprite.spritecollideany(block, alien_bullets)
                if shot:
                    for bullet in alien_bullets:
                        alien_bullets.remove(bullet)
                    block.remove(bunker.bunker)

def update_ufo(ufos):
    ufos.update()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(si_settings, screen, stats, sb, ship, aliens, aliensb, aliensc, bullets, play_button, alienbullets,
                  ufos, bunker):
    screen.fill(si_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for bullet in alienbullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    sb.show_score()
    aliens.draw(screen)
    aliensb.draw(screen)
    aliensc.draw(screen)
    ufos.draw(screen)
    for bunk in bunker:
        bunk.draw_bunker()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def alien_bullet_shoot(si_settings, screen, ship, alienbullets, aliens):
    alienbullets.update()
    # Get rid of bullets that have disappeared.
    for alien in aliens.sprites():
        i = alien.rect.y

    if len(alienbullets) < si_settings.bullets_allowed:
        bullet_sound = pygame.mixer.Sound("sounds/fire.ogg")
        pygame.mixer.Sound.play(bullet_sound)
        new_bullet = AlienBullet(si_settings, screen, ship, i)
        alienbullets.add(new_bullet)


def maybe_shoot(si_settings, screen, ship, alienbullets, aliens):
    if random.randint(1, 20) == 10:
        alien_bullet_shoot(si_settings, screen, ship, alienbullets, aliens)


def maybe_ufo(si_settings, screen, ufos):
    if ufos.__len__() == 0:
        if random.randint(1, 1000) == 10:
            create_ufo(si_settings, screen, ufos)

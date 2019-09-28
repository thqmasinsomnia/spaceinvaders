import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/ufoa.png')
        self.rect = self.image.get_rect()
        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the UFOS's exact position.
        self.x = float(self.rect.x)
        self.cnt = 1
        self.swap = False

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x = self.rect.x - 4

        if self.cnt < 50:
            self.cnt = self.cnt + 1
        elif self.swap and self.cnt == 50:
            self.cnt = 1
            self.image = pygame.image.load('images/ufoa.png')
            self.swap = False
        elif not self.swap and self.cnt == 50:
            self.cnt = 1
            self.image = pygame.image.load('images/ufob.png')
            self.swap = True

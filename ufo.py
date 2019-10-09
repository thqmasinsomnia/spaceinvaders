import pygame
from pygame.sprite import Sprite


class UFO(Sprite):
    def __init__(self, ai_settings, screen):
        super(UFO, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ufoa.png')
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = 100
        # Store the UFOS's exact position.
        self.x = -100
        self.y = 200
        self.cnt = 1
        self.swap = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def move(self):
        self.rect.x = self.rect.x + 1

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

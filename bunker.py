import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        pygame.sprite.Sprite.__init__(self)
        self.color

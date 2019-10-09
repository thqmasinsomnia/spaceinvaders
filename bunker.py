import pygame
from pygame.sprite import Sprite


class Bunker(Sprite):
    def __init__(self, row, column,  ai_settings, screen):
        Sprite.__init__(self)
        self.height = ai_settings.bunker_size
        self.width = ai_settings.bunker_size
        self.color = 0, 60, 0
        self.image = self.width, self.height
        self.image = self.color
        self.row = row
        self.column = column

    def update(self, keys, *args):
        self.screen.blit()

    def draw_bunker(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
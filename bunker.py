import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from block import Block


class Bunker(Sprite):
    def __init__(self, screen):
        Sprite.__init__(self)
        self.screen = screen
        self.bunker = Group()

    def create_bunker(self, x, y):
        x_hold = x
        cnt = 0
        for ehh in range(201):
            if ehh != 0:
                block = Block(x, y, self.screen)
                if cnt < 20:
                    x = x + 4
                else:
                    cnt = 0
                    x = x_hold

                if ehh % 20 == 0:
                    y = y + 4

                self.bunker.add(block)
                cnt = cnt + 1

    def draw_bunker(self):
        self.bunker.draw(self.screen)

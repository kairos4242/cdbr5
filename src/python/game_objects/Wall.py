import pygame
from Colours import Colours
from game_objects.GameObject import GameObject


class Wall(GameObject):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.make_solid()

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)
import pygame
from Colours import Colours
from game_objects.GameObject import GameObject
import sys
import os
sys.path.append(os.path.abspath('../'))
import Config


class Bullet(GameObject):

    def __init__(self, x, y, x_speed, y_speed, owner, attributes = list()):
        super().__init__(x, y)
        self.rect = self.create_rect(x, y, 24, 24)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.owner = owner
        self.attributes = attributes

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed)
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            if collide != self.owner:
                self.deal_damage(collide, 10, self.attributes)
                self.destroy(self)
import pygame
import pygame.geometry
from Circle import Circle
from Colours import Colours
from game_objects.GameObject import GameObject
import sys
import os
sys.path.append(os.path.abspath('../'))
import Config


class Bullet(GameObject):

    def __init__(self, x, y, x_speed, y_speed, owner: "GameObject", colour, attributes = list()):
        super().__init__(x, y)
        self.rect = self.create_rect(x, y, 24, 24)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.owner = owner
        self.attributes = attributes
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            if collide != self.owner:
                self.deal_damage(collide, 5, self.attributes)
                self.destroy(self)

class Bomb(GameObject):

    def __init__(self, x, y, owner, fuse, explosion_radius, attributes = list()):
        super().__init__(x, y)
        self.rect = self.create_rect(x, y, 24, 24)
        self.x_speed = 0
        self.y_speed = 0
        self.owner = owner
        self.fuse = fuse
        self.explosion_radius = explosion_radius
        self.attributes = attributes

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, self.outside_force_x, self.outside_force_y)
        self.fuse -= 1
        if self.fuse <= 0:
            collision_circle = pygame.geometry.Circle(self.rect.centerx, self.rect.centery, self.explosion_radius)
            collide = Circle.collideobjectsall(collision_circle, self.owner.solids_not_me())
            for collision in collide:
                self.owner.deal_damage(collision, 25, [])
                self.owner.map.screen_shake = 30
            self.destroy(self)
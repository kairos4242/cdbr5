import pygame
import pygame.geometry
from Circle import Circle
from Colours import Colours
from game_objects.GameObject import GameObject
import sys
import os
sys.path.append(os.path.abspath('../'))
import Config
import math


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

class Sword(GameObject):

    def __init__(self, x, y, owner, damage, x_dir, y_dir, attributes = list()):
        super().__init__(x, y)
        self.rect = self.create_rect(x, y, 24, 24)
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.damage = damage
        self.owner = owner
        self.attributes = attributes
        image_angle = math.degrees(math.atan2(-self.y_dir, self.x_dir))#y is negative because arctan assumes y increasing upward but y increases downward in pygame
        NUM_FRAMES = 8
        self.images = []
        for i in range(NUM_FRAMES - 1):
            image = pygame.image.load(os.path.join('assets', 'testing', 'Sword', f'Sword-0{i + 1}.png'))
            image_rot = pygame.transform.rotate(image, image_angle)
            self.images.append(image_rot)
        self.image_index = 0
        self.images_len = len(self.images)
        self.lifespan = self.images_len + 1

    def draw(self, surface):
        surface.blit(self.images[self.image_index], (self.rect.x, self.rect.y))
        self.image_index += 1
        if self.image_index >= self.images_len - 1:
            self.image_index = 0

    def step(self):
        self.rect.x = self.owner.rect.x + (self.x_dir * 64)
        self.rect.y = self.owner.rect.y + (self.y_dir * 64)
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.destroy(self)
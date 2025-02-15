import pygame
import pygame.geometry
from Circle import Circle
from Colours import Colours
from game_objects.GameObjects import GameObject
import sys
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from powers.Powers import AtlasStone, Power
sys.path.append(os.path.abspath('../'))
import Config
import math
import utils

class Projectile(GameObject):
    def __init__(self, x, y, power: "Power", attributes = list()):
        super().__init__(x, y, power.owner.command_registry)
        self.rect = utils.create_rect(x, y, 24, 24)
        self.power = power
        self.owner = power.owner
        self.attributes = attributes

class Bullet(Projectile):

    def __init__(self, x, y, x_speed, y_speed, power: "Power", colour, attributes = list()):
        super().__init__(x, y, power, attributes)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            if collide != self.owner:
                self.deal_damage(self.power, collide, 5, self.attributes)
                self.destroy(self)

class Bomb(Projectile):

    def __init__(self, x, y, power: "Power", fuse, explosion_radius, attributes = list()):
        super().__init__(x, y, power, attributes)
        self.x_speed = 0
        self.y_speed = 0
        self.fuse = fuse
        self.explosion_radius = explosion_radius

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.AshGrey.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)#should this be this way? knocking bombs away and such would be fun
        self.fuse -= 1
        if self.fuse <= 0:
            collision_circle = pygame.geometry.Circle(self.rect.centerx, self.rect.centery, self.explosion_radius)
            collide = Circle.collideobjectsall(collision_circle, self.owner.solids_not_me())
            for collision in collide:
                self.owner.deal_damage(self.power, collision, 25, [])
                self.owner.map.add_screen_shake(30)
            self.destroy(self)

class Sword(Projectile):

    def __init__(self, x, y, power: "Power", damage, x_dir, y_dir, attributes = list()):
        super().__init__(x, y, power, attributes)
        self.rect = utils.create_rect(x, y, 256, 256)
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.damage = damage
        image_angle = math.degrees(math.atan2(-self.y_dir, self.x_dir))#y is negative because arctan assumes y increasing upward but y increases downward in pygame
        pre_images = [image for image in SWORD_IMAGES]
        self.images = []
        NUM_FRAMES = 20
        for i in range(NUM_FRAMES - 1):
            image_rot, self.rect = utils.rot_center(pre_images[i], self.rect, image_angle)
            self.images.append(image_rot)
        self.image_index = 0
        self.curr_step = 0
        self.images_len = len(self.images)
        self.max_step = self.images_len + 1
        self.active_frame_start = 7
        self.active_frame_end = 11
        self.already_hit = []

    def draw(self, surface):
        surface.blit(self.images[self.image_index], (self.rect.x, self.rect.y))
        #pygame.draw.rect(surface, Colours.Black.value, self.rect)
        self.image_index += 1
        if self.image_index >= self.images_len - 1:
            self.image_index = 0

    def step(self):
        self.rect.centerx = self.owner.rect.centerx
        self.rect.centery = self.owner.rect.centery
        self.curr_step += 1
        if self.curr_step >= self.max_step:
            self.destroy(self)
        if self.curr_step >= self.active_frame_start and self.curr_step <= self.active_frame_end:
            hitbox = utils.create_rect(self.owner.rect.centerx + (self.x_dir * 64), self.owner.rect.centery + (self.y_dir * 64), 64, 64)
            solids_not_me = self.owner.solids_not_me()
            collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
            if collide != []:
                for collision in collide:
                    if collision not in self.already_hit:
                        self.owner.deal_damage(self.power, collision, self.damage, [])
                        self.already_hit.append(collision)
                        self.owner.map.add_screen_shake(30)

class SniperBullet(Projectile):

    def __init__(self, x, y, target: "GameObject", power: "Power", colour, attributes = list()):
        super().__init__(x, y, power, attributes)
        target_xdist = target.rect.centerx - self.rect.centerx
        target_ydist = target.rect.centery - self.rect.centery
        target_angle = math.atan2(-target_ydist, target_xdist)
        speed = 48
        self.x_speed = speed * math.cos(target_angle)
        self.y_speed = speed * -math.sin(target_angle)
        self.damage = 30
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            if collide != self.owner:
                self.deal_damage(self.power, collide, self.damage, self.attributes)
                self.destroy(self)

class AtlasBullet(Projectile):

    def __init__(self, x, y, x_speed, y_speed, power: "AtlasStone", colour, attributes = list()):
        super().__init__(x, y, power, attributes)
        self.rect = utils.create_rect(x, y, 128, 128)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.colour = colour
        self.damage = power.damage

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            if collide != self.owner:
                if collide == self.owner.opponent:
                    self.power.damage *= 2 #should this factor in stuff like strength? what's an elegant way to do that?
                self.deal_damage(self.power, collide, self.damage, self.attributes)
                self.destroy(self)

class TeleportBullet(Projectile):

    def __init__(self, x, y, x_speed, y_speed, power: "Power", colour, attributes = list()):
        super().__init__(x, y, power, attributes)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            if collide != self.owner:
                self.deal_damage(self.power, collide, 5, self.attributes)
                if self.x_speed > 0:
                    self.owner.rect.right = collide.rect.left
                elif self.x_speed < 0:
                    self.owner.rect.left = collide.rect.right
                else:
                    self.owner.rect.centerx = self.rect.centerx

                if self.y_speed > 0:
                    self.owner.rect.bottom = collide.rect.top
                elif self.y_speed < 0:
                    self.owner.rect.top = collide.rect.bottom
                else:
                    self.owner.rect.centery = self.rect.centery
                self.destroy(self)

class ShieldBoomerang(Projectile):

    def __init__(self, x, y, x_speed, y_speed, power: "Power", colour, attributes = list()):
        super().__init__(x, y, power, attributes)
        self.x_speed = utils.floor_int_bidirectional(x_speed)
        self.y_speed = utils.floor_int_bidirectional(y_speed)
        x_dir = utils.sign(self.x_speed)
        y_dir = utils.sign(self.y_speed)
        self.x_decay = x_dir
        self.y_decay = y_dir
        self.colour = colour
        self.shield_amount = 25

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour.value, self.rect)

    def step(self):
        self.move(self.x_speed, self.y_speed, 0, 0)
        self.x_speed -= self.x_decay
        self.y_speed -= self.y_decay
        if self.rect.centerx < -16 or self.rect.centerx > Config.SCREEN_WIDTH or self.rect.centery < -16 or self.rect.centery > Config.SCREEN_HEIGHT:
            self.destroy(self)
        collide = self.rect.collideobjects(self.solids_not_me(), key=lambda o: o.rect)
        if collide != None:
            self.gain_shield(self.power, collide, self.shield_amount)
            self.destroy(self)

SWORD_IMAGES = []
NUM_FRAMES = 20
for i in range(NUM_FRAMES - 1):
    number = f"{i:05d}" #leading zeros
    image = pygame.image.load(os.path.join('assets', 'testing', 'Sword', f'Sword Slash_{number}.png'))
    SWORD_IMAGES.append(image)
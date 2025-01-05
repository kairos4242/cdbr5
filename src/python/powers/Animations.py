from abc import abstractmethod
import math
import random

import pygame

from Colours import Colours
from game_objects import Projectiles
from game_objects.GameObject import GameObject
from powers.Particles import GrowingSpark, Spark


class Animation():

    def __init__(self, duration: int, dir_x: int, dir_y: int, move_allowed: bool, owner: GameObject, interruptible: bool = False, interrupted_by_damage: bool = False):
        self.curr_step = 0
        self.duration = duration
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.interruptible = interruptible #can be interrupted by self
        self.interrupted_by_damage = interrupted_by_damage #is always interrupted by damage
        self.move_allowed = move_allowed
        self.owner = owner
        self.recast = False #allow the player to trigger the power a second time while the animation is still occurring e.g. playful/trickster

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

class DashAnimation(Animation):

    def __init__(self, duration, dir_x, dir_y, owner, dash_speed):
        super().__init__(duration, dir_x, dir_y, False, owner)
        self.dash_speed = dash_speed

    def step(self):
        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
        else:
            self.owner.move_direction(self.dir_x, self.dir_y, self.dash_speed, 0, 0, True)

class PlayfulAnimation(Animation):

    def __init__(self, owner):
        super().__init__(15, owner.move_xdir, owner.move_ydir, False, owner)
        self.recast = True

    def step(self):
        self.curr_step += 1
        if self.curr_step <= self.duration:
            self.owner.move_direction(self.dir_x, self.dir_y, 15, 0, 0, True)

class FalconPunchAnimation(Animation):

    def __init__(self, owner):
        super().__init__(90, owner.move_xdir, owner.move_ydir, False, owner)
        self.recast = False
        self.punch_frame = 75
        self.particles = []

        self.dist = 128
        """for angle in range(0, 360, 30):
            angle_radians = math.radians(angle)
            #angle_radians = angle
            self.particles.append(
                Spark(
                    math.cos(angle_radians) * dist + self.owner.rect.centerx, 
                    math.sin(angle_radians) * dist + self.owner.rect.centery, 
                    angle_radians + math.pi, #add pi to flip 180 degress so moving towards player
                    5, 
                    Colours.White
                )
            )"""

    def step(self):
        
        for particle in self.particles:
            particle.step()
        self.particles = [particle for particle in self.particles if particle.alive == True]

        if self.curr_step <= self.punch_frame - 45:
            step_angle = random.randint(1, 360)
            angle_radians = math.radians(step_angle)
            self.particles.append(
                GrowingSpark(
                    math.cos(angle_radians) * self.dist + self.owner.rect.centerx, 
                    math.sin(angle_radians) * self.dist + self.owner.rect.centery, 
                    angle_radians + math.pi, #add pi to flip 180 degrees so moving towards player
                    1,
                    5,
                    0.1,
                    Colours.White
                )
            )

            step_angle = random.randint(1, 360)
            angle_radians = math.radians(step_angle)
            self.particles.append(
                Spark(
                    math.cos(angle_radians) * self.dist + self.owner.rect.centerx, 
                    math.sin(angle_radians) * self.dist + self.owner.rect.centery, 
                    angle_radians + math.pi, #add pi to flip 180 degrees so moving towards player
                    5,
                    0.1,
                    Colours.White
                )
            )


        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
        if self.curr_step == self.punch_frame:
            hitbox = self.owner.create_rect(self.owner.rect.centerx + (self.dir_x * 64), self.owner.rect.centery + (self.dir_y * 64), 64, 64)
            solids_not_me = self.owner.solids_not_me()
            collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
            if collide != []:
                for collision in collide:
                    self.owner.deal_damage(collision, 25, [])
                    collision.outside_force_x = self.dir_x * 35
                    collision.outside_force_y = self.dir_y * 35
                    self.owner.map.screen_shake += 30

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


class BodySlamAnimation(Animation):

    def __init__(self, owner):
        super().__init__(25, owner.move_xdir, owner.move_ydir, False, owner)
        self.dash_speed = self.owner.calculate_movespeed() * 2

    def step(self):

        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
        self.owner.move_direction(self.dir_x, self.dir_y, self.dash_speed, 0, 0, True)
        hitbox = self.owner.create_rect(self.owner.rect.centerx + (self.dir_x * 8), self.owner.rect.centery + (self.dir_y * 8), 64, 64)
        solids_not_me = self.owner.solids_not_me()
        collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
        if collide != []:
            for collision in collide:
                self.owner.deal_damage(collision, 40, [])
                collision.outside_force_x = self.dir_x * 25
                collision.outside_force_y = self.dir_y * 25
                self.owner.map.screen_shake += 30
            self.owner.animation = None

class SniperRifleAnimation(Animation):

    def __init__(self, owner):
        super().__init__(60, owner.move_xdir, owner.move_ydir, False, owner, interrupted_by_damage=True)

    def step(self):
        self.curr_step += 1
        if self.curr_step == self.duration:
            Projectiles.SniperBullet(self.owner.rect.centerx, self.owner.rect.centery, self.owner.opponent, self.owner, self.owner.colour)
            self.owner.animation = None
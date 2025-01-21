from abc import abstractmethod
import math
import random
from Colours import Colours
from game_objects import Projectiles
from powers.Particles import GrowingSpark, Spark
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from powers.Powers import Power
import utils


class Timeline():

    def __init__(self, duration: int, dir_x: int, dir_y: int, move_allowed: bool, power: "Power", interruptible: bool = False, interrupted_by_damage: bool = False):
        self.curr_step = 0
        self.duration = duration
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.interruptible = interruptible #can be interrupted by self
        self.interrupted_by_damage = interrupted_by_damage #is always interrupted by damage
        self.move_allowed = move_allowed
        self.power = power
        self.owner = power.owner
        self.recast = False #allow the player to trigger the power a second time while the animation is still occurring e.g. playful/trickster

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def draw(self, surface):
        pass

class DashTimeline(Timeline):

    def __init__(self, duration, dir_x, dir_y, power, dash_speed):
        super().__init__(duration, dir_x, dir_y, False, power)
        self.dash_speed = dash_speed

    def step(self):
        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
        else:
            self.owner.move_direction(self.dir_x, self.dir_y, self.dash_speed, 0, 0, True)

class PlayfulTimeline(Timeline):

    def __init__(self, power):
        super().__init__(15, power.owner.move_xdir, power.owner.move_ydir, False, power)
        self.recast = True

    def step(self):
        self.curr_step += 1
        if self.curr_step <= self.duration:
            self.owner.move_direction(self.dir_x, self.dir_y, 15, 0, 0, True)

class FalconPunchTimeline(Timeline):

    def __init__(self, power):
        super().__init__(90, power.owner.move_xdir, power.owner.move_ydir, False, power)
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
            hitbox = utils.create_rect(self.owner.rect.centerx + (self.dir_x * 64), self.owner.rect.centery + (self.dir_y * 64), 64, 64)
            solids_not_me = self.owner.solids_not_me()
            collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
            if collide != []:
                for collision in collide:
                    self.owner.deal_damage(self.power, collision, 25, [])
                    collision.outside_force_x = self.dir_x * 35
                    collision.outside_force_y = self.dir_y * 35
                    self.owner.map.add_screen_shake(60)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)


class BodySlamTimeline(Timeline):

    def __init__(self, power):
        super().__init__(25, power.owner.move_xdir, power.owner.move_ydir, False, power)
        self.dash_speed = self.owner.calculate_movespeed() * 2

    def step(self):

        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
        self.owner.move_direction(self.dir_x, self.dir_y, self.dash_speed, 0, 0, True)
        hitbox = utils.create_rect(self.owner.rect.centerx + (self.dir_x * 8), self.owner.rect.centery + (self.dir_y * 8), 64, 64)
        solids_not_me = self.owner.solids_not_me()
        collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
        if collide != []:
            for collision in collide:
                self.owner.deal_damage(self.power, collision, 40, [])
                collision.outside_force_x = self.dir_x * 25
                collision.outside_force_y = self.dir_y * 25
                self.owner.map.add_screen_shake(30)
            self.owner.animation = None

class SniperRifleTimeline(Timeline):

    def __init__(self, power):
        super().__init__(60, power.owner.move_xdir, power.owner.move_ydir, False, power, interrupted_by_damage=True)

    def step(self):
        self.curr_step += 1
        if self.curr_step == self.duration:
            Projectiles.SniperBullet(self.owner.rect.centerx, self.owner.rect.centery, self.owner.opponent, self, self.owner.colour)
            self.owner.animation = None

class EmbraceTimeline(Timeline):

    def __init__(self, duration, dir_x, dir_y, power, dash_speed):
        super().__init__(duration, dir_x, dir_y, False, power)
        self.max_dash_speed = dash_speed
        self.current_dash_speed = 5
        self.hit_max = False

    def step(self):
        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
            return
        if self.hit_max == False:
            self.current_dash_speed += 3
            if self.current_dash_speed >= self.max_dash_speed:
                self.hit_max = True
        else:
            self.current_dash_speed = max(self.current_dash_speed - 3, 5)

        self.owner.move_direction(self.dir_x, self.dir_y, self.current_dash_speed, 0, 0, True)
        #check for collision
        hitbox = utils.create_rect(self.owner.rect.centerx + (self.dir_x * 2), self.owner.rect.centery + (self.dir_y * 2), 64, 64)
        solids_not_me = self.owner.solids_not_me()
        collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
        if collide != []:
            for collision in collide:
                if collision == self.owner.opponent:
                    self.owner.heal(self.power, self.owner, 10)
            self.owner.animation = None
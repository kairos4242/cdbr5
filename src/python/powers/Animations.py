from abc import abstractmethod

import pygame

from game_objects.GameObject import GameObject


class Animation():

    def __init__(self, duration: int, dir_x: int, dir_y: int, interruptible: bool, owner: GameObject):
        self.curr_step = 0
        self.duration = duration
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.interruptible = interruptible
        self.owner = owner
        self.recast = False #allow the player to trigger the power a second time while the animation is still occurring e.g. playful/trickster

    @abstractmethod
    def step(self):
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
            self.owner.move_direction(self.dir_x, self.dir_y, self.dash_speed, True)

class PlayfulAnimation(Animation):

    def __init__(self, owner):
        super().__init__(15, owner.move_xdir, owner.move_ydir, False, owner)
        self.recast = True

    def step(self):
        self.curr_step += 1
        if self.curr_step <= self.duration:
            self.owner.move_direction(self.dir_x, self.dir_y, 15, True)

class FalconPunchAnimation(Animation):

    def __init__(self, owner):
        super().__init__(90, owner.move_xdir, owner.move_ydir, False, owner)
        self.recast = True
        self.punch_frame = 75

    def step(self):
        self.curr_step += 1
        if self.curr_step == self.duration:
            self.owner.animation = None
        if self.curr_step == self.punch_frame:
            hitbox = self.owner.create_rect(self.owner.rect.x + (self.dir_x * 64), self.owner.rect.y + (self.dir_y * 64), 64, 64)
            solids_not_me = self.owner.solids_not_me()
            collide = hitbox.collideobjectsall(solids_not_me, key=lambda o: o.rect)
            if collide != []:
                for collision in collide:
                    self.owner.deal_damage(collision, 100, [])

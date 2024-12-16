from abc import abstractmethod

from game_objects.GameObject import GameObject


class Animation():

    def __init__(self, duration: int, dir_x: int, dir_y: int, interruptible: bool, owner: GameObject):
        self.curr_step = 0
        self.duration = duration
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.interruptible = interruptible
        self.owner = owner

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
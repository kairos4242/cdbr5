from game_objects.GameObject import GameObject
import pygame
from Colours import Colours
from ControlType import ControlType
from powers import Powers


class Player(GameObject):

    def __init__(self, x, y, control_type: ControlType):
        super().__init__(x, y)
        self.solid = True
        self.object_registry.add_to_global_solid_registry(self)
        self.powers = [Powers.FalconPunch(self)]
        self.control_type = control_type
        self.opponent = None

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.Red.value, self.rect)

        if self.animation != None:
            self.animation.draw(surface)

    def step(self):

        for power in self.powers:
            power.step()

        for effect in self.effects:
            if effect.duration == 0:
                self.effects.remove(effect)
            else:
                effect.duration -= 1

        if self.control_type == ControlType.HUMAN:
            # get keys
            # hotkey system here in future?

            movespeed = int(self.calculate_movespeed())
            keys = pygame.key.get_pressed()
            key_left = keys[pygame.K_a]
            key_right = keys[pygame.K_d]
            self.move_xdir = (-key_left + key_right) 

            key_up = keys[pygame.K_w]
            key_down = keys[pygame.K_s]
            self.move_ydir = (-key_up + key_down)

            key_shoot = keys[pygame.K_SPACE]

            if self.animation != None:
                if self.animation.recast == True:
                    if key_shoot:
                        self.use_power(0)
                self.animation.step()
            else:
                self.move_direction(self.move_xdir, self.move_ydir, movespeed, self.outside_force_x, self.outside_force_y, True)
                if key_shoot:
                    self.use_power(0) #this is bad practice, better way to do this without repeating?
        else:
            self.move_direction(0, 0, self.movespeed, self.outside_force_x, self.outside_force_y, True)

        self.apply_friction()

    def use_power(self, power_num: int):
        power_to_use = self.powers[power_num]
        if power_to_use.cooldown == 0:
            power_to_use.cooldown = power_to_use.max_cooldown
            power_to_use.on_use()

    def get_direction_to_opponent(self):
        x = self.rect.centerx - self.opponent.rect.centerx
        y = self.rect.centery - self.opponent.rect.centery
        print(x, y)

        total = abs(x) + abs(y)
        x /= total
        y /= total
        print(x, y)

        return [x, y]
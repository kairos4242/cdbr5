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
        self.powers = [Powers.Blink(self)]
        self.control_type = control_type

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.Red.value, self.rect)

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
            move_x = self.move_xdir * movespeed

            key_up = keys[pygame.K_w]
            key_down = keys[pygame.K_s]
            self.move_ydir = (-key_up + key_down)
            move_y = self.move_ydir * movespeed
            
            self.move_tangible(move_x, move_y)

            key_shoot = keys[pygame.K_SPACE]
            if key_shoot:
                self.use_power(0)

    def use_power(self, power_num: int):
        power_to_use = self.powers[power_num]
        if power_to_use.cooldown == 0:
            power_to_use.cooldown = power_to_use.max_cooldown
            power_to_use.on_use()
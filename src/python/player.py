from GameObject import GameObject
import pygame
from Colours import Colours
from ControlType import ControlType


class Player(GameObject):

    def __init__(self, x, y, control_type: ControlType):
        super().__init__(x, y)
        self.solid = True
        self.object_registry.add_to_global_solid_registry(self)

        self.control_type = control_type

    def draw(self, surface):
        pygame.draw.rect(surface, Colours.Red.value, self.rect)

    def step(self):
        if self.control_type == ControlType.HUMAN:
            # get keys
            # hotkey system here in future?
            key = pygame.key.get_pressed()
            key_left = key[pygame.K_a]
            key_right = key[pygame.K_d]
            move_x = (-key_left + key_right) * self.movespeed

            key_up = key[pygame.K_w]
            key_down = key[pygame.K_s]
            move_y = (-key_up + key_down) * self.movespeed
            
            self.move_tangible(move_x, move_y)
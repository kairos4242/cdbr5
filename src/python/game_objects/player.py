from CommandRegistry import CommandRegistry
from commands.MoveCommand import MoveCommand
from commands.UsePowerCommand import UsePowerCommand
from game_objects.GameObject import GameObject
import pygame
from Colours import Colours
from ControlType import ControlType
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CdbrLogic import Map


class Player(GameObject):

    def __init__(self, x, y, control_type: ControlType, powers, colour, map: "Map", command_registry: "CommandRegistry", image='Player 1.png'):
        super().__init__(x, y, command_registry)
        self.make_solid()
        self.powers = powers
        self.control_type = control_type
        self.opponent = None
        self.colour = colour
        self.image = pygame.image.load(os.path.join('assets', 'testing', image)).convert_alpha()
        self.map = map

    def draw(self, surface):
        #pygame.draw.rect(surface, self.colour, self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))

        if self.animation != None:
            self.animation.draw(surface)

    def step(self):

        for power in self.powers:
            power.step()

        if self.animation != None:
            self.animation.step()

        for effect in self.effects:
            if effect.duration == 0:
                self.effects.remove(effect)
            else:
                effect.duration -= 1

        keys = pygame.key.get_pressed()
        movespeed = int(self.calculate_movespeed())

        if self.control_type == ControlType.HUMAN:
            # get keys
            # hotkey system here in future?
            key_left = keys[pygame.K_a]
            key_right = keys[pygame.K_d]
            key_up = keys[pygame.K_w]
            key_down = keys[pygame.K_s]
            key_shoot = keys[pygame.K_SPACE]
            key_power2 = keys[pygame.K_j]

        elif self.control_type == ControlType.HUMAN_PLAYER2:
            key_left = keys[pygame.K_LEFT]
            key_right = keys[pygame.K_RIGHT]
            key_up = keys[pygame.K_UP]
            key_down = keys[pygame.K_DOWN]
            key_shoot = False
            key_power2 = False
            events = self.map.events
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        key_shoot = True
                    elif event.button == 3:
                        key_power2 = True

        self.move_xdir = (-key_left + key_right)
        self.move_ydir = (-key_up + key_down)

        self.move()

        if key_shoot:
            self.use_power(0)
        if key_power2:
            self.use_power(1)

        self.apply_friction()

    def move(self):
        if self.animation != None:
            if not self.animation.move_allowed:
                return
        MoveCommand(self, self.command_registry).execute()

    def use_power(self, power_num: int):
        if self.animation != None:
            if self.animation.recast != True:
                return
        power_to_use = self.powers[power_num]
        if power_to_use.cooldown == 0:
            UsePowerCommand(power_to_use, self, self.command_registry).execute()

    def get_direction_to_opponent(self):
        x = self.rect.centerx - self.opponent.rect.centerx
        y = self.rect.centery - self.opponent.rect.centery
        print(x, y)

        total = abs(x) + abs(y)
        x /= total
        y /= total
        print(x, y)

        return [x, y]
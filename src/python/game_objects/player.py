from commands.CommandRegistry import CommandRegistry
from HotkeyManager import HotkeyManager
from commands.MoveCommand import MoveCommand
from commands.UsePowerCommand import UsePowerCommand
from game_objects.GameObjects import GameActor
import pygame
from ControlType import ControlType
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from CdbrLogic import Map


class Player(GameActor):

    def __init__(self, x, y, control_type: ControlType, powers, colour, map: "Map", command_registry: "CommandRegistry", hotkey_manager: "HotkeyManager", image='Player 1.png', name="Player 1"):
        super().__init__(x, y, command_registry)
        self.make_solid()
        self.powers = powers
        self.control_type = control_type
        self.hotkey_manager = hotkey_manager
        self.opponent = None
        self.colour = colour
        self.name = name
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

        self.move()

        self.apply_friction()

    def move(self):
        if self.animation != None:
            if not self.animation.move_allowed:
                return
        self.move_direction(
            self.move_xdir, 
            self.move_ydir, 
            int(self.calculate_movespeed()),
            self.outside_force_x,
            self.outside_force_y,
            True
        )

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
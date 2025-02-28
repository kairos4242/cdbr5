from animations.Animations import AnimationManager
from commands.CommandRegistry import CommandRegistry
from HotkeyManager import HotkeyManager
from commands.MoveCommand import MoveCommand
from commands.UsePowerCommand import UsePowerCommand
from game_objects.GameObjects import GameActor, GameObject
import pygame
from ControlType import ControlType
import os
from typing import TYPE_CHECKING

from game_objects.Teams import Team
from powers.Powers import Power
if TYPE_CHECKING:
    from CdbrLogic import Map

class PlayerPrototype:

    def __init__(
            self,
            money: int,
            income: int,
            win_bonus: int,
            powers: list[Power],
            colour,
            name
    ):
        self.money = money
        self.income = income
        self.win_bonus = win_bonus
        self.powers = powers
        self.colour = colour
        self.name = name

    def get_income(self):
        self.money += self.income

    def get_win_bonus(self):
        self.money += self.win_bonus

    def to_player(self, x, y, control_type, team, map, command_registry, hotkey_manager, animation_manager, image):
        new_player = Player(
            x,
            y,
            control_type,
            self.powers,
            self.colour,
            team,
            map,
            command_registry=command_registry,
            hotkey_manager=hotkey_manager,
            animation_manager=animation_manager,
            image=image,
            name=self.name,
            prototype = self
        )

        for power in self.powers:
            power.attach(new_player)

        return new_player

class Player(GameActor):

    def __init__(
            self, 
            x, 
            y, 
            control_type: ControlType, 
            powers, 
            colour,
            team: "Team",
            map: "Map", 
            command_registry: "CommandRegistry", 
            hotkey_manager: "HotkeyManager", 
            animation_manager: "AnimationManager", 
            image='Player 1.png', 
            name="Player 1",
            prototype: "PlayerPrototype" = None
    ):
        super().__init__(x, y, command_registry)
        self.make_solid()
        self.powers = powers
        self.control_type = control_type
        self.hotkey_manager = hotkey_manager
        self.animation_manager = animation_manager
        self.colour = colour
        self.prototype = prototype

        self.team = team
        if not self.team.is_member(self):
            self.team.add_member(self)

        self.opponent = None

        self.name = name
        self.image = pygame.image.load(os.path.join('assets', 'testing', image)).convert_alpha()
        self.map = map

    def draw(self, surface):
        #pygame.draw.rect(surface, self.colour, self.rect)
        surface.blit(self.image, (self.rect.x, self.rect.y))

        if self.timeline != None:
            self.timeline.draw(surface)

    def step(self):

        for power in self.powers:
            power.step()

        if self.timeline != None:
            self.timeline.step()

        for effect in self.effects:
            if effect.duration == 0:
                self.effects.remove(effect)
            else:
                effect.duration -= 1

        self.move()

        self.apply_friction()

    def move(self):
        if self.timeline != None:
            if not self.timeline.move_allowed:
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
        if self.timeline != None:
            if self.timeline.recast != True:
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
    
    def on_destroy(self, source: "GameObject"):
        self.command_registry.add_player_died(source, self)
    
class NeutralPlayer(Player):

    def __init__(
            self, 
            powers, 
            colour,
            team: "Team",
            map: "Map", 
            command_registry: "CommandRegistry", 
            hotkey_manager: "HotkeyManager", 
            animation_manager: "AnimationManager"
    ):
        self.powers = powers
        self.command_registry = command_registry
        self.hotkey_manager = hotkey_manager
        self.animation_manager = animation_manager
        self.colour = colour

        self.team = team
        if not self.team.is_member(self):
            self.team.add_member(self)

        self.map = map
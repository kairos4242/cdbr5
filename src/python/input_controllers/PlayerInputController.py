
from HotkeyManager import HotkeyManager
from Hotkeys import Hotkeys
from typing import TYPE_CHECKING

from commands.UsePowerCommand import UsePowerCommand
from input_controllers.InputController import InputController
if TYPE_CHECKING:
    from commands.Command import Command
    from Clock import Clock
from commands.MoveCommand import MoveCommand
from game_objects.player import Player


class PlayerInputController(InputController):

    def __init__(self, hotkey_manager: "HotkeyManager"):

        #hardcoding this to two players for now, not thrilled about it
        self.hotkey_manager = hotkey_manager


    def get_input(self, player1: "Player", player2: "Player", keys, clock: "Clock") -> list["Command"]:

        moves = self.get_move_input(player1, player2, keys, clock)
        powers = self.get_power_input(player1, player2, keys, clock)

        all_commands = moves + powers

        return all_commands

    def get_move_input(self, player1: "Player", player2: "Player", keys, clock: "Clock") -> list["Command"]:

        commands = []
        
        # get keys
        # hotkey system here in future?
        key_left = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_LEFT)
        key_right = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_RIGHT)
        key_up = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_UP)
        key_down = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_DOWN)

        move_xdir = (-key_left + key_right)
        move_ydir = (-key_up + key_down)
        if move_xdir != player1.move_xdir or move_ydir != player1.move_ydir:
            commands.append(MoveCommand(player1, move_xdir, move_ydir, clock.get_ticks()))

        key_left = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_LEFT)
        key_right = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_RIGHT)
        key_up = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_UP)
        key_down = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_DOWN)

        move_xdir = (-key_left + key_right)
        move_ydir = (-key_up + key_down)
        if move_xdir != player2.move_xdir or move_ydir != player2.move_ydir:
            commands.append(MoveCommand(player2, move_xdir, move_ydir, clock.get_ticks()))

        return commands


    def get_power_input(self, player1: "Player", player2: "Player", keys, clock: "Clock"):

        commands = []

        p1_keys = [
            self.hotkey_manager.check_pressed(keys, Hotkeys.P1_AB1),
            self.hotkey_manager.check_pressed(keys, Hotkeys.P1_AB2),
            self.hotkey_manager.check_pressed(keys, Hotkeys.P1_AB3)
        ]

        for index, key in enumerate(p1_keys):
            if key:
                power_index = index - 1
                power = player1.powers[power_index]
                if power.cooldown <= 0:
                    print("Using power")
                    commands.append(UsePowerCommand(player1, power_index, clock.get_ticks()))

        
        p2_keys = [
            self.hotkey_manager.check_pressed(keys, Hotkeys.P2_AB1),
            self.hotkey_manager.check_pressed(keys, Hotkeys.P2_AB2),
            self.hotkey_manager.check_pressed(keys, Hotkeys.P2_AB3)
        ]

        for index, key in enumerate(p2_keys):
            if key:
                power_index = index - 1
                power = player2.powers[power_index]
                if power.cooldown <= 0:
                    print("Using power")
                    commands.append(UsePowerCommand(player2, power_index, clock.get_ticks()))

        return commands
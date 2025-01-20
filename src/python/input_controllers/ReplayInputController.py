
from HotkeyManager import HotkeyManager
from Hotkeys import Hotkeys
from typing import TYPE_CHECKING

from input_controllers.InputController import InputController
from commands.Command import Command
if TYPE_CHECKING:
    
    from Clock import Clock
from commands.MoveCommand import MoveCommand
from game_objects.player import Player


class ReplayInputController(InputController):

    def __init__(self, hotkey_manager: "HotkeyManager", filename: str):

        #hardcoding this to two players for now, not thrilled about it
        self.hotkey_manager = hotkey_manager
        self.command_list = self.load_replay(filename)

    def load_replay(self, filename: str) -> list[Command]:
        with open(filename, "r") as f:
            assembled_commands = []
            commands = f.readlines()
            for command in commands:
                print(command)
                name, xdir, ydir, timestamp = command.split('!')
                assembled_command = MoveCommand(name, int(xdir), int(ydir), int(timestamp))
                assembled_commands.append(assembled_command)
            f.close()
        return assembled_commands


    def get_move_input(self, player1: "Player", player2: "Player", keys, clock: "Clock") -> list["Command"]:

        commands = [] #type: list[Command]
        curr_step = clock.get_ticks()

        while len(self.command_list) > 0 and self.command_list[0].timestamp == curr_step:
            print("command found! appending")
            commands.append(self.command_list.pop(0))

        for command in commands:
            if command.target == player1.name:
                command.target = player1
            elif command.target == player2.name:
                command.target = player2
            else:
                raise Exception(f"name from replay unrecognized: {command.target}")

        return commands


    def get_power_input(self, player1: "Player", player2: "Player", keys):

        key_power1 = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_AB1)
        key_power2 = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_AB2)
        key_power3 = self.hotkey_manager.check_pressed(keys, Hotkeys.P1_AB3)


        key_power1 = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_AB1)
        key_power2 = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_AB2)
        key_power3 = self.hotkey_manager.check_pressed(keys, Hotkeys.P2_AB3)

from HotkeyManager import HotkeyManager
from Hotkeys import Hotkeys
from typing import TYPE_CHECKING

from commands.UsePowerCommand import UsePowerCommand
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
        self.step_commands = []

    def load_replay(self, filename: str) -> list[Command]:
        with open(filename, "r") as f:
            assembled_commands = []
            commands = f.readlines()
            for command in commands:
                print(command)
                command_type = command.split(',')[0]
                if command_type == "Move":
                    _, name, xdir, ydir, timestamp = command.split(',')
                    assembled_command = MoveCommand(name, int(xdir), int(ydir), int(timestamp))
                elif command_type == "Power":
                    _, name, index, timestamp = command.split(',')
                    assembled_command = UsePowerCommand(name, int(index), int(timestamp))
                else:
                    raise Exception(f"Unrecognized command type: {command_type}")
                assembled_commands.append(assembled_command)
            f.close()
        return assembled_commands
    
    def get_input(self, player1: "Player", player2: "Player", keys, clock: "Clock") -> list["Command"]:
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
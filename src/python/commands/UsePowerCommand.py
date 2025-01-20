from abc import abstractmethod

from commands.Command import Command
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player
    from commands.CommandRegistry import CommandRegistry
    from powers.Powers import Power


class UsePowerCommand(Command):

    def __init__(self, target: "Player", power_index: int, timestamp = None):
        super().__init__(target, timestamp)
        self.power_index = power_index

    def execute(self, command_registry: "CommandRegistry"):
        command_registry.add_active_command(self)
        #capture all the properties modified, all the objects created, all the objects destroyed in a list
        power = self.target.powers[self.power_index]
        power.cooldown = power.max_cooldown
        power.on_use()
        command_registry.clear_active_command()

    def undo(self):
        #for each property modified, change it back
        #for each object created, destroy it
        #for each object destroyed, recreate it
        pass

    def to_string(self):
        string = f"Power,{self.target.name},{self.power_index},{self.timestamp}\n"
        return string
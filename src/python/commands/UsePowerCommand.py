from abc import abstractmethod

from commands.Command import Command
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player
    from CommandRegistry import CommandRegistry
    from powers.Powers import Power


class UsePowerCommand(Command):

    def __init__(self, power: "Power", target: "Player", command_registry: "CommandRegistry"):
        super().__init__(target, command_registry)
        self.power = power

    def execute(self):
        #capture all the properties modified, all the objects created, all the objects destroyed in a list
        self.command_registry.add_active_command(self)
        self.power.cooldown = self.power.max_cooldown
        self.power.on_use()
        self.command_registry.clear_active_command()

    def undo(self):
        #for each property modified, change it back
        #for each object created, destroy it
        #for each object destroyed, recreate it
        pass
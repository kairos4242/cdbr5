from abc import abstractmethod

from commands.Command import Command
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player
    from commands.CommandRegistry import CommandRegistry
    from powers.Powers import Power


class UsePowerCommand(Command):

    def __init__(self, power: "Power", target: "Player"):
        super().__init__(target)
        self.power = power

    def execute(self):
        #capture all the properties modified, all the objects created, all the objects destroyed in a list
        self.power.cooldown = self.power.max_cooldown
        self.power.on_use()

    def undo(self):
        #for each property modified, change it back
        #for each object created, destroy it
        #for each object destroyed, recreate it
        pass
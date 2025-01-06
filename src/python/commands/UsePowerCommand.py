from abc import abstractmethod

from commands.Command import Command
from game_objects.player import Player


class UsePowerCommand(Command):

    def __init__(self, power_index: int, target: "Player"):
        super().__init__(target)
        self.pre_x = None
        self.pre_y = None
        self.power_index = power_index

    def execute(self):
        #capture all the properties modified, all the objects created, all the objects destroyed in a list
        pass


    def undo(self):
        #for each property modified, change it back
        #for each object created, destroy it
        #for each object destroyed, recreate it
        pass
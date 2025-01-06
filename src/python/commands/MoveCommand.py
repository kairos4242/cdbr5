from abc import abstractmethod

from commands.Command import Command
from game_objects.player import Player


class MoveCommand(Command):

    def __init__(self, target: "Player"):
        super().__init__(target)
        self.pre_x = None
        self.pre_y = None

    @abstractmethod
    def execute(self):
        self.command_registry.add_active_command(self)
        self.pre_x = self.target.rect.centerx
        self.pre_y = self.target.rect.centery
        self.target.move_direction(
            self.target.move_xdir, 
            self.target.move_ydir, 
            self.target.movespeed, 
            self.target.outside_force_x, 
            self.target.outside_force_y, 
            True
        )
        self.command_registry.clear_active_command()

    @abstractmethod
    def undo(self):
        self.target.rect.centerx = self.pre_x
        self.target.rect.centery = self.pre_y
        for modification in self.property_modifications:
            modification.undo()
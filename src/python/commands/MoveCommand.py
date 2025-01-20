from abc import abstractmethod


from commands.Command import Command
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player
    from commands.CommandRegistry import CommandRegistry


class MoveCommand(Command):

    def __init__(self, target: "Player", x_dir: int, y_dir: int, timestamp = None):
        super().__init__(target, timestamp)
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.pre_x = None
        self.pre_y = None

    def execute(self, command_registry: "CommandRegistry"):
        command_registry.add_active_command(self)
        self.pre_x = self.target.rect.centerx
        self.pre_y = self.target.rect.centery
        self.target.move_xdir = self.x_dir
        self.target.move_ydir = self.y_dir
        command_registry.clear_active_command()

    def undo(self):
        self.target.rect.centerx = self.pre_x
        self.target.rect.centery = self.pre_y
        for modification in self.property_modifications:
            modification.undo()

    def to_string(self):
        string = f"{self.target.name}!{self.x_dir}!{self.y_dir}!{self.timestamp}\n"
        return string
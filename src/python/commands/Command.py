from abc import abstractmethod

from commands.CommandRegistry import CommandRegistry
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player


class Command:

    def __init__(self, target: "Player", timestamp: int):
        self.target = target
        self.timestamp = timestamp
        self.property_modifications = []
        self.objects_created = []
        self.objects_destroyed = []

    @abstractmethod
    def execute(self, command_registry: "CommandRegistry"):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def to_string(self):
        pass
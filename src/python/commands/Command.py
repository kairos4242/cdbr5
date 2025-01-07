from abc import abstractmethod

from CommandRegistry import CommandRegistry
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.player import Player


class Command:

    def __init__(self, target: "Player", command_registry: "CommandRegistry"):
        self.target = target
        self.property_modifications = []
        self.objects_created = []
        self.objects_destroyed = []
        self.command_registry = command_registry

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass
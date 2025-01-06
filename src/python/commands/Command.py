from abc import abstractmethod

from CommandRegistry import CommandRegistry
from game_objects.player import Player


class Command:

    def __init__(self, target: "Player"):
        self.target = target
        self.property_modifications = []
        self.objects_created = []
        self.objects_destroyed = []
        self.command_registry = CommandRegistry()

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass
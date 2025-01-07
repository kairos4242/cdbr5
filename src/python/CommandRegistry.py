from typing import TYPE_CHECKING

from Clock import Clock
from commands.ObjectCreation import ObjectCreation
from commands.ObjectDestruction import ObjectDestruction
from game_objects.GameObject import GameObject
if TYPE_CHECKING:
    from commands.Command import Command
from commands.PropertyModification import PropertyModification

class CommandRegistry:
    
    def __init__(self, clock: Clock):
        self.clock = clock
        self.active_command = None
        self.other_modifications = []
        self.other_creations = []
        self.other_destructions = []

    def add_active_command(self, command: "Command"):
        self.active_command = command

    def clear_active_command(self):
        self.active_command = None
    
    def add_modification(self, target, property_name, property_old_value, property_new_value):
        modification = PropertyModification(target, property_name, property_old_value, property_new_value, self.clock.get_ticks())
        if self.active_command != None:
            self.active_command.property_modifications.append(modification)
        else:
            self.other_modifications.append(modification) # still not sure how this will come into play precisely, might end up rewritten

    def add_creation(self, object: "GameObject"):
        # should this allow optionally passing in a timestamp?
        creation = ObjectCreation(object, self.clock.get_ticks())
        if self.active_command != None:
            self.active_command.objects_created.append(creation)
        else:
            self.other_creations.append(creation)

    def add_destruction(self, object: "GameObject"):
        destruction = ObjectDestruction(object, self.clock.get_ticks())
        if self.active_command != None:
            self.active_command.objects_destroyed.append(destruction)
        else:
            self.other_destructions.append(destruction)
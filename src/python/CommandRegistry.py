from typing import TYPE_CHECKING

from Clock import Clock
if TYPE_CHECKING:
    from commands.Command import Command
from commands.PropertyModification import PropertyModification

class CommandRegistry:
    
    def __init__(self, clock: Clock):
        self.clock = clock
        self.active_command = None
        self.other_modifications = []

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
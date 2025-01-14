from typing import TYPE_CHECKING

from Clock import Clock
from commands.CreationEvent import CreationEvent
from commands.DestructionEvent import DestructionEvent
from commands.Event import Event
from commands.EventManager import EventManager
from commands.EventType import EventType
from commands.ObjectCreation import ObjectCreation
from commands.ObjectDestruction import ObjectDestruction
from commands.PowerUsageEvent import PowerUsageEvent
from commands.PropertyModificationEvent import PropertyModificationEvent
from game_objects.GameObject import GameObject
if TYPE_CHECKING:
    from commands.Command import Command
from commands.PropertyModification import PropertyModification

import pickle

class CommandRegistry:
    
    def __init__(self, clock: Clock, event_manager: EventManager):
        self.clock = clock
        self.active_command = None
        self.other_modifications = []
        self.other_creations = []
        self.other_destructions = []
        self.event_manager = event_manager

    def add_active_command(self, command: "Command"):
        self.active_command = command

    def clear_active_command(self):
        self.active_command = None
    
    def add_modification(self, target, property_name, property_old_value, property_new_value):
        #having both of these should be temporary, modification should be phased out in favour of more generic event
        modification = PropertyModification(target, property_name, property_old_value, property_new_value, self.clock.get_ticks())

        event = PropertyModificationEvent(None, target, self.clock.get_ticks(), property_name, property_old_value, property_new_value)
        self.event_manager.notify(event)

        if self.active_command != None:
            self.active_command.property_modifications.append(modification)
        else:
            self.other_modifications.append(modification) # still not sure how this will come into play precisely, might end up rewritten

    def add_creation(self, object: "GameObject"):
        # should this allow optionally passing in a timestamp?
        creation = ObjectCreation(object, self.clock.get_ticks())
        event = CreationEvent(None, object, self.clock.get_ticks())
        self.event_manager.notify(event)

        if self.active_command != None:
            self.active_command.objects_created.append(creation)
        else:
            self.other_creations.append(creation)

    def add_destruction(self, object: "GameObject"):
        destruction = ObjectDestruction(object, self.clock.get_ticks())
        event = DestructionEvent(None, object, self.clock.get_ticks())
        self.event_manager.notify(event)

        if self.active_command != None:
            self.active_command.objects_destroyed.append(destruction)
        else:
            self.other_destructions.append(destruction)

    def add_power_used(self, power):
        event = PowerUsageEvent(power.owner, power.owner, self.clock.get_ticks(), power)
        # maybe need to ponder a bit more here about what precisely source and target means in this context?
        self.event_manager.notify(event)

    def save_replay(self, filename: str):
        output = pickle.dumps(self)
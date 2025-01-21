from events.Event import Event
from events.EventType import EventType



class PropertyModificationEvent(Event):

    def __init__(self, source, target, time, property_name, old_value, new_value):
        super().__init__(source, target, time, property_name, EventType.PROPERTY_MODIFICATION)
        self.old_value = old_value
        self.new_value = new_value

    def print_self(self):
        pass #TODO
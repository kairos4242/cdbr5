from events.Event import Event
from events.EventType import EventType

class ShieldEvent(Event):

    def __init__(self, source, target, time, amount):
        super().__init__(source, target, time, None, EventType.SHIELD)
        self.amount = amount

    def print_self(self):
        pass #TODO
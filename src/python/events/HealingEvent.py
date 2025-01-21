from events.Event import Event
from events.EventType import EventType



class HealingEvent(Event):

    def __init__(self, source, target, time, amount):
        super().__init__(source, target, time, None, EventType.HEALING)
        self.amount = amount

    def print_self(self):
        pass #TODO
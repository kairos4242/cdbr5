from events.Event import Event
from events.EventType import EventType



class PowerUsageEvent(Event):

    def __init__(self, source, target, time, power):
        super().__init__(source, target, time, None, EventType.POWER_USAGE)
        self.power = power

    def print_self(self):
        pass #TODO
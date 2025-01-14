from commands.Event import Event
from commands.EventType import EventType


class CreationEvent(Event):

    def __init__(self, source, target, time):
        super().__init__(source, target, time, "EXISTENCE", EventType.CREATION)

    def print_self(self):
        pass #TODO
from commands.Event import Event
from commands.EventType import EventType



class DestructionEvent(Event):

    def __init__(self, source, target, time):
        super().__init__(source, target, time, "EXISTENCE", EventType.DESTRUCTION)

    def print_self(self):
        pass #TODO
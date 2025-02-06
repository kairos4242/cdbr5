from events.Event import Event
from events.EventType import EventType

class PlayerDeathEvent(Event):

    def __init__(self, source, target, time):
        #source here refers to the killer, target refers to the killed
        super().__init__(source, target, time, None, EventType.PLAYER_DEATH)

    def print_self(self):
        pass #TODO
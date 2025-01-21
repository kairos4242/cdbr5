from abc import abstractmethod
from events.Event import Event

class EventListener:

    def __init__(self):
        pass

    @abstractmethod
    def notify(self, event: Event):
        pass
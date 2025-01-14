from abc import abstractmethod
from commands.Event import Event

class EventListener:

    def __init__(self):
        pass

    @abstractmethod
    def notify(self, event: Event):
        pass
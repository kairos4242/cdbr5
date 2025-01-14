from collections import defaultdict
from commands.EventListener import EventListener
from commands.Event import Event
from commands.EventType import EventType


class EventManager:

    def __init__(self):
        self.listeners = defaultdict(list)

    def subscribe(self, event_type: EventType, property_name: str, listener: EventListener):
        self.listeners[(event_type, property_name)].append(listener)

    def unsubscribe(self, event_type: EventType, property_name, listener: EventListener):
        self.listeners[(event_type, property_name)].remove(listener)

    def notify(self, event: Event):
        for listener in self.listeners[(event.event_type, event.property_name)]:
            listener.notify(event)
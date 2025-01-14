class Event:

    def __init__(self, source, target, time, property_name, event_type):
        self.source = source
        self.target = target
        self.time = time
        self.property_name = property_name
        self.event_type = event_type

    def print_self(self):
        pass #TODO
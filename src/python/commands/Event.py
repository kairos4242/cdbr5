class Event:

    def __init__(self, event_type, target, old_value, new_value, time, property_name = "EXISTENCE"):
        self.event_type = event_type
        self.target = target
        self.property_name = property_name
        self.old_value = old_value
        self.new_value = new_value
        self.time = time

    def print_self(self):
        pass #TODO
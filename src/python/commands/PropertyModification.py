class PropertyModification:

    def __init__(self, target, property_name, property_old_value, property_new_value, timestamp):
        self.target = target
        self.property_name = property_name
        self.property_old_value = property_old_value
        self.property_new_value = property_new_value
        self.timestamp = timestamp

        print(f"Property named {property_name} modified at {str(timestamp)}, previously was {str(property_old_value)} and is now {str(property_new_value)}")

    def undo(self):
        setattr(self.target, self.property_name, self.property_old_value)
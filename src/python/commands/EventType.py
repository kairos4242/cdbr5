from enum import Enum

class EventType(Enum):
    CREATION = 0
    DESTRUCTION = 1
    PROPERTY_MODIFICATION = 2
    POWER_USAGE = 3
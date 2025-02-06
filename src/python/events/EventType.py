from enum import Enum

class EventType(Enum):
    CREATION = 0
    DESTRUCTION = 1
    PROPERTY_MODIFICATION = 2
    POWER_USAGE = 3
    DAMAGE_DEALT = 4
    HEALING = 5
    SHIELD = 6
    PLAYER_DEATH = 7
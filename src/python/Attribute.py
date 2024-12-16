from enum import Enum

class Attribute(Enum):
    Christian = 0
    Fire = 1
    Poison = 2

class Property(Enum):
    MOVESPEED = 0
    HEALTH = 1
    MAX_HP = 2
    DAMAGE = 3

class ModificationType(Enum):
    FLAT = 0
    PERCENT = 1
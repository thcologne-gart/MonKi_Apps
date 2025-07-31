from enum import Enum

#class Enums(Enum):
#    def __init__(self):
#        super().__init__()


class TriggerType(Enum):
    TIMER = 0
    EVENT = 1
    REQUEST = 2


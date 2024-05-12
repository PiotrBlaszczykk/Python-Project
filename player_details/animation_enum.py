from enum import Enum, auto

class State(Enum):
    IDLE_LEFT = auto()
    IDLE_RIGHT = auto()
    MOVING_LEFT = auto()
    MOVING_RIGHT = auto()
    AIRBORNE_LEFT = auto()
    AIRBORNE_RIGHT = auto()

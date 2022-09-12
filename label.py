from enum import Enum, auto, unique


@unique
class Label(Enum):
    NEGATIVE = auto()
    POSITIVE = auto()
    UNKNOWN = auto()

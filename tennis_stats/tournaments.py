from aenum import Enum


class Tour(Enum):
    Australian = 1
    French = 2
    Wimbledon = 3
    USopen = 4


class Result(Enum):
    W = 0
    F = 1
    SF = 2
    QF = 3
    R4 = 4
    R3 = 5
    R2 = 6
    R1 = 7

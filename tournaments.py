from aenum import Enum


class Tour(Enum):
    australian = 1
    french = 2
    wimbledon = 3
    usopen = 4


class Result(Enum):
    W = 0
    F = 1
    SF = 2
    QF = 3
    R4 = 4
    R3 = 5
    R2 = 6
    R1 = 7

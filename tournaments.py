from aenum import Enum

class Tour(Enum):
    australian = 1
    french = 2
    wimbledon = 3
    usopen = 4

class Result(Enum):
    win = 1
    semifinal = 2
    quarterfinal = 3
    round4 = 4
    round3 = 5
    round2 = 6
    round1 = 7


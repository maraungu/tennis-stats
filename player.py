from aenum import Enum


class Gender(Enum):
    female = 1
    male = 2


class Nationality(Enum):
    any = 1
    US = 2
    France = 3
    Germany = 4
    Russia = 5


class Players:
    def __init__(self, gender=Gender.female.name, birthyear='1950', link='https://en.wikipedia.org/wiki'
                                                                         '/List_of_female_tennis_players',
                 nationality=Nationality.any.name):
        self.gender = gender
        self.birthyear = birthyear
        self.link = link
        self.nationality = nationality

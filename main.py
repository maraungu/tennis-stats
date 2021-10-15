import scrape
from scrape import make_soup
import cmd, sys
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
    def __init__(self, gender=Gender.female.name, birthyear='1950', link='', alive=True,
                 nationality=Nationality.any.name):
        self.gender = gender
        self.birthyear = birthyear
        self.link = link
        self.alive = alive
        self.nationality = nationality


class TennisPlayersShell(cmd.Cmd):
    """This is a simple shell for interactive tennis stats"""
    intro = 'Welcome to the tennis stats shell.  Type help or ? to list commands. \n'
    prompt = '(tennis)'
    file = None

    default_player = Players()

    # --------- basic commands ----------
    def do_exit(self, arg):
        """Exit the shell"""
        print('Thank you for using tennis-stats')
        raise SystemExit()

    def do_showdefaults(self, arg):
        """Shows the default player parameters"""
        print("gender: {} \n birth year: {} \n alive: {} \n nationality: {}".format(self.default_player.gender,
                                                                                    self.default_player.birthyear,
                                                                                    self.default_player.alive,
                                                                                    self.default_player.nationality))

    def do_playergender(self, arg):
        """Choose player gender (male or female): PLAYERGENDER female"""
        print("hello")

    # if gender == 'male' or gender == 'Male':
    #     players.link = 'https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players'
    #     players.gender = gender
    #     print('yay male')
    # else:
    #     if gender == 'female' or gender == 'Female':
    #         players.link = 'https://en.wikipedia.org/wiki/List_of_female_tennis_players'
    #         players.gender = gender
    #         print('yay female')
    #     else:
    #         print('Cannot read answer')
    #
    # if birthyear >= '1950':
    #     make_soup(players.link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TennisPlayersShell().cmdloop()

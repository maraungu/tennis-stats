from scrape import make_soup
import cmd
from player import *


class TennisPlayersShell(cmd.Cmd):
    """This is a simple shell for interactive tennis stats"""
    intro = 'Welcome to the tennis stats shell.  Type help or ? to list commands. \n'
    prompt = '(tennis-stats)'
    file = None

    players = Players()

    # TODO: add pandas
    # dataframe =

    # --------- basic commands ----------
    def do_exit(self, arg):
        """Exit the shell"""
        print('Thank you for using tennis-stats')
        raise SystemExit()

    # -------- player settings -------------
    def do_showsettings(self, arg):
        """Shows the default player parameters"""
        print("gender: {} \n birth year: {} \n nationality: {}".format(self.players.gender,
                                                                       self.players.birthyear,
                                                                       self.players.nationality))

    def do_playergender(self, arg):
        """Choose player gender (male or female): PLAYERGENDER female"""
        if arg == 'female':
            self.players.gender = Gender.female.name
            self.players.link = 'https://en.wikipedia.org/wiki/List_of_female_tennis_players'
        else:
            if arg == 'male':
                self.players.gender = Gender.male.name
                self.players.link = 'https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players'

    # TODO: check input validity
    def do_birthyear(self, arg):
        """Choose earliest birth year of players: BIRTHYEAR 1958"""
        self.players.birthyear = arg

    def do_nationality(self, arg):
        """Choose player nationality"""
        self.players.nationality = arg

    # -------- tennis stats commands ----------------
    def do_generatedataframe(self, arg):
        if self.players.birthyear >= '1950':
            make_soup(self.players.link)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TennisPlayersShell().cmdloop()

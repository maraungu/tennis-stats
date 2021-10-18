import cmd
import readline
import rlcompleter

from player import *
from scrape import make_dataframe
from pandas import DataFrame


# ------- Making autocomplete work on Mac -------
class TabCompleter(rlcompleter.Completer):
    """Completer that supports indenting"""

    def complete(self, text, state):
        if not text:
            return ('    ', None)[state]
        else:
            return rlcompleter.Completer.complete(self, text, state)


readline.set_completer(TabCompleter().complete)

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind -e")
    readline.parse_and_bind("bind '\t' rl_complete")
else:
    readline.parse_and_bind("tab: complete")


# ----------- Shell commands  -------------------

class TennisPlayersShell(cmd.Cmd):
    """This is a simple shell for interactive tennis stats"""
    intro = 'Welcome to the tennis stats shell.  Type help or ? to list commands. \n'
    prompt = '(tennis-stats)'
    file = None

    players = Players()
    nationality_list = [nat.name for nat in Nationality]
    gender_list = [g.name for g in Gender]

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

    def complete_playergender(self, text, line, begidx, endidx):
        if not text:
            completions = self.gender_list
        else:
            completions = [g for g in self.gender_list if g.startswith(text)]
        return completions

    def do_birthyear(self, arg):
        """Choose earliest birth year of players: BIRTHYEAR 1958"""
        if arg < '2010' and arg > '1920':
            self.players.birthyear = arg
        else:
            print('Not a valid earliest birthyear')

    def do_nationality(self, arg):
        """Choose player nationality"""
        if arg and arg in self.nationality_list:
            self.players.nationality = arg
        else:
            print('Not a valid nationality')

    def complete_nationality(self, text, line, begidx, endidx):
        if not text:
            completions = self.nationality_list
        else:
            completions = [nat for nat in self.nationality_list if nat.startswith(text)]
        return completions

    # -------- tennis stats commands ----------------
    def do_generatedataframe(self, arg):
        if self.players.birthyear >= '1950':
            data = make_dataframe(self.players.link, self.players.gender, self.players.nationality, self.players.birthyear)

    # --------- basic commands ----------
    def do_exit(self, arg):
        """Exit the shell"""
        print('Thank you for using tennis-stats')
        raise SystemExit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TennisPlayersShell().cmdloop()

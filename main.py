import cmd
import readline
import rlcompleter
import pickle

import pandas
import analysis

from player import *
from scrape import make_dataframe
from tournaments import *
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
    tour_list = [t.name for t in Tour]
    data = pandas.DataFrame()

    # -------- player settings -------------
    def do_showdefaults(self, arg):
        """Shows the default player settings for male and female"""
        print('The following default settings are used: \n')
        if arg == 'female' or arg == 'male':
            print("gender: {} \n birth year: {} \n nationality: {}".format(arg,
                                                                           '1950',
                                                                           'any'))
        else:
            print("Not a valid gender.  Please input male or female")

    def complete_showdefaults(self, text, line, begidx, endidx):
        if not text:
            completions = self.gender_list
        else:
            completions = [g for g in self.gender_list if g.startswith(text)]
        return completions


    def do_showsettings(self, arg):
        """Shows the current player settings"""
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
        """
            Generate data frame based on the player settings.
            To check which settings apply, use command showsettings
        """
        if self.players.birthyear >= '1950':
            self.data = make_dataframe(self.players.link, self.players.gender, self.players.nationality, self.players.birthyear)
            #self.data.to_pickle('females.pkl')

    def do_displaydataframe(self, arg):
        """
            Display the current player dataframe
        """
        print(self.data)

    def do_usedefaultframe(self, arg):
        """
            Use the pickled data frame obtained from the default player settings.
            Wikipedia scrape from 19.10.2021
        """
        self.do_showdefaults(arg)
        if arg == 'female':
            self.data = pandas.read_pickle('females.pkl')
        elif arg == 'male':
            self.data = pandas.read_pickle('males.pkl')

    def do_max(self, arg):
        """
            Print maximum for
             - career record
             - TODO: wins at grand slams
        """
        if arg == 'career record':
            maximum, id_max = analysis.max(self.data['career_record'])
            print('maximum career record: {}% obtained by {}'.format(maximum, self.data['Name'][id_max]))

        elif arg in 'Wimbledon':
            print('maximum number of wins at Wimbledon:')
        else:
            print("Not a valid input.  Please input either career record or the name of a tournament")

    def do_plot(self, arg):
        if arg == 'career record, highest rankings':
            analysis.plot_dataframe(self.data, 'career_record', 'highest_rankings')
        if arg == 'gradient descent':
            analysis.gradient_descent(self.data)

    # --------- basic commands ----------
    def do_exit(self, arg):
        """Exit the shell"""
        print('Thank you for using tennis-stats')
        raise SystemExit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TennisPlayersShell().cmdloop()

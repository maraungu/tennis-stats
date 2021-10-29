import cmd
import readline
import rlcompleter

import pandas as pd
import analysis
import framemethods

from player import *
from scrape import make_dataframe
from tournaments import *


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
    prompt = '(tennis_stats)'
    file = None

    players = Players()
    nationality_list = [nat.name for nat in Nationality]
    gender_list = [g.name for g in Gender]
    tour_list = [t.name for t in Tour]
    data = pd.DataFrame()

    # -------- INITIAL PLAYER SETTINGS -------------
    # To be used prior to scraping
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
        """Autocompleter for playergender command"""
        if not text:
            completions = self.gender_list
        else:
            completions = [g for g in self.gender_list if g.startswith(text)]
        return completions

    def do_birthyear(self, arg):
        """Choose earliest birth year of players: BIRTHYEAR 1958"""
        if '2010' > arg > '1920':
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
        """Adds autocomplete for supported nationalities"""
        if not text:
            completions = self.nationality_list
        else:
            completions = [nat for nat in self.nationality_list if nat.startswith(text)]
        return completions

    # -------- OBTAIN DATAFRAME ----------------
    def do_generatedataframe(self, arg):
        """
            Generate data frame based on the player settings.
            To check which settings apply, use command showsettings
        """
        if self.players.birthyear >= '1950':
            self.data = make_dataframe(self.players.link, self.players.gender, self.players.nationality,
                                       self.players.birthyear)
            # If you want to pickle the generated dataframe:
            # self.data.to_pickle('pickled-dataframes/gender-new.pkl')

    def do_usedefaultframe(self, arg):
        """
            Use the pickled data frame obtained from the default player settings.
            Wikipedia scrape from 22.10.2021
        """
        self.do_showdefaults(arg)
        if arg == 'female':
            self.data = pd.read_pickle('pickled-dataframes/females-final.pkl')
        elif arg == 'male':
            self.data = pd.read_pickle('pickled-dataframes/males-final.pkl')

    def do_displaydataframe(self, arg):
        """
            Display the current player dataframe
        """
        print(self.data)

    # ----------- WRAPPED DATAFRAME METHODS ---------
    # To be used once scraping is complete to manipulate
    # the dataframe
    def do_filterranking(self, arg):
        """Filters out players with highest ranking > arg.
        Example: FILTERRANKING 150 outputs players with highest ranking at most 150"""
        self.data = framemethods.highest_ranking(self.data, arg)

    def do_filterrecord(self, arg):
        """Filters out players with career record < arg.
        Example: FILTERRECORD 60 outputs players with career record of
        at least 60%"""
        self.data = framemethods.career_record(self.data, arg)

    def do_filterbirthyear(self, arg):
        """Filters out players with birthyears < arg.
        Example: FILTERBIRTHYEAR 1980 outputs players with year
        of birth earlier than 1980
        """
        if '2010' > arg > '1920':
            self.data = framemethods.birthyear(self.data, arg)
        else:
            print('Not a valid earliest birthyear')

    def do_filternationality(self, arg):
        """Keeps players of specified nationality only.
        Example: FILTERNATIONALITY France keeps only players
        with nationality France"""

        if arg and arg in self.nationality_list:
            self.data = framemethods.nationality(self.data, arg)
        else:
            print('Not a valid nationality')

    def complete_filternationality(self, text, line, begidx, endidx):
        """Autocompleter for supported nationalities"""
        if not text:
            completions = self.nationality_list
        else:
            completions = [nat for nat in self.nationality_list if nat.startswith(text)]
        return completions

    def do_selectplayer(self, arg):
        """Prints to terminal the information contained in the database
        about player whose name contains arg"""
        framemethods.select_player(self.data, arg)

    def do_max(self, arg):
        """
            Print maximum for
             - career record
             - TODO: potentially wins at different tours - need to upgrade the scraping
        """
        if arg == 'career record':
            maximum, id_max = framemethods.maximum(self.data['career_record'])
            print('maximum career record: {}% obtained by {}'.format(maximum, self.data['Name'][id_max]))
        # TODO: potentially do this as well
        elif arg in 'Wimbledon':
            print('maximum number of wins at Wimbledon:')
        else:
            print("Not a valid input.  Please input either career record or the name of a tournament")

    # ------- DATA ANALYSIS COMMANDS -----

    def do_plot(self, arg):
        """
        Yields different plots for the dataframe.
        Parameters are numerical columns of player dataframe.

        Intended format: PLOT x-axis y-axis (optional: fitcurve).

        Example: PLOT career_record highest_rankings fitcurve

        FIXME: Only implemented gradient descent for x-axis = career_record and y-axis = highest ranking

        Horizontal bar plot for each supported nationality
        and supported tours.

        For supported nationalities, see Nationality enum.  For supported tours, see Tour enum

        Example: NATIONALRESULTS Wimbledon outputs the
        number of wins, finals, semis, etc. reached by players with
        the supported nationality
        """
        arg_list = arg.rsplit()
        # print(arg_list, len(arg_list))
        column_list = self.data.columns.tolist()
        # print(column_list)
        if len(arg_list) == 1 and arg_list[0] == 'tourresults':
            analysis.plot_tour_results(self.data)
        elif len(arg_list) == 2 and set(arg_list) <= set(column_list):
            analysis.plot_dataframe(self.data, arg_list[0], arg_list[1])
        elif len(arg_list) == 2 and arg_list[0] == 'nationalresults':
            analysis.plot_tour_results_nationality(self.data, arg_list[1])
        elif len(arg_list) == 3 and arg_list[2] == 'fitcurve' and set(arg_list[:2]) <= set(column_list):
            analysis.gradient_descent(self.data)

    def complete_plot(self, text, line, begidx, endidx):
        """Autocomplete for plot command"""
        column_list = self.data.columns.tolist()
        if not text:
            completions = column_list[4:]
            completions.extend(['nationalresults', 'tourresults'])
        else:
            completions = [col for col in column_list[3:] if col.startswith(text)]

        return completions

    # --------- BASIC COMMANDS ----------
    def do_exit(self, arg):
        """Exit the shell"""
        print('Thank you for using tennis_stats')
        raise SystemExit()


if __name__ == '__main__':
    TennisPlayersShell().cmdloop()

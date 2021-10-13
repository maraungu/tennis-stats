import scrape
from scrape import make_soup
import argparse


class Players(object):
    def __init__(self, gender='', birthyear='1950', link='', alive=True, nationality=''):
        self.gender = gender
        self.birthyear = birthyear
        self.link = link
        self.alive = alive
        self.nationality = nationality

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
    parser = argparse.ArgumentParser()
    parser.add_argument("gender", help="pick player gender: male or female")
    #parser.add_argument("birthyear", help="earliest birth year. default is 1950")
    #parser.add_argument("alive", help="alive or dead. default doesn't care")
    #parser.add_argument("nationality", help="default doesn't care")
    args = parser.parse_args()
    link = ''
    if args.gender == 'male':
        link = 'https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players'
        print('male')
    else:
        if args.gender == 'female':
            link = 'https://en.wikipedia.org/wiki/List_of_female_tennis_players'
            print('female')

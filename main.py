import scrape
from scrape import make_soup
import click


class Players(object):
    def __init__(self, gender='', birthyear='1950', link='', alive=True, nationality=''):
        self.gender = gender
        self.birthyear = birthyear
        self.link = link
        self.alive = alive
        self.nationality = nationality


@click.group(chain=True)
@click.option('--gender', default='')
@click.option('--link', default='')
@click.option('--birthyear', default='1950')
@click.option('--alive/--dead', default=True)
@click.option('--nationality', default='')
@click.pass_context
def cli(ctx, gender, link, birthyear, alive, nationality):
    ctx.obj = Players(gender, link, birthyear, alive, nationality)


@cli.command()
@click.option('--gender', prompt='Male or female?')
@click.pass_obj
def male_or_female(players, gender):
    if gender == 'male' or gender == 'Male':
        players.link = 'https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players'
        players.gender = gender
        print('yay male')
    else:
        if gender == 'female' or gender == 'Female':
            players.link = 'https://en.wikipedia.org/wiki/List_of_female_tennis_players'
            players.gender = gender
            print('yay female')
        else:
            print('Cannot read answer')


@cli.command()
@click.option('--birthyear', prompt='Earliest birth year:', help='Only consider tennis players born after that year')
@click.pass_obj
def year_of_birth(players, birthyear):
    if birthyear >= '1950':
        make_soup(players.link)


# Make another group?
# @click.group(chain=True)
# @click.pass_context
# def database_stuff(ctx):
#     pass
#
#
# @database_stuff.command()
# @click.pass_obj
# def steps(players):
#     print("What next?")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(scrape.ok_to_scrape())
    cli()
    #database_stuff()
    print("bla")

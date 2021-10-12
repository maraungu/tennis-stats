import scrape
import click


@click.command()
@click.option('--gender', prompt='Male of female?', help='Male of female tennis players')
def players(gender):
    if gender == 'male' or gender == 'Male':
        link = 'https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players'
        print('yay male')
    else:
        if gender == 'female' or gender == 'Female':
            link = 'https://en.wikipedia.org/wiki/List_of_female_tennis_players'
            print('yay female')
        else:
            print('Cannot read answer')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(scrape.ok_to_scrape())
    players()

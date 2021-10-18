import wikipedia
import requests
import pandas
from pandas import DataFrame
from bs4 import BeautifulSoup


def get_html(link):
    # html = requests.get('https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players')
    return requests.get(link)


def ok_to_scrape(link):
    html = get_html(link)
    if html.status_code == 200:
        return True
    else:
        return False


def make_player_table(link):
    html = get_html(link)
    if ok_to_scrape(link):
        soup = BeautifulSoup(html.text, 'html.parser')
        player_table = soup.find('table', {'class': "sortable wikitable"})
        return player_table
    else:
        print("Not OK to scrape")
        raise ConnectionRefusedError


def get_wikilinks(player_table):
    links = []
    for i in player_table.find_all(name='tr'):
        links.append(i.find('a', href=True))

    new_links = []
    for i in range(1, len(links)):
        new_links.append(links[i]['href'])

    new_links = ['https://en.wikipedia.org' + i for i in new_links]

    return new_links


def make_dataframe(link, gender, nat):
    player_table = make_player_table(link)
    wikilinks = get_wikilinks(player_table)

    df = pandas.read_html(str(player_table))
    df = pandas.DataFrame(df[0])

    if gender == 'male' and nat == 'any':
        data = df.drop(["Nationality", "Death", "HoF", "Rank[a]", "Highest inclusion criteria"], axis=1)
    elif gender == 'female' and nat == 'any':
        data = df.drop(["Nationality", "Death", "Grand Slam singles titles", "Notes"], axis=1)
    else:
        print('Not a valid gender')
        raise AttributeError

    data['wikilink'] = wikilinks

    # ------ remove players with missing data ---------
    data = clean_dataframe(data, gender)


def clean_dataframe(data, gender):
    if gender == 'female':
        clean_data = data[~data.wikilink.str.contains("index.php?")]
    elif gender == 'male':
        clean_data = data[data.Birth != '?']
    else:
        print('Not a valid gender')
        raise AttributeError

    return clean_data
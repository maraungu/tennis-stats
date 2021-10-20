import re
import requests
import pandas
from bs4 import BeautifulSoup


def get_html(link):
    """Requests wikipedia link"""
    return requests.get(link)


def ok_to_scrape(link):
    """Checks status code.  Returns True if result is 200, False otherwise"""
    html = get_html(link)
    if html.status_code == 200:
        return True
    else:
        return False


def make_player_table(link):
    """If status code of link is 200, then generate soup from the player table"""
    html = get_html(link)
    if ok_to_scrape(link):
        soup = BeautifulSoup(html.text, 'html.parser')
        player_table = soup.find('table', {'class': "sortable wikitable"})
        return player_table
    else:
        print("Not OK to scrape")
        raise ConnectionRefusedError


def get_wikilinks(player_table):
    """Returns list of wikilinks for each player in the player table"""
    links = []
    for i in player_table.find_all(name='tr'):
        links.append(i.find('a', href=True))

    new_links = []
    for i in range(1, len(links)):
        new_links.append(links[i]['href'])

    new_links = ['https://en.wikipedia.org' + i for i in new_links]

    return new_links


def birthyear_filter(data, birthyear):
    filtered_data = data.drop(data[data.Birth < int(birthyear)].index)
    return filtered_data


def make_dataframe(link, gender, nat, birthyear):
    """ Constructs player dataframe.  Looks like this:

        Name | Birth | wikilink | career record | highest ranking

        career record = percentage of wins out of total number of games played
    """

    player_table = make_player_table(link)

    df = pandas.read_html(str(player_table))
    df = pandas.DataFrame(df[0])

    wikilinks = get_wikilinks(player_table)
    df['wikilink'] = wikilinks

    # ------ clean data frame ---------
    data = clean_dataframe(df, gender, nat)

    # ------ birth years filter --------
    data = data.drop(data[data.Birth < int(birthyear)].index)

    # TODO: introduce a nationality filter as well

    # ----- add new columns to be filled with career record and highest rankings ----
    data = data.assign(career_record="", highest_rankings="")

    career_record, highest_rankings = get_record_and_ranking(data)

    data['career_record'] = career_record
    data['highest_rankings'] = highest_rankings

    # get rid of zeros and very low rankings
    data = data[data.career_record != 0.0]
    data = data[data.highest_rankings != 0]
    data = data[data.highest_rankings <= 150]

    return data


def process_player_cards(data):
    """ Process player cards soup to get career prerecords and prerankings.
        The prefix "pre" is used because the data at this point looks like this:
            523–130 (80.1%) or 309–242
        for records and
            No. 8 (February 9, 2004)
        for highest rankings.
    """

    player_cards = get_player_cards(data)

    pre_records = []
    pre_rankings = []

    for index, player_card in enumerate(player_cards):
        record_flag = 0
        ranking_flag = 0

        if player_card is not None:
            for i in player_card.find_all('th', {'class': "infobox-label"}):
                if "record" in str(i.string):
                    # print("true")
                    # print("record", i.next_sibling.text)  # text is a str
                    pre_records.append(i.next_sibling.text)
                    record_flag += 1
                if "ranking" in str(i.string) and ranking_flag == 0:
                    # print("ranking", i.next_sibling.text)
                    pre_rankings.append(i.next_sibling.text)
                    ranking_flag += 1
                if i.parent.next_sibling is None:
                    break
                else:
                    if "Doubles" in str(i.parent.next_sibling.string) or "Other" in str(i.parent.next_sibling.string):
                        break
            if record_flag == 0:
                pre_records.append("not there")
            if ranking_flag == 0:
                pre_rankings.append("not there")
        else:
            pre_records.append("not there")
            pre_rankings.append("not there")

    return pre_records, pre_rankings


def get_record_and_ranking(data):
    """ Post-processing the output of the process_player_cards function.
        We want to keep (or compute) only the percentages for the records and the
        integer corresponding to the highest ranking for the rankings.
        For example:
            The entry: 523–130 (80.1%) -> 80.1%
            The entry: 309–242 -> 56.1%
            The entry: No. 8 (February 9, 2004) -> 8
        The output is a list of career records and a list of highest rankings
    """

    pre_records, pre_rankings = process_player_cards(data)

    highest_rankings = []
    for ranking in pre_rankings:
        if ranking != 'not there' and ranking != 'no value' and ranking != 'unknown value' and ranking != '':
            split_ranking = re.split('\W+', ranking)
            print(split_ranking)
            highest_rankings.append(int(split_ranking[1]))
        else:
            print(ranking)
            highest_rankings.append(0)

    career_record = []
    for record in pre_records:
        if record != 'not there' and record != 'no value' and record != 'unknown value' and record != '':
            split_record = re.split('\W+', record)  # fix this regular expression stuff to see the -
            # print(split_record)
            if len(split_record) == 6 and split_record[0] == '1':
                wins = int(split_record[0]) * 1000 + int(split_record[1])
                losses = int(split_record[2])
            else:
                wins = int(split_record[0])
                losses = int(split_record[1])
            total = wins + losses
            wins_percentage_of_total = round((wins / total) * 100, 1)
            # print(wins_percentage_of_total)
            career_record.append(wins_percentage_of_total)
        else:
            if record == '':
                career_record.append(0.0)
                # print('not there')
            else:
                # print(record)
                career_record.append(0.0)

    return career_record, highest_rankings


def get_player_cards(data):
    player_cards = []

    for index, row in data.iterrows():
        print(data.wikilink[index])
        html = requests.get(data.wikilink[index])
        soup = BeautifulSoup(html.text, 'html.parser')

        player_card = soup.find('table', {'class': "infobox vcard"})

        player_cards.append(player_card)

    return player_cards


def clean_dataframe(df, gender, nat):
    """Removes unnecessary columns from the global player table and
    player rows missing info/website"""

    if gender == 'male' and nat == 'any':
        data = df.drop(["Nationality", "Death", "HoF", "Rank[a]", "Highest inclusion criteria"], axis=1)
        clean_data = data[data.Birth != '?']
        clean_data = clean_data[clean_data.Birth != 'c.1921']
        clean_data['Birth'] = clean_data['Birth'].astype(int)
    elif gender == 'female' and nat == 'any':
        data = df.drop(["Nationality", "Death", "Grand Slam singles titles", "Notes"], axis=1)
        clean_data = data[~data.wikilink.str.contains("index.php?")]
        # gets rid of NaNs
        # TODO: should get the female players birth years as ints as well
        clean_data = clean_data.dropna()
        clean_data['Birth'] = clean_data['Birth'].astype(int)
    else:
        print('Not a valid gender')
        raise AttributeError

    return clean_data

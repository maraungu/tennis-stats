import wikipedia
import requests
import pandas
from bs4 import BeautifulSoup

def get_html():
    html = requests.get('https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players')
    return html

def ok_to_scrape():
    html = get_html()
    if html.status_code == 200:
        return True
    else:
        return False

def make_soup():
    soup = BeautifulSoup(html.text, 'html.parser')


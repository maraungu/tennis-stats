import wikipedia
import requests
import pandas
from bs4 import BeautifulSoup

def get_html(link):
    #html = requests.get('https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players')
    return requests.get(link)

def ok_to_scrape(html):
    if html.status_code == 200:
        return True
    else:
        return False

def make_soup(link):
    html = get_html(link)
    if ok_to_scrape(html):
        soup = BeautifulSoup(html.text, 'html.parser')


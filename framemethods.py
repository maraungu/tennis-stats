import pandas as pd


def birthyear(data, year):
    data.drop(self[self.Birth < int(year)].index)


def career_record(data, record):
    data.drop(data[data.career_record < record].index)


def highest_ranking(data, ranking):
    new_data = data.drop(data[data.highest_rankings > int(ranking)].index)
    return new_data

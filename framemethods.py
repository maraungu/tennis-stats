def birthyear(data, year):
    data.drop(data[data.Birth < int(year)].index)


def career_record(data, record):
    data.drop(data[data.career_record < float(record)].index)


def highest_ranking(data, ranking):
    new_data = data.drop(data[data.highest_rankings > int(ranking)].index)
    return new_data


def nationality(data, nat):
    if nat != 'any':
        if nat == 'Russia':
            # new_data = data.drop(data[data.Nationality != 'Russia'].index)
            new_data = data.loc[data.Nationality.str.contains('Russia')]
        elif nat == 'UK':
            new_data = data.drop(data[data.Nationality != 'Great Britain'].index)
        elif nat == 'US':
            new_data = data.drop(data[data.Nationality != 'United States'].index)
        else:
            new_data = data.drop(data[data.Nationality != nat].index)
        return new_data
    else:
        return data


def select_player(data, name):
    # print(name)
    if name != '':
        new_data = data.drop(['wikilink'], axis=1)
        idx = new_data.loc[new_data.Name.str.contains(name)]
        if not idx.empty:
            print(idx)
        else:
            print("The player {} does not appear in the database.".format(name))
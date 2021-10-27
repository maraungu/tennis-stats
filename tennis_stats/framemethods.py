# Collection of dataframe methods which are
# wrapped up as commands in the CLI


def maximum(column):
    """Yields maximum value in dataframe column and its index"""
    return column.max(), column.idxmax()


def birthyear(data, year):
    """
    Filters out birthyears lower than input
    :param data: dataframe
    :param year: str
    :return: dataframe filtered by birthyear
    """
    data.drop(data[data.Birth < int(year)].index)


def career_record(data, record):
    """
    Filters out career records lower than input
    :param data: dataframe
    :param record: str
    :return: dataframe filtered by career_record
    """
    data.drop(data[data.career_record < float(record)].index)


def highest_ranking(data, ranking):
    """
    Filters out highest_rankings higher than input
    :param data: dataframe
    :param ranking: str
    :return: dataframe filtered by highest_rankings
    """
    new_data = data.drop(data[data.highest_rankings > int(ranking)].index)
    return new_data


def nationality(data, nat):
    """
    Filter out players not of given nationality
    :param data: dataframe
    :param nat: str
    :return: dataframe filtered by nationality
    """
    if nat != 'any':
        if nat == 'Russia':
            # new_data = data.drop(data[data.Nationality != 'Russia'].index)
            new_data = data.loc[data.Nationality.str.contains('Russia')]
        elif nat == 'UK':
            new_data = data.drop(data[(data.Nationality != 'Great Britain') &
                                      (data.Nationality != 'United Kingdom')].index)
        elif nat == 'Germany':
            new_data = data.loc[data.Nationality.str.contains('Germany')]
        elif nat == 'US':
            new_data = data.drop(data[data.Nationality != 'United States'].index)
        else:
            new_data = data.drop(data[data.Nationality != nat].index)
        return new_data
    else:
        return data


def select_player(data, name):
    """
    Finds player entry containing name in Name column
    :param data: data
    :param name: str
    :return: dataframe filtered by name
    """
    if name != '':
        new_data = data.drop(['wikilink'], axis=1)
        idx = new_data.loc[new_data.Name.str.contains(name)]
        if not idx.empty:
            print(idx)
            return idx
        else:
            print("The player {} does not appear in the database.".format(name))
            return idx

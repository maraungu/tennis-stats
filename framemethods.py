def birthyear(data, year):
    data.drop(data[data.Birth < int(year)].index)


def career_record(data, record):
    data.drop(data[data.career_record < float(record)].index)


def highest_ranking(data, ranking):
    new_data = data.drop(data[data.highest_rankings > int(ranking)].index)
    return new_data


def nationality(data, nat):
    # TODO: deal with Russia
    if nat != 'any':
        new_data = data.drop(data[data.Nationality != nat].index)
        return new_data
    else:
        return data

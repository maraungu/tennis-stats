import unittest
import pandas as pd

from tennis_stats import framemethods


# To run: in root folder (tennis) python -m unittest tests.birth_record_test
# Test results based on dataframe pickled from wikipedia scrape on 22.10.2021
class TestBirthRecord(unittest.TestCase):
    data_female = pd.read_pickle('tennis_stats/pickled-dataframes/females-final.pkl')
    data_male = pd.read_pickle('tennis_stats/pickled-dataframes/males-final.pkl')

    def test_birth_record(self):
        filtered_data = framemethods.birthyear(self.data_female, '1980')
        filtered_data = framemethods.career_record(filtered_data, '81')
        self.assertEqual(filtered_data['Name'].to_string(index=False).replace(' ', ''), 'JustineHenin\nSerenaWilliams')

        filtered_data = framemethods.birthyear(self.data_male, '1980')
        filtered_data = framemethods.career_record(filtered_data, '83')
        self.assertEqual(filtered_data['Name'].to_string(index=False).replace(' ', ''), 'NovakDjokovic\nRafaelNadal')

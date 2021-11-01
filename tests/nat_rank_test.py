import unittest
import pandas as pd

from tennis_stats import framemethods


# To run: in root folder (tennis) python -m unittest tests.nat_rank_test
# Test results based on dataframe pickled from wikipedia scrape on 22.10.2021
class TestNatRanking(unittest.TestCase):
    data_female = pd.read_pickle('tennis_stats/pickled-dataframes/females-final.pkl')
    data_male = pd.read_pickle('tennis_stats/pickled-dataframes/males-final.pkl')

    def test_nat_ranking(self):
        filtered_data = framemethods.nationality(self.data_female, 'Germany')
        filtered_data = framemethods.highest_ranking(filtered_data, '1')
        self.assertEqual(filtered_data['Name'].to_string(index=False).replace(' ', ''), 'SteffiGraf\nAngeliqueKerber')

        filtered_data = framemethods.nationality(self.data_male, 'Russia')
        filtered_data = framemethods.highest_ranking(filtered_data, '1')
        self.assertEqual(filtered_data['Name'].to_string(index=False).replace(' ', ''), 'YevgenyKafelnikov\nMaratSafin')


if __name__ == '__main__':
    unittest.main()

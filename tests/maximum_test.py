import unittest
import pandas as pd

from tennis_stats import framemethods


# To run: in root folder (tennis) python -m unittest tests.maximum_test
# Test results based on dataframe pickled from wikipedia scrape on 22.10.2021
class TestMaxRecord(unittest.TestCase):
    data_female = pd.read_pickle('tennis_stats/pickled-dataframes/females-final.pkl')
    data_male = pd.read_pickle('tennis_stats/pickled-dataframes/males-final.pkl')

    def test_max_career_record(self):
        maximum, id_max = framemethods.maximum(self.data_female['career_record'])
        self.assertEqual(self.data_female['Name'][id_max], 'Chris Evert')

        maximum, id_max = framemethods.maximum(self.data_male['career_record'])
        self.assertEqual(self.data_male['Name'][id_max], 'Novak Djokovic')


if __name__ == '__main__':
    unittest.main()

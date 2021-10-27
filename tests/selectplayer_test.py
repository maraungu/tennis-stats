import unittest
import pandas as pd

from tennis_stats import framemethods

# To run: in root folder (tennis) python -m unittest tests.selectplayer_test
# Test results based on dataframe pickled from wikipedia scrape on 22.10.2021
class TestSelectPlayer(unittest.TestCase):
    data_female = pd.read_pickle('tennis_stats/pickled-dataframes/females-final.pkl')
    data_male = pd.read_pickle('tennis_stats/pickled-dataframes/males-final.pkl')

    def test_halep(self):
        """Test that it finds Simona Halep's record"""
        filtered_data = framemethods.select_player(self.data_female, 'Halep')
        self.assertEqual(filtered_data['highest_rankings'].to_string(index=False), '1')
        self.assertEqual(filtered_data['French'].to_string(index=False), 'W')
        self.assertEqual(filtered_data['Wimbledon'].to_string(index=False), 'W')
        self.assertEqual(filtered_data['Nationality'].to_string(index=False), 'Romania')

    def test_williams(self):
        """Test that it finds the Williams sisters"""
        filtered_data = framemethods.select_player(self.data_female, 'Williams')
        self.assertEqual(filtered_data['highest_rankings'].to_string(index=False), '1\n1')
        self.assertEqual(filtered_data['French'].to_string(index=False), 'W\nF')
        self.assertEqual(filtered_data['Wimbledon'].to_string(index=False), 'W\nW')
        self.assertEqual(filtered_data['Nationality'].to_string(index=False), 'United States\nUnited States')

    def test_zverevz(self):
        """Tests that it finds the Zverev brothers"""
        filtered_data = framemethods.select_player(self.data_male, 'Zverev')
        self.assertEqual(filtered_data['highest_rankings'].to_string(index=False), ' 3\n25')
        self.assertEqual(filtered_data['French'].to_string(index=False), 'SF\n3R')
        self.assertEqual(filtered_data['Wimbledon'].to_string(index=False), '4R\n3R')
        self.assertEqual(filtered_data['Nationality'].to_string(index=False), 'Germany\nGermany')


if __name__ == '__main__':
    unittest.main()

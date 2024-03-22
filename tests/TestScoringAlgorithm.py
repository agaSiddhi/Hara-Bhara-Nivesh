import unittest
from unittest import mock
from unittest.mock import patch, mock_open
import pandas as pd
import yaml
from scoring_algorithm.scoring_algo import assign_weights, update_final_esg_score, update_historical_esg_score, push_data_to_csv, update_yaml_file, scoring

class TestFunctions(unittest.TestCase):

    def assertDataFramesEqual(self, df1, df2):
        """
        Custom assertion to check if two DataFrames are equal.
        """
        # Check if indices are equal
        self.assertTrue(df1.index.equals(df2.index))

        # Check if columns are equal
        self.assertCountEqual(df1.columns, df2.columns)

        # Check if values are equal
        pd.testing.assert_frame_equal(df1, df2)
    
    def test_assign_weights(self):
        self.assertEqual(assign_weights(-1), 0)
        self.assertEqual(assign_weights(0), 1)
        self.assertEqual(assign_weights(1), 1)

    def test_push_data_to_csv(self):
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6]
        })
        csv_file = 'test.csv'
        push_data_to_csv(df, csv_file)
        df_read = pd.read_csv(csv_file)
        self.assertTrue(df.equals(df_read))

    def test_update_yaml_file(self):
        data = {'A': [1,3], 'B': [2,5], 'C': [6,3]}
        yaml_file = 'test.yaml'
        update_yaml_file(data, yaml_file)
        with open(yaml_file, 'r') as file:
            data_read = yaml.safe_load(file)
        self.assertDictEqual(data, data_read)

    def test_scoring_algorithm(self):
        # Mock data for articles and esg_ratings
        articles_data = {
            'Heading': ['Article 1', 'Article 2', 'Article 3'],
            'Text': ['Text 1', 'Text 2', 'Text 3'],
            'Datetime': ['2024-03-22', '2024-03-22', '2024-03-22'],
            'Company': ['A', 'A', 'B'],
            'Category': ['Environment', 'Social', 'Governance'],
            'Score': [0.5, 0.6, 0.7],
            'Score_blob': [0.4, 0.7, 0.8]
        }
        esg_ratings_data = {
            'Company': ['A', 'B'],
            'Score': [50, 60]
        }

        articles_data = pd.DataFrame(articles_data)
        articles_data.to_csv('test_articles.csv')
        esg_ratings_data = pd.DataFrame(esg_ratings_data)
        esg_ratings_data.to_csv('test_esg_ratings.csv')
        # Call the function
        df = scoring(articles_file='test_articles.csv', esg_ratings_file='test_esg_ratings.csv')
        data = {'Company Name': ['A', 'B'],
                 'Date': ['2024-03-22', '2024-03-22'],
                 'Environment': [35.25, -1],
                 'Social': [42.8, -1],
                 'Governance': [-1, 45.35],
                 'ESG_ratings': [50, 60],
                 'Final_ESG_Score':[-1,-1],
                 'Historical_esg_score':[-1,-1]}
        data = pd.DataFrame(data)
        self.assertDataFramesEqual(df, data)
        
    
    def test_update_final_esg_score(self):
        df = pd.DataFrame({
            'Environment': [1, 0, -1],
            'Social': [1, -1, 0],
            'Governance': [-1, 1, 0],
            'ESG_ratings': [0, 1, 1]
        })
        expected_final_esg_score = [0.6666666666666666, 0.6666666666666666, 0.3333333333333333]
        df = update_final_esg_score(df)
        self.assertListEqual(list(df['Final_ESG_Score']), expected_final_esg_score)

    def test_update_historical_esg_score(self):
        df = pd.DataFrame({
            'Company Name': ['A', 'A', 'B', 'B'],
            'Final_ESG_Score': [0.5, 0.75, 0.6, 0.8]
        })
        last_occurrence = {}
        expected_historical_esg_scores = pd.DataFrame({'Company Name':['A', 'A', 'B', 'B'],'Final_ESG_Score':[0.5, 0.75, 0.6, 0.8],'Historical_esg_score': [0.5, 0.625, 0.6, 0.7]})
        data, _ = update_historical_esg_score(df, last_occurrence)
        self.assertDataFramesEqual(data, expected_historical_esg_scores)

if __name__ == '__main__':
    unittest.main()

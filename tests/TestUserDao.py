import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from backend.dao.user_dao import UserDao
import pandas as pd

class TestUserDao(unittest.TestCase):

    def setUp(self):
       self.user_dao = UserDao(host='localhost', user='root',password='mysql_12#$',database='Securities')
       self.user_dao.execute_query = MagicMock()

    def test_add_user_details(self):
        username = 'test_user'
        name = 'Test User'
        password = 'test_password'
        age = 30
        country = 'Test Country'
        gender = 'Male'
        
        self.user_dao.add_user_details(username, name, password, age, country, gender)
        
        expected_query = f'INSERT INTO User (username, name, password, balance, age, country, gender) VALUES ("{username}", "{name}", "{password}", 10000, "{age}", "{country}", "{gender}");'
        self.user_dao.execute_query.assert_called_once_with(expected_query)

    def test_add_user_email(self):
        username = 'test_user'
        email = 'test@example.com'

        self.user_dao.add_user_email(username, email)

        expected_query = f'INSERT INTO User_mail (username, email) VALUES ("{username}", "{email}");'
        self.user_dao.execute_query.assert_called_once_with(expected_query)

    def test_get_user_data(self):
        user_data_mock = [('test_user', 'Test User', 'test_password', 10000, 30, 'Test Country', 'Male')]
        user_mail_data_mock = [('test_user', 'test@example.com')]
        
        self.user_dao.execute_query.side_effect = [user_data_mock, user_mail_data_mock]
        
        user_data, user_mail_data = self.user_dao.get_user_data()

        expected_user_data = [('test_user', 'Test User', 'test_password', 10000, 30, 'Test Country', 'Male')]
        expected_user_mail_data = [('test_user', 'test@example.com')]

        self.assertEqual(user_data, expected_user_data)
        self.assertEqual(user_mail_data, expected_user_mail_data)

    def test_get_user_name_ticker_from_portfolio(self):
       
        query_result_mock = [('user1', 'AAPL'), ('user2', 'MSFT')]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_user_name_ticker_from_portfolio()
        
        expected_result = [('user1', 'AAPL'), ('user2', 'MSFT')]
       
        self.assertEqual(result, expected_result)

    def test_add_uploaded_file_to_current_portfolio(self):
       
        self.user_dao.execute_query = MagicMock()
        
        uploaded_file_mock = pd.DataFrame({
            'Date': [datetime.now(), datetime.now()],
            'Order Type': ['Buy', 'Sell'],
            'Ticker': ['AAPL', 'MSFT'],
            'Amount': [10, 20],
            'Price/Quote': [150.0, 200.0]
        })
        
        self.user_dao.add_uploaded_file_to_current_portfolio(uploaded_file_mock)
        
        self.assertEqual(self.user_dao.execute_query.call_count, 2)

    def test_get_wallet_balance(self):
       
        query_result_mock = [(10000.0,)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_wallet_balance('test_user')
        
        expected_result = 10000.0
        
        self.assertEqual(result, expected_result)

    def test_update_transaction_history(self):

        self.user_dao.update_transaction_history('AAPL', 10, 150.0, 'Buy')
        
        self.assertTrue(self.user_dao.execute_query.called)

    def test_update_portfolio(self):

        self.user_dao.update_portfolio('AAPL', 10, 150.0, 'Buy')
        
        self.assertTrue(self.user_dao.execute_query.called)

    def test_get_current_price_for_ticker(self):
      
        query_result_mock = [(150.0,)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_current_price_for_ticker('AAPL')

        expected_result = 150.0
        
        self.assertEqual(result, expected_result)

    def test_update_wallet(self):
      
        self.user_dao.update_wallet(10000.0)
        
        self.assertTrue(self.user_dao.execute_query.called)

    def test_get_usernames(self):
       
        query_result_mock = [('user1',), ('user2',)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_usernames()
        
        expected_result = ['user1', 'user2']
        
        self.assertEqual(result, expected_result)

    def test_get_mail(self):
        
        query_result_mock = [('test@example.com',)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_mail('test_user')
        
        expected_result = 'test@example.com'
        
        self.assertEqual(result, expected_result)

    def test_get_portfolio_entry_for_user(self):
       
        query_result_mock = [(10, datetime.now(), 'Buy', 150.0, 'AAPL')]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_portfolio_entry_for_user('test_user')
    
        expected_result = pd.DataFrame(query_result_mock, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"]).sort_values(by='Date')
        
        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_name_from_username(self):

        query_result_mock = [('Test User',)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_name_from_username('test_user')
        
        expected_result = 'Test User'
        
        self.assertEqual(result, expected_result)

    def test_get_transaction_history(self):
        
        query_result_mock = [(10, datetime.now(), 'Buy', 150.0, 'AAPL')]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_transaction_history('test_user')
        
        expected_result = pd.DataFrame(query_result_mock, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"]).sort_values(by='Date')
        
        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_age_from_username(self):

        query_result_mock = [(30,)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_age_from_username('test_user')
        
        expected_result = 30
    
        self.assertEqual(result, expected_result)

    def test_get_gender_from_username(self):
        
        query_result_mock = [('Male',)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_gender_from_username('test_user')
        
        expected_result = 'Male'
        
        self.assertEqual(result, expected_result)

    def test_get_country_from_username(self):
    
        query_result_mock = [('Test Country',)]
        self.user_dao.execute_query.return_value = query_result_mock
        
        result = self.user_dao.get_country_from_username('test_user')
        
        expected_result = 'Test Country'
        
        self.assertEqual(result, expected_result)

    def test_get_time_frequency_of_user(self):
    
        query_result_mock = [(datetime.now(), 5)]
        self.user_dao.execute_query.return_value = query_result_mock
  
        result = self.user_dao.get_time_frequency_of_user()
        
        expected_result = pd.DataFrame(query_result_mock, columns=['date', 'num_transactions'])
        
        pd.testing.assert_frame_equal(result, expected_result)

    def test_get_date_amount_for_avg_insights(self):

        query_result_mock = [(datetime.now(), 10)]
        self.user_dao.execute_query.return_value = query_result_mock

        result = self.user_dao.get_date_amount_for_avg_insights()

        expected_result = pd.DataFrame(query_result_mock, columns=['date', 'amount'])
        
        pd.testing.assert_frame_equal(result, expected_result)

        
    def tearDown(self):
        self.user_dao.connection.close()

if __name__ == '__main__':
    unittest.main()

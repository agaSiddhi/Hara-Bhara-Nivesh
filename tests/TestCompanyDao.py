import unittest
from unittest.mock import MagicMock
from backend.dao.dao import CompanyDao

class TestCompanyDao(unittest.TestCase):

    def setUp(self):
        # Creating a mock connection
        self.company_dao = CompanyDao(host='localhost', user='root', password='mysql_12#$', database='Securities')
        self.company_dao.execute_query = MagicMock()

    def test_get_company_name_and_description(self):
        # Define sample data
        sample_data = [('Company A', 0.8, 'Description A'),
                       ('Company B', 0.7, 'Description B')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_data

        # Call the method under test
        result = self.company_dao.get_company_name_and_description()

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_data)

    def test_get_companyID_from_company_name(self):
        # Define sample data
        company_name = 'Company A'
        sample_result = [('12345',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_companyID_from_company_name(company_name)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_ESG_score_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [(0.7, 0.6, 0.8)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_ESG_score_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_company_details_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [('ABC123', 'Company A', '2024-03-22', '2024-03-23', 1000000, 500000, 100, 0.75, 2000, 'http://companya.com')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_company_details_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_industry_description_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [('Some industry description')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_industry_description_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_price_history_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [(100.0, '2024-03-22'), (105.0, '2024-03-23')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_price_history_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_current_price_for_ticker(self):
        # Define sample data
        company_id = 'AAPL'
        sample_result = [(150.0,)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_current_price_for_ticker(company_id)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result[0][0])

    def test_get_score_history_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [(0.7, '2024-03-22'), (0.8, '2024-03-23')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_score_history_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_fund_category_from_ticker(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [('Equity',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_fund_category_from_ticker(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_industry(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [('Some industry description',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_industry(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result[0][0])

    def test_get_score_history_of_all_companies(self):
        # Define sample data
        sample_result = [('ABC123', 0.7, '2024-03-22'), ('DEF456', 0.8, '2024-03-23')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_score_history_of_all_companies()

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_price_history_of_all_companies(self):
        # Define sample data
        sample_result = [('ABC123', 100.0, '2024-03-22'), ('DEF456', 105.0, '2024-03-23')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_price_history_of_all_companies()

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_companies_for_fund_category(self):
        # Define sample data
        sample_result = {
            'Equity': ['ABC', 'DEF'],
            'Debt': ['GHI'],
            'Hybrid': ['JKL', 'MNO'],
            'Others': ['PQR']
        }

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.side_effect = [
            [('ABC',), ('DEF',)],
            [('GHI',)],
            [('JKL',), ('MNO',)],
            [('PQR',)]
        ]

        # Call the method under test
        result = self.company_dao.get_companies_for_fund_category()

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_companies_for_industry_category(self):
        # Define sample data
        sample_result = {
            'Capital Goods': ['ABC', 'DEF'],
            'HealthCare': ['GHI'],
            'Financial': ['JKL', 'MNO'],
            'Services': ['PQR'],
            'Other': ['STU'],
            'Consumer Staples': ['VWX']
        }

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.side_effect = [
            [('ABC',), ('DEF',)],
            [('GHI',)],
            [('JKL',), ('MNO',)],
            [('PQR',)],
            [('STU',)],
            [('VWX',)]
        ]

        # Call the method under test
        result = self.company_dao.get_companies_for_industry_category()

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_company_name_from_ticker(self):
        # Define sample data
        sample_result = [('ABC', 'Company ABC'), ('DEF', 'Company DEF')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_company_name_from_ticker()

        # Assert that the result matches the expected data
        self.assertEqual(result, {'ABC': 'Company ABC', 'DEF': 'Company DEF'})

    def test_get_average_score_from_ticker(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [(0.75,)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_average_score_from_ticker(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result[0][0])


    def test_get_company_details_for_credits(self):
        # Define sample data
        sample_result = [
            ('ABC123', 'Company ABC', 1000000, 500, 1000000, 0, 'Equity', 'Capital Goods', 1990),
            ('DEF456', 'Company DEF', 2000000, 1000, 2000000, 0, 'Debt', 'HealthCare', 2000)
        ]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_company_details_for_credits()

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_update_wallet_balance(self):
        # Define sample data
        ticker = 'ABC'
        updated_wallet_balance = 500

        # Call the method under test
        self.company_dao.update_wallet_balance(ticker, updated_wallet_balance)

        # Assert that the execute_query method was called with the correct query
        self.company_dao.execute_query.assert_called_once_with(
            f'UPDATE Company SET wallet = {updated_wallet_balance} WHERE companyID = "{ticker}";'
        )

    def test_get_industry_keyword_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [('Technology',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_industry_keyword_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_wallet_balance_from_companyID(self):
        # Define sample data
        companyID = 'ABC123'
        sample_result = [(1000,)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_wallet_balance_from_companyID(companyID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_add_new_company(self):
        # Define sample data
        ticker = 'ABC'
        name = 'Company ABC'
        total_assets = 1000000
        revenue = 500000
        employee_count = 100
        founded_year = 1990
        industry_id = 'Tech'
        fund_category = 'Equity'

        # Call the method under test
        self.company_dao.add_new_company(ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category)

        # Assert that the execute_query method was called with the correct query and parameters
        expected_query = """
            INSERT INTO Company (companyID, name, createdAt, updatedAt, totalAssets, revenue, employeeCount, currentScore, foundedYear, industryID, fundCategory, wallet)
            VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, 0.00 , %s, %s, %s, 0.00)
        """
        expected_params = (ticker.upper(), name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category)
        self.company_dao.execute_query.assert_called_once_with(expected_query, expected_params)

    def test_get_industry_id_by_keyword(self):
        # Define sample data
        industry_keyword = 'Technology'
        sample_result = [('Tech',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_industry_id_by_keyword(industry_keyword)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)


    def test_get_score_and_ticker_map(self):
        # Define sample data
        sample_result = [('ABC123', 80.0), ('DEF456', 75.0)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_score_and_ticker_map()

        # Assert that the result matches the expected data
        self.assertEqual(result, dict(sample_result))

    def test_add_company_signup_details(self):
        # Define sample data
        company_name = 'Company XYZ'
        company_ticker = 'XYZ'
        password = 'password123'
        initial_money_wallet_balance = 10000
        initial_credits_wallet_balance = 5000
        industryID = 'Tech'
        fund_category = 'Equity'

        # Call the method under test
        self.company_dao.add_company_signup_details(company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance, industryID, fund_category)

        # Assert that the execute_query method was called with the correct query and parameters
        expected_query = """
            INSERT INTO CompanySignup (CompanyName, CompanyTicker, Password, InitialMoneyWalletBalance, InitialCreditsWalletBalance, fundCategory, industryID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        expected_params = (company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance, fund_category, industryID)
        self.company_dao.execute_query.assert_called_once_with(expected_query, expected_params)
    
    def test_get_signup_company_data(self):
        # Define sample data
        name = 'XYZ'
        sample_result = [('XYZ', 'Company XYZ', 'password123', 10000, 5000, 'Tech', 'Equity')]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_signup_company_data(name)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_update_credit_wallet_balance(self):
        # Define sample data
        ticker = 'XYZ'
        credits = 200

        # Call the method under test
        self.company_dao.update_credit_wallet_balance(ticker, credits)

        # Assert that the execute_query method was called with the correct query
        expected_query = f'''UPDATE CompanySignup
                    SET InitialCreditsWalletBalance = InitialCreditsWalletBalance - {credits}
                    WHERE CompanyTicker = '{ticker}';'''
        self.company_dao.execute_query.assert_called_once_with(expected_query)

    def test_add_listed_credit_to_bid(self):
        # Define sample data
        initial_bid = 100
        min_step = 10
        credits = 200
        ticker = 'XYZ'

        # Call the method under test
        self.company_dao.add_listed_credit_to_bid(initial_bid, min_step, credits, ticker)

        # Assert that the execute_query method was called with the correct query
        expected_query = f'''INSERT INTO Bid (initial_Bid, minimum_Step, credits_Listed, companyID)
                VALUES ({initial_bid}, {min_step}, {credits}, '{ticker}');'''
        self.company_dao.execute_query.assert_called_once_with(expected_query)

    def test_get_max_bidding_amount(self):
        # Define sample data
        ticker = 'XYZ'
        sample_result = [(500,)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_max_bidding_amount(ticker)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_companyID_from_bidID(self):
        # Define sample data
        bidID = 123
        sample_result = [('XYZ',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_companyID_from_bidID(bidID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_max_bidding_amount(self):
        # Define sample data
        ticker = 'XYZ'
        sample_result = [(500,)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_max_bidding_amount(ticker)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_companyID_from_bidID(self):
        # Define sample data
        bidID = 123
        sample_result = [('XYZ',)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_companyID_from_bidID(bidID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_bidding_details_from_ticker(self):
        # Define sample data
        ticker = 'XYZ'
        sample_result = [('user1', 500, 123), ('user2', 600, 124)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_bidding_details_from_ticker(ticker)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

    def test_get_credits_listed_from_bidID(self):
        # Define sample data
        bidID = 123
        sample_result = [(1000,)]

        # Mock the execute_query method to return sample data
        self.company_dao.execute_query.return_value = sample_result

        # Call the method under test
        result = self.company_dao.get_credits_listed_from_bidID(bidID)

        # Assert that the result matches the expected data
        self.assertEqual(result, sample_result)

if __name__ == '__main__':
    unittest.main()

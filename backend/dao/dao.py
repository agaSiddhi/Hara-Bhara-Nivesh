import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from datetime import datetime as dt

class CompanyDao:
    '''This class definition, CompanyDao, is a data access object for a company database. 
    It establishes a connection to the database and provides methods for executing various 
    queries related to company data.'''

    def __init__(self, host, user, password, database,port):
        """
        Initializes a new instance of the class.

        Args:
            host (str): The host of the MySQL server.
            user (str): The username to connect to the MySQL server.
            password (str): The password to authenticate the user.
            database (str): The name of the database to connect to.
            port (int): The port number of the MySQL server.

        Returns:
            None
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port = port
        )
        
    def execute_query(self, query, params=None):
        """
        Executes a SQL query using the provided query and parameters and returns the result set.

        Parameters:
            query (str): The SQL query to be executed.
            params (dict, optional): The parameters to be used in the query. Default is None.

        Returns:
            list: A list containing the result set of the query.

        Raises:
            mysql.connector.Error: If an error occurs while executing the query.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params=params)
                return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error executing query: {query}. Error: {err}")
            raise
        finally:
            if not self.connection.autocommit:
                self.connection.commit()
                
    def get_company_name_and_description(self):
        """
        Retrieves the name, current score, and description of each company from the database.

        Returns:
            A list of tuples, where each tuple contains the name, current score, and description of a company.
            The list is sorted in descending order based on the current score.
        """
        query = "SELECT name,currentScore, (SELECT description FROM Industry WHERE Company.industryID = Industry.industryID)  FROM Company ORDER BY currentScore DESC;"
        results = self.execute_query(query)
        return results
    
    def get_companyID_from_company_name(self,company_name=None):
        """
        Retrieves the company ID associated with the given company name.

        Parameters:
            company_name (str): The name of the company. Defaults to None.

        Returns:
            list: A list containing the company ID as a single element.
        """
        query = 'SELECT companyID FROM Company WHERE name = %s;'
        params = (company_name,)
        result = self.execute_query(query,params)
        
        return result
    
    def get_ESG_score_from_companyID(self,companyID):
        """
        Retrieves the ESG score from the database for a given company ID.

        Parameters:
            companyID (str): The ID of the company for which the ESG score is to be retrieved.

        Returns:
            list: A list containing the environmental, social, and governance scores of the company.

        Raises:
            Exception: If there is an error executing the query or retrieving the result.
        """

        query = '''SELECT c.Environmental, c.Social , c.Governance
                FROM ESG c WHERE c.companyID = %s;'''
        params = (companyID,)
        try:
            result = self.execute_query(query,params)
            return result
        except Exception as e:
            print(e)
    
    def get_company_data(self):
        """
        Retrieves data from the CompanySignup table.
        """
        query = '''SELECT * FROM CompanySignup;'''
        company_data = self.execute_query(query)
        return company_data

    def get_company_details_from_companyID(self, companyID):
        """
        Retrieves the details of a company from the database based on the provided company ID.

        Parameters:
            companyID (int): The ID of the company.

        Returns:
            list: A list containing the details of the company. Each item in the list is a dictionary with the following keys:
                - companyID (int): The ID of the company.
                - companyName (str): The name of the company.
                - createdAt (datetime): The date and time when the company was created.
                - updatedAt (datetime): The date and time when the company was last updated.
                - totalAssets (float): The total assets of the company.
                - revenue (float): The revenue of the company.
                - employeeCount (int): The number of employees in the company.
                - currentScore (float): The current score of the company.
                - foundedYear (int): The year the company was founded.
                - url (str): The website URL of the company.

        Raises:
            Exception: If there is an error executing the query.
        """
        query = '''SELECT c.companyID, c.name AS companyName, c.createdAt, c.updatedAt, c.totalAssets, c.revenue, c.employeeCount, c.currentScore, c.foundedYear, w.url 
                FROM Company c 
                LEFT JOIN CompanyWebsite w ON c.companyID = w.companyID WHERE c.companyID = %s;'''
        params = (companyID,)
        try:
            result = self.execute_query(query,params)
        except Exception as e:
            print(e)
        return result
    
    def get_industry_description_from_companyID(self,companyID=None):
        """
        Retrieves the industry description associated with the given company ID.

        Parameters:
            companyID : The ID of the company.

        Returns:
            list: A list containing the industry description.
        """
        query = ''' SELECT i.description
                FROM Company c
                JOIN Industry i ON c.industryID = i.industryID
                WHERE c.companyID = %s; '''
        params = (companyID,)
        result = self.execute_query(query,params)
        return result
    
    def get_price_history_from_companyID(self, companyID=None):
        """
        Retrieves the price history and updatedAt information from the PriceHistory table for a given companyID.

        Parameters:
            companyID (str): The ID of the company for which the price history is requested.

        Returns:
            list: A list of tuples containing the price and updatedAt information for the company.
        """
        query = '''SELECT price, updatedAt
                FROM PriceHistory
                WHERE companyID = %s;'''
        params = (companyID,)
        result = self.execute_query(query,params)
        return result

    def get_current_price_for_ticker(self, company_id):
        """
        Retrieves the current price for a given company ticker symbol.

        Args:
            company_id (str): The ticker symbol of the company.

        Returns:
            float: The current price of the company's stock.
        """
        query = '''SELECT price
            FROM PriceHistory
            WHERE companyID = %s
            ORDER BY updatedAt DESC
            LIMIT 1;'''
        params = (company_id,)
        result = self.execute_query(query,params)
        return result[0][0]

    def get_score_history_from_companyID(self, companyID=None):
        """
        Retrieves the score history for a specific company.

        Args:
            companyID (str): The ID of the company. Defaults to None.

        Returns:
            list: A list of tuples containing the score and the update timestamp for each score history entry.
        """
        query = '''SELECT score, updatedAt
                FROM ScoreHistory
                WHERE companyID = %s;'''
        params = (companyID,)
        result = self.execute_query(query,params)
        return result
    
    def get_fund_category_from_ticker(self,companyID=None):
        """
        Retrieves the fund category associated with a given company ID.

        Parameters:
            companyID (str): The ID of the company.

        Returns:
            str: The fund category associated with the company ID.
        """
        query = '''SELECT fundCategory
                FROM Company
                WHERE companyID = %s;'''
        params = (companyID,)
        result = self.execute_query(query,params)
        return result
    
    def get_industry(self, companyID=None):
        """
        Retrieves the industry description for a given company ID.

        Args:
            companyID (str): The ID of the company. Defaults to None.

        Returns:
            str: The industry description for the specified company ID.
        """
        query = '''SELECT Industry.description
                FROM Company
                JOIN Industry ON Company.industryID = Industry.industryID
                WHERE Company.companyID = %s;'''
        params = (companyID,)
        result = self.execute_query(query,params)
        return result[0][0]
   
    def get_score_history_of_all_companies(self):
        """
        Retrieves the score history of all companies.

        Returns:
            scoreData (list): A list of dictionaries containing the company ID, score, and update timestamp for each company.
        """
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        scoreData = self.execute_query(query)
        return scoreData
    
    def get_price_history_of_all_companies(self):
        """
        Fetches the price history of all companies from the database.

        Args:
            data: Optional parameter for additional data.

        Returns:
            The price history data including company ID, price, and update timestamp.
        """
        query = f'''SELECT companyID, price, updatedAt
                FROM PriceHistory;'''
        priceData = self.execute_query(query)
        return priceData

    def get_companies_for_fund_category(self):
        """
        Retrieves companies grouped by fund category.

        Returns:
            dict: A dictionary where keys are fund categories ('Equity', 'Debt', 'Hybrid', 'Others'),
                and values are lists of company IDs belonging to each category.
        """
        result_dict={}
        categories=['Equity','Debt','Hybrid','Others']
        for category in categories:
            query=f'''SELECT companyID
                    FROM Company
                    WHERE fundCategory = "{category}";'''
            result=self.execute_query(query)
            result = [tup[0] for tup in result]
            result_dict[category]=result

        df = pd.DataFrame.from_dict(result_dict, orient='index').transpose()
        return result_dict
    
    def get_companies_for_industry_category(self):
        """
        Retrieves a dictionary of companies for each industry category.

        Returns:
            result_dict (dict): A dictionary where the keys are industry categories and the values are lists of company IDs.

        """
        result_dict={}
        categories=['Capital Goods','HealthCare','Financial','Services','Other','Consumer Staples']
        for category in categories:
            query=f'''SELECT Company.companyID
                        FROM Company
                        JOIN Industry ON Company.industryID = Industry.industryID
                        WHERE Industry.keyword = "{category}";'''
            result=self.execute_query(query)
            result = [tup[0] for tup in result]
            result_dict[category]=result

        df = pd.DataFrame.from_dict(result_dict, orient='index').transpose()

        return result_dict
    
    def get_company_name_from_ticker(self):
        """
        Retrieves a dictionary mapping company tickers to their names.

        Returns:
            dict: A dictionary where keys are company tickers and values are company names.
        """
        query=f'SELECT companyID, name  FROM Company;'
        result=self.execute_query(query)
        ticker_company_dict = {ticker: company_name for ticker, company_name in result}
        return ticker_company_dict
        
    def get_average_score_from_ticker(self, companyID=None):
        """
        Calculates the average score from the ScoreHistory table for a given company ID.

        Parameters:
            companyID (str): The ID of the company for which to calculate the average score. If a list is provided, only the first element will be used.

        Returns:
            float: The average score from the ScoreHistory table for the given company ID.
        """
        if isinstance(companyID,list):
            companyID=companyID[0]

        query='SELECT AVG(score) FROM ScoreHistory WHERE companyID=%s;'
        params = (companyID,)
        result=self.execute_query(query,params)

        return float(result[0][0])

    def get_companies(self,stocks,category):
        """
        Retrieves a list of companies based on the stocks and category provided.

        Parameters:
            stocks (dict): A dictionary containing stock tickers as keys and their corresponding amounts as values.
            category (str): The category of funds to filter the companies by.

        Returns:
            list: A list of dictionaries, where each dictionary contains a stock ticker as the key and its corresponding amount as the value.
        """
        companies = []
        
        for ticker, amount in stocks.items():
            if not ticker:
                break
            fund_category=self.get_fund_category_from_ticker(ticker)
            if category == fund_category[0][0]:
                companies.append({ticker: amount})
        return companies

    def get_company_details_for_credits(self):
        """
        Retrieves company details for credits.
        """
        query = f'''SELECT c.companyID AS compID,
                c.name,
                c.totalAssets,
                c.employeeCount,
                c.revenue,
                c.wallet,
                c.fundCategory,
                i.keyword AS industry,
                c.foundedYear
            FROM Company c
            JOIN Industry i ON c.industryID = i.industryID;'''
        result = self.execute_query(query)

        return result
    
    def update_wallet_balance(self, ticker, updated_wallet_balance):
        """
        Updates the wallet balance for a given company ticker.

        Parameters:
            ticker (str): The company ticker symbol.
            updated_wallet_balance (float): The updated wallet balance for the company.

        Returns:
            None
        """
        query = '''UPDATE Company SET wallet = %s WHERE companyID = %s;'''
        params = (updated_wallet_balance,ticker)
        try:
            self.execute_query(query, params)
            print(f"Wallet balance updated successfully for {ticker}")
        except Exception as e:
            print(f"Error updating wallet balance for {ticker}: {e}")
            raise
    
    def get_industry_keyword_from_companyID(self,companyID=None):
        """
        Retrieves the industry keyword associated with a given company ID.

        Parameters:
            companyID (str): The ID of the company. Defaults to None.

        Returns:
            list: A list of industry keywords associated with the company ID.
        """
        query = '''SELECT i.keyword
                FROM Company c
                JOIN Industry i ON c.industryID = i.industryID
                WHERE c.companyID = %s; '''
        params = (companyID,)
        result = self.execute_query(query,params)

        return result

    def get_wallet_balance_from_companyID(self,companyID=None):
        """
        Retrieves the wallet balance from the Company table based on the provided company ID.

        Parameters:
            companyID (str): The ID of the company.

        Returns:
            list: A list containing the wallet balance for the specified company ID.
        """
        query = '''SELECT wallet
                FROM Company
                WHERE companyID = %s; '''
        params = (companyID,)
        result = self.execute_query(query, params)

        return result
    
    def add_new_company(self, ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category):
        """
        A function to add a new company to the database.

        Parameters:
        - ticker (str): The stock ticker symbol of the company.
        - name (str): The name of the company.
        - total_assets (float): The total assets of the company.
        - revenue (float): The revenue of the company.
        - employee_count (int): The number of employees in the company.
        - founded_year (int): The year the company was founded.
        - industry_id (int): The ID of the industry the company belongs to.
        - fund_category (str): The category of funds the company belongs to.
        """
        query = """
            INSERT INTO Company (companyID, name, createdAt, updatedAt, totalAssets, revenue, employeeCount, currentScore, foundedYear, industryID, fundCategory, wallet)
            VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, 0.00 , %s, %s, %s, 0.00)
        """
        params = (ticker.upper(), name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category)
        try:
            self.execute_query(query, params)
            print("New company added successfully.")
        except Exception as e:
            print(f"Error adding new company: {e}")
            raise

    def get_industry_id_by_keyword(self, industry_keyword):
        """
        Retrieve the industry ID based on a given industry keyword.

        Parameters:
            industry_keyword (str): The keyword to search for in the Industry table.

        Returns:
            result: The industry ID corresponding to the provided keyword.
        """
        query = '''SELECT industryID FROM Industry WHERE keyword = %s;'''
        params = (industry_keyword,)
        result = self.execute_query(query,params)

        return result
    
    def get_companies_by_industry(self,stocks,industry):
        """
        Get companies by industry.

        Args:
            stocks (dict): A dictionary of stock tickers and corresponding amounts.
            industry (str): The industry to filter by.

        Returns:
            list: A list of dictionaries containing stock tickers and amounts for companies in the specified industry.
        """
        companies = []
        for ticker, amount in stocks.items():
            result= self.get_industry_keyword_from_companyID(ticker)
            if industry == result[0][0]:
                companies.append({ticker: amount})
        return companies
    
    def get_score_and_ticker_map(self):
        """
        Retrieves the average score for each company from the ScoreHistory table.

        Returns:
            score_dict (dict): A dictionary mapping company IDs to their average scores.
        """
        query=""" SELECT companyID, AVG(score) AS average_score
            FROM ScoreHistory
            GROUP BY companyID """
        result=self.execute_query(query)
        score_dict = {company_id: average_score for company_id, average_score in result}

        return score_dict
    
    def add_company_signup_details(self, company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance,industryID,fund_category):
        """
        Adds company signup details to the database.

        Parameters:
            company_name (str): The name of the company.
            company_ticker (str): The ticker symbol of the company.
            password (str): The password for the company's account.
            initial_money_wallet_balance (float): The initial balance in the money wallet.
            initial_credits_wallet_balance (float): The initial balance in the credits wallet.
            industryID (int): The industry ID of the company.
            fund_category (str): The category of fund.

        Returns:
            None
        """
        query = """
            INSERT INTO CompanySignup (CompanyName, CompanyTicker, Password, InitialMoneyWalletBalance, InitialCreditsWalletBalance, fundCategory, industryID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance,fund_category,industryID)
        try:
            self.execute_query(query, params)
            print("Company signup details added successfully.")
        except Exception as e:
            print(f"Error adding company signup details: {e}")
    
    def get_signup_company_data(self, name):
        """
        Retrieves signup company data based on the given company name.

        Parameters:
            name (str): The name of the company.

        Returns:
            list: A list of dictionaries containing the signup company data.
        """
        query = '''SELECT * FROM CompanySignup WHERE CompanyTicker = %s;'''
        params = (name, )
        result = self.execute_query(query,params)
        return result
    
    def update_credit_wallet_balance(self, ticker, credits):
        """
        Updates the credit wallet balance for a specific company.

        Parameters:
            self (obj): The object itself.
            ticker (str): The company ticker symbol.
            credits (int): The amount of credits to update the balance by.

        Returns:
            None
        """
        query = '''UPDATE CompanySignup
                    SET InitialCreditsWalletBalance = InitialCreditsWalletBalance - %s
                    WHERE CompanyTicker = %s;'''
        params = (credits,ticker)
        try:
            self.execute_query(query, params)
            print("updated credit wallet balance successfully.")
        except Exception as e:
            print(f"Error updating credit wallet balance : {e}")

    def add_listed_credit_to_bid(self, initial_bid, min_step, credits, ticker):
        """
        Adds a listed credit to the bid table in the database.

        Parameters:
            initial_bid (float): The initial bid amount.
            min_step (float): The minimum step size for the bid.
            credits (int): The number of credits listed for the bid.
            ticker (str): The ticker symbol of the company.

        Returns:
            None

        Raises:
            Exception: If there is an error executing the query.
        """
        query= '''INSERT INTO Bid (initial_Bid, minimum_Step, credits_Listed, companyID)
                VALUES (%s, %s, %s, %s);'''
        params = (initial_bid, min_step, credits, ticker)
        try:
            self.execute_query(query)
            print("added listed credit to bid successfully")
        except Exception as e:
            print(f"Error adding listed credit to bid : {e}")

    def get_industry_keyword_from_companySignup_ticker(self,ticker):
        """
        Retrieves the industry keyword associated with a given company ticker.

        Parameters:
            ticker (str): The company ticker.

        Returns:
            list: A list of industry keywords.
        """
        query = '''SELECT i.keyword
                FROM CompanySignup cs
                JOIN Industry i ON cs.industryID = i.industryID
                WHERE cs.CompanyTicker = %s; '''
        params = (ticker,)
        result = self.execute_query(query,params)

        return result
    
    def get_wallet_balance_from_companySignup_ticker(self,ticker):
        """
        Retrieves the initial credit wallet balance for a given company ticker.

        Parameters:
            ticker (str): The company ticker.

        Returns:
            result (object): The initial credit wallet balance.
        """
        query = '''SELECT InitialCreditsWalletBalance
                FROM CompanySignup
                WHERE CompanyTicker = %s; '''
        params = (ticker,)
        result = self.execute_query(query, params)

        return result
    
    def add_credits_wallet_balance_from_companySignup_ticker(self, ticker, updated_wallet_balance):
        """
        Updates the initial credits wallet balance of a company with the given ticker in the CompanySignup table.

        Parameters:
            ticker (str): The ticker of the company to update the wallet balance for.
            updated_wallet_balance (int): The new value for the wallet balance.

        Returns:
            None

        Raises:
            Exception: If there is an error updating the wallet balance.
        """
        query = '''UPDATE CompanySignup SET InitialCreditsWalletBalance = %s WHERE CompanyTicker = %s;'''
        params = (updated_wallet_balance, ticker)
        try:
            self.execute_query(query)
            print(f"Credits Wallet balance updated successfully for {ticker}")
        except Exception as e:
            print(f"Error updating credits wallet balance for {ticker}: {e}")
            raise

    def get_listings_for_auction(self):
        """
        Get listings for an auction.

        No parameters.

        Returns:
            The result of the query to retrieve listings.
        """
        query = "SELECT * FROM Bid;"
        result = self.execute_query(query)
        return result

    def get_my_biddings(self):
        """
        Method to retrieve all biddings from the database.
        """
        query = "SELECT * FROM Bidding;"
        result = self.execute_query(query)
        return result
    
    def insert_into_bidding_table(self,bidder, bidID, bid):
        """
        Inserts a new bid into the Bidding table.

        Parameters:
            bidder (str): The name of the bidder.
            bidID (int): The ID of the bid.
            bid (int): The value of the bid.

        Returns:
            None
        """
        query = """INSERT INTO Bidding (bidder, bidID, bid)
        VALUES (%s, %s, %s);"""
        params = (bidder,bidID,bid)
        try:
            self.execute_query(query,params)
            print("added to bidding table successfully")
        except Exception as e:
            print(f"Error adding to bidding table : {e}")

    def get_max_bidding_amount(self, ticker):
        """
        Retrieves the maximum bidding amount for a given ticker.

        Parameters:
            ticker (str): The ticker symbol of the company.

        Returns:
            list: A list containing the maximum bidding amount.
        """
        query = '''SELECT MAX(b.bid) AS max_bid
                    FROM Bidding b
                    JOIN Bid bd ON b.bidID = bd.bidID
                    WHERE bd.companyID = %s;'''
        params = (ticker,)
        result = self.execute_query(query,params)
        return result

    def get_companyID_from_bidID(self, bidID):
        """
        Retrieves the company ID associated with a given bid ID.

        Parameters:
            bidID (str): The ID of the bid.

        Returns:
            list: A list containing the company ID associated with the bid ID.
        """
        query = '''SELECT companyID AS cID
                    FROM Bid as bd
                    JOIN Bidding b on b.bidID = bd.bidID
                    WHERE b.bidID = %s;'''
        params = (bidID,)
        result = self.execute_query(query, params)
        return result
    
    def get_bidding_details_from_ticker(self, ticker):
        """
        Retrieves the bidding details for a specific ticker.

        Parameters:
            ticker (str): The ticker symbol of the company.

        Returns:
            list: A list of dictionaries containing the bidder, bid amount, and bid ID for the specified ticker.
        """
        query = '''SELECT b.bidder, b.bid, b.bidID
                    FROM Bidding as b
                    JOIN Bid bd on b.bidID = bd.bidID
                    WHERE bd.companyID = %s;'''
        params = (ticker,)
        result = self.execute_query(query,params)
        return result
    
    def get_credits_listed_from_bidID(self, bidID):
        """
        Retrieves the credits listed for a given bid ID.

        Parameters:
            bidID (str): The ID of the bid.

        Returns:
            list: The list of credits listed for the bid.
        """
        query = '''SELECT credits_Listed
                    FROM Bid
                    WHERE bidID = %s;'''
        params = (bidID,)
        result = self.execute_query(query, params)
        return result
    
    def add_money_to_wallet(self,ticker,money):
        """
        Updates the initial money wallet balance of a company with the specified ticker by adding the given amount of money.

        Parameters:
            ticker (str): The ticker symbol of the company.
            money (float): The amount of money to be added to the wallet balance.

        Returns:
            None

        Raises:
            Exception: If there is an error while updating the wallet balance.
        """
        query = '''UPDATE CompanySignup
                    SET InitialMoneyWalletBalance = InitialMoneyWalletBalance + %s
                    WHERE CompanyTicker = %s;'''
        params = (money,ticker)
        try:
            self.execute_query(query, params)
            print("added to money wallet balance successfully")
        except Exception as e:
            print(f"Error adding to money wallet balance : {e}")

    def add_credit_to_credit_wallet(self,ticker,cred_listed):
        """
        Updates the InitialCreditsWalletBalance in the CompanySignup table by adding the specified amount of credits to the current balance for the given company ticker.

        Parameters:
            ticker (str): The company ticker for which the credits are to be added.
            cred_listed (int): The amount of credits to be added to the wallet balance.

        Returns:
            None
        """
        query = '''UPDATE CompanySignup
                    SET InitialCreditsWalletBalance = InitialCreditsWalletBalance + %s
                    WHERE CompanyTicker = %s;'''
        params = (cred_listed, ticker)
        try:
            self.execute_query(query,params)
            print("added credit to credit balance successfully")
        except Exception as e:
            print(f"Error adding credit to credit wallet balance : {e}")

    def subtract_money_from_wallet(self,ticker,money):
        """
        Subtracts a specified amount of money from the initial money wallet balance of a company with the given ticker.

        Parameters:
            ticker (str): The ticker symbol of the company.
            money (float): The amount of money to subtract from the wallet balance.

        Returns:
            None

        Raises:
            Exception: If there is an error subtracting the money from the wallet balance.
        """
        query = '''UPDATE CompanySignup
                    SET InitialMoneyWalletBalance = InitialMoneyWalletBalance - %s
                    WHERE CompanyTicker = %s;'''
        params = (money,ticker)
        try:
            self.execute_query(query, params)
            print("subtracted money from wallet balance successfully")
        except Exception as e:
            print(f"Error subtracting money from wallet balance : {e}")

    def remove_bid_from_bidID(self, bidID):
        """
        This function removes a bid and its associated bid details from the database.
        
        Parameters:
            bidID (int): The ID of the bid to be removed.
            
        Returns:
            None
        """
        query = '''DELETE B, BD
                    FROM Bidding B
                    JOIN Bid BD ON B.bidID = BD.bidID
                    WHERE B.bidID = %s;'''
        params = (bidID,)
        try:
            self.execute_query(query, params)
            print("removed successfully")
        except Exception as e:
            print(f"Error removing : {e}")
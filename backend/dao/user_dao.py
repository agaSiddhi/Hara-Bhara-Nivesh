import mysql.connector
# from backend.database import return_price_and_date, return_score_and_date
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
from backend.dao.dao import CompanyDao
import pycountry_convert as pc
import string

class UserDao(CompanyDao):
    """
    This class provides methods to interact with the User table and related tables in a MySQL database.
    It inherits from the CompanyDao class and provides additional functionalities specific to user data.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes a UserDao object with the connection details to the MySQL database.

        Args:
            host (str): The hostname or IP address of the MySQL server.
            user (str): The username to access the MySQL database.
            password (str): The password to access the MySQL database.
            database (str): The name of the database containing the user tables.
        """
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            # port = port
        )

    def execute_query(self, query, params=None):
        """
        Executes a query on the MySQL database connection and returns the results.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): A tuple of parameters to be used in the query. Defaults to None.

        Returns:
            list: A list of tuples containing the results of the query.

        Raises:
            mysql.connector.Error: If an error occurs during the query execution.
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

    def add_user_details(self, username, name, password, age, country, gender):
        """
        Adds a new user to the User table in the database.

        Args:
            username (str): The unique username of the user.
            name (str): The full name of the user.
            password (str): The encrypted password of the user.
            age (int): The age of the user.
            country (str): The country of residence of the user.
            gender (str): The gender of the user (e.g., male, female, others).
        """
        query = f'''INSERT INTO User (username, name, password, balance, age, country, gender) VALUES ("{username}", "{name}", "{password}", {10000}, "{age}", "{country}", "{gender}");'''
        self.execute_query(query)

    def add_user_email(self, username, email):
        """
        Adds an email address for a user to the User_mail table in the database.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
        """
        query = f'''INSERT INTO User_mail (username, email) VALUES ("{username}", "{email}");'''
        self.execute_query(query)

    def get_user_data(self):
        """
        Retrieves all user data from the User and User_mail tables.

        Returns:
            tuple: A tuple containing two lists. The first list contains user data from the User table,
                   and the second list contains email data from the User_mail table.
        """
        query = '''SELECT * FROM User;'''
        user_data = self.execute_query(query)
        query = '''SELECT * FROM User_mail;'''
        user_mail_data = self.execute_query(query)
        return user_data, user_mail_data

    def get_user_name_ticker_from_portfolio(self):
        """
        Retrieves a list of username and ticker symbol pairs from the Portfolio_entry table.

        Returns:
            list: A list of tuples containing username and ticker symbol pairs.
        """
        query = f'''
        SELECT username, Ticker
        FROM Portfolio_entry;'''
        result = self.execute_query(query)
        return result
    
    def add_uploaded_file_to_current_portfolio(self,uploaded_file):
        """
        Processes an uploaded file containing portfolio transactions and adds them to the database.

        Args:
            uploaded_file (pandas.DataFrame): A pandas DataFrame containing the uploaded portfolio data.
        """
        for _, row in uploaded_file.iterrows():
            """
            Iterates through each row of the uploaded DataFrame and adds the transaction data to the Portfolio_entry table.

            Args:
                row (pandas.Series): A pandas Series representing a single row of the DataFrame.
            """
            query = f'''
                INSERT INTO Portfolio_entry (date, order_type, Ticker, amount, price_quote,username)
                VALUES ("{row['Date'].strftime('%Y-%m-%d')}","{row['Order Type']}", "{row['Ticker']}", {float(row['Amount'])}, {float(row['Price/Quote'])}, "{st.session_state.get('username')}");
            '''
      
            self.execute_query(query)
    
    def get_wallet_balance(self, username):
        """
        Retrieves the current wallet balance of a user.

        Args:
            username (str): The username of the user.

        Returns:
            float: The current wallet balance of the user.
        """
        query = f'''SELECT balance
                FROM User
                WHERE username = "{username}";'''
        result = self.execute_query(query)
        return result[0][0]

    def update_transaction_history(self, company_id, quantity, price_per_stock, order_type):
        """
        Updates the Transaction_history table with a new transaction record.

        Args:
            company_id (str): The ticker symbol of the company involved in the transaction.
            quantity (int): The number of shares bought or sold.
            price_per_stock (float): The price per share of the stock.
            order_type (str): The type of order (e.g., buy, sell).
        """
        today_date = dt.today()
        today_date_str = today_date.strftime('%Y-%m-%d')
        query = f'''INSERT INTO Transaction_history (order_type, date, amount, ticker, username, price_quote) 
        VALUES ("{order_type}","{today_date_str}",{quantity},"{company_id}","{st.session_state.get('username')}",{price_per_stock});'''
        self.execute_query(query)

    def update_portfolio(self, company_id, quantity, price_per_stock, order_type):
        """
        Updates the Portfolio_entry table with a new portfolio entry.

        Args:
            company_id (str): The ticker symbol of the company involved in the transaction.
            quantity (int): The number of shares bought or sold.
            price_per_stock (float): The price per share of the stock.
            order_type (str): The type of order (e.g., buy, sell).
        """
        today_date = dt.today()
        today_date_str = today_date.strftime('%Y-%m-%d')
        query = f'''INSERT INTO Portfolio_entry (order_type, date, amount, ticker, username, price_quote) 
        VALUES ("{order_type}","{today_date_str}",{quantity},"{company_id}","{st.session_state.get('username')}",{price_per_stock});'''
        self.execute_query(query)

    def get_current_price_for_ticker(self, company_id):
        """
        Retrieves the current price for a given company ticker symbol.

        Args:
            company_id (str): The ticker symbol of the company.

        Returns:
            float: The current price of the company's stock.
        """
        query = f'''SELECT price
            FROM PriceHistory
            WHERE companyID = "{company_id}"
            ORDER BY updatedAt DESC
            LIMIT 1;'''
        result = self.execute_query(query)
        return result[0][0]

    def update_wallet(self, user_wallet):
        """
        Updates the wallet balance of a user in the User table.

        Args:
            user_wallet (float): The new wallet balance of the user.
        """
        query = f'''UPDATE User
                 SET balance = {user_wallet}
                 WHERE username = "{st.session_state.get('username')}"; '''
        self.execute_query(query)  
        
    def get_usernames(self):
        """
        Retrieves all usernames from the User table.

        Returns:
            list: A list of usernames.
        """
        query = '''SELECT username FROM User;'''
        result = self.execute_query(query)
        return [row[0] for row in result]     
    
    def get_mail(self, username):
        """
        Retrieves the email address of a user.

        Args:
            username (str): The username of the user
        Returns:
            str: The email address of the user, or None if not found.
        """
        query = f'''SELECT email from User_mail
                WHERE username="{username}";'''
        result = self.execute_query(query)
        if result:
            return result[0][0]
        else:
            return None
    

    def get_portfolio_entry_for_user(self, username):
        """
        Retrieves all portfolio entries for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            pandas.DataFrame: A DataFrame containing the user's portfolio data.
        """
        query = f'''SELECT amount, date, order_type, price_quote, Ticker
            FROM Portfolio_entry WHERE username="{username}"; '''
        result = self.execute_query(query)
        df = pd.DataFrame(result, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"])
        df = df.sort_values(by='Date')
        return df

    def get_name_from_username(self, username):
        """
        Retrieves the full name of a user.

        Args:
            username (str): The username of the user.

        Returns:
            str: The full name of the user, or None if not found.
        """
        query = f'''SELECT name FROM User WHERE username="{username}";'''
        result = self.execute_query(query)
        if result:
            return result[0][0]
        else:
            return None

    def get_transaction_history(self, username):
        """
        Retrieves the transaction history for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            pandas.DataFrame: A DataFrame containing the user's transaction history data.
        """
        query = f'''
        SELECT amount, date, order_type, price_quote, Ticker
        FROM Transaction_history
        WHERE username = '{username}';'''
        result = self.execute_query(query)
        df = pd.DataFrame(result, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"])
        df = df.sort_values(by='Date')
        return df

    def get_age_from_username(self, username):
        """
        Retrieves the age of a user.

        Args:
            username (str): The username of the user.

        Returns:
            int: The age of the user, or None if not found.
        """
        query = f'''SELECT age from User
                WHERE username="{username}";'''
        result = self.execute_query(query)
        if result:
            return result[0][0]
        else:
            return None

    def get_gender_from_username(self, username):
        """
        Retrieves the gender of a user.

        Args:
            username (str): The username of the user.

        Returns:
            str: The gender of the user, or None if not found.
        """
        query = f'''SELECT gender from User
                WHERE username="{username}";'''
        result = self.execute_query(query)
        if result:
            return result[0][0]
        else:
            return None

    def get_country_from_username(self, username):
        """
        Retrieves the country of residence of a user.

        Args:
            username (str): The username of the user.

        Returns:
            str: The country of residence of the user, or None if not found.
        """
        query = f'''SELECT country from User
                WHERE username="{username}";'''
        result = self.execute_query(query)
        if result:
            return result[0][0]
        else:
            return None

    def get_time_frequency_of_user(self):
        """
        Calculates the frequency of transactions made by a user over time.

        Returns:
            pandas.DataFrame: A DataFrame containing the date and number of transactions for each date.
        """
        query = f'''SELECT date, COUNT(transactionID) AS num_transactions
                    FROM Transaction_history
                    GROUP BY date;'''
        result = self.execute_query(query)
        df = pd.DataFrame(result, columns=['date', 'num_transactions'])
        return df

    def get_date_amount_for_avg_insights(self):
        """
        Retrieves dates and transaction amounts for calculating average investment insights.

        Returns:
            pandas.DataFrame: A DataFrame containing the date and transaction amount for each transaction.
        """
        query = f'''SELECT date, amount FROM Transaction_history;'''
        result = self.execute_query(query)
        df = pd.DataFrame(result, columns=['date', 'amount'])
        return df
    
    def get_score_history_of_all_companies(self):
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        scoreData = self.execute_query(query)
        df = pd.DataFrame(scoreData, columns=['tickers', 'score', 'dates'])
        df['Date']=pd.to_datetime(df['dates'])
        df = df.pivot(index="Date", columns="tickers", values="score")
        df.fillna(method='ffill', inplace=True)
        df=df.fillna(0)
        return df
    


        
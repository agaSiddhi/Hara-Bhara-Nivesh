import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from datetime import datetime as dt
from backend.dao.dao import CompanyDao
from backend.dao.user_dao import UserDao
import streamlit as st
import pycountry_convert as pc
import string
from logger import logger
logger = logger.get_logger()


class CompanyService():
    def __init__(self, company_dao):
        self.company_dao = company_dao
        logger.basicConfig(filename="./app.log", filemode='w')
    
    def return_company_name_and_description(self):
        """
        Retrieve the names, scores, and descriptions of companies.

        Returns:
            dict: A dictionary where keys are company names and values are lists containing the company's current score,
                industry description, and rank based on score (in ascending order).
        """
        results= self.company_dao.get_company_name_and_description()
        descriptions = {}
        rank = 1
        for row in results:
            temp = list(row[1:])
            temp.append(rank)
            descriptions[row[0]] = temp
            rank += 1

        return descriptions

    def return_companyID_from_company_name(self,companyName=None):
        """
        Retrieve the companyID of a company given its name.

        Args:
            company_name (str): The name of the company for which the companyID is to be retrieved.

        Returns:
            str: The companyID of the company.
        """
        return self.company_dao.get_companyID_from_company_name(company_name=companyName)

    def return_company_details_from_companyID(self,companyID=None):
        """
        Retrieve details of a company identified by its companyID.

        Args:
            companyID (str): The ID of the company for which details are to be retrieved.

        Returns:
            tuple: A tuple containing the following details of the company:
                - companyID (str): The ID of the company.
                - companyName (str): The name of the company.
                - createdAt (datetime): The creation date of the company.
                - updatedAt (datetime): The last update date of the company.
                - totalAssets (float): The total assets of the company.
                - revenue (float): The revenue of the company.
                - employeeCount (int): The number of employees in the company.
                - currentScore (float): The current score of the company.
                - foundedYear (int): The year the company was founded.
                - url (str): The URL of the company's website.
        """
        return self.company_dao.get_company_details_from_companyID(companyID=companyID)
    
    def return_ESG_score_from_companyID(self,companyID=None):
        """
        Retrieve the ESG (Environmental, Social, Governance) scores of a company identified by its companyID.

        Args:
            companyID (str): The ID of the company for which the ESG scores are to be retrieved.

        Returns:
            tuple: A tuple containing the Environmental, Social, and Governance scores of the company.
        """
        return self.company_dao.get_ESG_score_from_companyID(companyID=companyID)

    def return_industry_description_from_companyID(self,companyID=None):
        """
        Retrieve the industry description of a company identified by its companyID.

        Args:
            companyID (str): The ID of the company for which the industry description is to be retrieved.

        Returns:
            str: The industry description of the company.
        """
        return self.company_dao.get_industry_description_from_companyID(companyID=companyID)

    def return_score_history_from_companyID(self,companyID=None):
        """
        Retrieve the score history of a company identified by its companyID.

        Args:
            companyID (str): The ID of the company for which the score history is to be retrieved.

        Returns:
            list: A list of tuples containing scores and corresponding update timestamps.
        """
        return self.company_dao.get_score_history_from_companyID(companyID=companyID)

    def return_price_history_from_companyID(self,companyID=None):
        """
        Retrieve the price history of a company identified by its companyID.

        Args:
            companyID (str): The ID of the company for which the price history is to be retrieved.

        Returns:
            list: A list of tuples containing price and corresponding update timestamps.
        """
        return self.company_dao.get_price_history_from_companyID(companyID=companyID)

    def return_category_percentage(self,stocks=None):
        """
        Calculate the percentage of stocks held in each fund category based on the given stock quantities.

        Args:
            stocks (dict): A dictionary where keys are company tickers and values are corresponding stock quantities.

        Returns:
            dict: A dictionary containing the percentage of stocks held in each fund category.
        """
    # Calculate the percentage of each category
        total_stocks = sum(stocks.values())
        category_percentage = {'Equity': 0, 'Debt': 0, 'Hybrid': 0, 'Others': 0}
        for ticker, amount in stocks.items():
            category= self.company_dao.get_fund_category_from_ticker(ticker)
            category_percentage[category[0][0]] += amount / total_stocks
        return category_percentage

    def return_industry_percentage(self,stocks=None):
        """
        Calculate the percentage of stocks held in each industry based on the given stock quantities.

        Args:
            stocks (dict): A dictionary where keys are company tickers and values are corresponding stock quantities.

        Returns:
            dict: A dictionary containing the percentage of stocks held in each industry.
        """
        total_stocks = sum(stocks.values())
        # Calculate the percentage of each industry
        industry_percentage = {'Capital Goods': 0, 'Financial': 0, 'Services': 0, 'HealthCare': 0, 'Consumer Staples':0, 'Other':0}
        for ticker, amount in stocks.items():
            industry = self.company_dao.get_industry_keyword_from_companyID(ticker)
            industry_percentage[industry[0][0]] += amount / total_stocks
        return industry_percentage
    
    def calculate_portfolio_balance(self,data=None):
        """
        Calculate the total balance of the portfolio based on the provided stock data.
        """
        return self.company_dao.calculate_portfolio_balance(data=data)

    def calculate_portfolio_score(self,data=None):
        """
        Calculate the total score of the portfolio based on the provided stock data.
        """
        return self.company_dao.calculate_portfolio_score(data=data)
    
    def return_companies_for_fund_category(self):
        """
        Retrieve a dictionary mapping fund categories to lists of companies associated with each category.

        Returns:
            dict: A dictionary where keys are fund categories and values are lists of company IDs.
        """
        return self.company_dao.get_companies_for_fund_category()
    
    def return_companies_for_industry_category(self):
        """
        Retrieve a dictionary mapping industry categories to lists of companies associated with each category.

        Returns:
            dict: A dictionary where keys are industry categories and values are lists of company IDs.
        """
        return self.company_dao.get_companies_for_industry_category()
    
    def return_company_name_from_ticker(self):
        """
        Retrieve a dictionary mapping company tickers to their corresponding names.

        Returns:
            dict: A dictionary where keys are company tickers and values are company names.
        """
        return self.company_dao.get_company_name_from_ticker()
    
    def return_industry_from_ticker(self,companyID=None):
        """
        Retrieve the industry description associated with a company based on its ID.

        Args:
            companyID (str): The ID of the company.

        Returns:
            str: The industry description of the specified company.
        """
        return self.company_dao.get_industry(companyID)
    
    def return_fund_category_from_ticker(self,companyID=None):
        """
        Retrieve the fund category associated with a company based on its ID.

        Args:
            companyID (str): The ID of the company.

        Returns:
            list: A list containing the fund category of the specified company.
        """
        return self.company_dao.get_fund_category_from_ticker(companyID)
    
    def return_average_score_from_ticker(self,companyID=None):
        """
        Retrieve the average score from the score history for a specific company.

        Args:
            companyID (str or list): The company ID or a list containing the company ID.

        Returns:
            float: The average score for the specified company.
        """
        return self.company_dao.get_average_score_from_ticker(companyID)
     
    def return_companies(self,stocks,category):
        """
        Retrieve companies belonging to a specific fund category from the provided stock data.

        Args:
            stocks (dict): A dictionary containing ticker symbols as keys and corresponding amounts as values.
            category (str): The fund category to filter companies by.

        Returns:
            list: A list of dictionaries, where each dictionary contains ticker symbols as keys and their
                respective amounts as values, for companies belonging to the specified fund category.
        """
        companies = []
        
        for ticker, amount in stocks.items():
            if not ticker:
                break
            fund_category=self.company_dao.get_fund_category_from_ticker(ticker)
            if category == fund_category[0][0]:
                companies.append({ticker: amount})
        return companies

    def return_ticker_percentages(self,companies):
        """
        Calculate the percentage composition of each ticker in the provided list of companies.

        Args:
            companies (list): List of dictionaries containing ticker symbols as keys and corresponding
                            amounts as values.

            Returns:
            dict: A dictionary where keys are ticker symbols and values are their respective percentages
                of the total amount invested.
        """
        # Getting composition of each ticker in out category

        total_amount = sum(amount for company in companies for amount in company.values())
        ticker_percentages = {}
        if(total_amount==0):
            return ticker_percentages
        for company in companies:

            for ticker, amount in company.items():

                if not ticker:
                    break
                percentage = (amount / total_amount) 
                if percentage!=0:
                    ticker_percentages[ticker] = percentage
                    
        ticker_percentages = dict(sorted(ticker_percentages.items(), key=lambda item: item[1], reverse=True))
        return ticker_percentages
    
    def return_company_details_for_credits(self):
        """
        Retrieve company details relevant for credits.

        Returns:
            pandas.DataFrame: DataFrame containing company details including company ID, name, total assets, 
            employee count, revenue, wallet balance, fund category, industry, and founded year.
        """
        return self.company_dao.get_company_details_for_credits()
    
    def get_current_price_for_ticker(self,ticker):
        """
        Retrieves the current price for a given company ticker symbol.

        Args:
            company_id (str): The ticker symbol of the company.

        Returns:
            float: The current price of the company's stock.
        """
        return self.company_dao.get_current_price_for_ticker(ticker)
    
    def carry_over(self,score_data,field):
        """
        Carry over the score data for missing dates.

        Args:
            score_data (pandas.DataFrame): DataFrame containing score data with a 'Date' column.
            field (str): The column name containing the score values.

        Returns:
            pandas.DataFrame: DataFrame with missing scores filled by carrying over the last available score
            and interpolating missing scores at the beginning.
        """
        
        # Define the start and end dates for the data
        start_date = '2023-01-01'
        end_date = dt.today().strftime('%Y-%m-%d')

        # Generate a list of dates from start_date to end_date
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        # Convert the 'Date' column to datetime format
        score_data['Date'] = pd.to_datetime(score_data['Date'])
        
        # Set 'Date' as the index for score_data
        score_data.set_index('Date', inplace=True)
        
        # Sort the DataFrame by date
        score_data = score_data.sort_values(by='Date')
        
        # Fill missing dates with NaN scores
        score_data = score_data.reindex(date_range)

        # Carry over the score from the previous available date
        score_data[field].fillna(method='ffill', inplace=True)

        # Fill missing scores at the beginning with the average of available scores
        score_data[field].fillna(score_data[field].mean(), inplace=True)

        # Reset the index to have the 'Date' as a column
        score_data.reset_index(drop=True,inplace=True)
        score_data['Date']=date_range
        # Print the interpolated scores DataFrame
        return score_data
    
    def return_update_wallet_balance(self, ticker, updated_wallet_balance):
        """
        Update the wallet balance of a company in the database.

        Args:
            ticker (str): The ticker symbol of the company.
            updated_wallet_balance (float): The updated wallet balance to be set for the company.

        Returns:
            bool: True if the wallet balance is updated successfully, False otherwise.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.update_wallet_balance(ticker, updated_wallet_balance)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error updating wallet balance for {ticker}: {e}")
            return False  # Indicate failure
    
    def return_industry_keyword_from_companyID(self,companyID=None):
        """
        Retrieve the industry keyword of a company by its ID.

        Args:
            companyID (str, optional): The ID of the company. Defaults to None.

        Returns:
            list: A list containing the industry keyword of the company.
        """
        return self.company_dao.get_industry_keyword_from_companyID(companyID=companyID)
    

    def return_wallet_balance_from_companyID(self,companyID=None):
        """
        Retrieve the wallet balance of a company by its ID.

        Args:
            companyID (str, optional): The ID of the company. Defaults to None.

        Returns:
            list: A list containing the wallet balance of the company.
        """
        return self.company_dao.get_wallet_balance_from_companyID(companyID=companyID)
    
    def return_add_new_company(self, ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category):
        """
        Add a new company to the database.

        Args:
            ticker (str): The ticker symbol of the new company.
            name (str): The name of the new company.
            total_assets (float): The total assets of the new company.
            revenue (float): The revenue of the new company.
            employee_count (int): The employee count of the new company.
            founded_year (int): The year the new company was founded.
            industry_id (int): The industry ID of the new company.
            fund_category (str): The fund category of the new company.

        Returns:
            bool: True if the company is successfully added, False otherwise.
        """
        try:
            # Call the DAO method to insert the new company into the database
            self.company_dao.add_new_company(ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error adding new company: {e}")
            return False  # Indicate failure

    def return_industry_id_by_keyword(self, industry_keyword):
        """
        Retrieve the industry ID corresponding to a given industry keyword.

        Args:
            industry_keyword (str): The keyword representing the industry.

        Returns:
            list: A list containing the industry ID(s) corresponding to the given keyword.
        """
        return self.company_dao.get_industry_id_by_keyword(industry_keyword)
    
    def return_companies_by_industry(self,stocks,industry):
        """
        Get companies from the given stocks belonging to the specified industry.

        Args:
            stocks (dict): Dictionary containing stock tickers as keys and corresponding amounts.
            industry (str): The industry keyword to filter the companies.

        Returns:
            list: List of dictionaries containing company tickers as keys and corresponding amounts.
        
        """
        return self.company_dao.get_companies_by_industry(stocks,industry)

    def filter_companies(self,selected_categories, selected_sectors):
        """
        Filter companies based on selected fund categories and industry sectors.

        Args:
            selected_categories (list): List of selected fund categories.
            selected_sectors (list): List of selected industry sectors.

        Returns:
            dict: A dictionary containing filtered companies with their corresponding scores, categories, and sectors.
        """
        data1=  self.company_dao.get_companies_for_fund_category()
        data2= self.company_dao.get_companies_for_industry_category()
        scores_dict=self.company_dao.get_score_and_ticker_map()

        filtered_companies = {}
        for category in selected_categories:
            if category in data1:
                for company in data1[category]:
                    if company not in filtered_companies:
                        filtered_companies[company] = {'score': scores_dict[company], 'category': category, 'sector': None}
        
        for sector in selected_sectors:
            if sector in data2:
                for company in data2[sector]:
                    if company not in filtered_companies:
                        # filtered_companies[company] = {'score': scores_dict[company], 'category': None, 'sector': sector}
                        continue
                    else:
                        # If the company is already in the dictionary (from data1), update its sector
                        filtered_companies[company]['sector'] = sector
        filtered_companies = {company: details for company, details in filtered_companies.items() if details['sector'] is not None}
        filtered_companies = dict(sorted(filtered_companies.items(), key=lambda x: x[1]['score'], reverse=True))
        return filtered_companies      

    def return_add_new_company_signup(self, company_name,company_ticker,password,initial_money_wallet_balance,initial_credits_wallet_balance,industry,fund_category):
        """
        Adds new company signup details to the database.

        Args:
            company_name (str): The name of the company.
            company_ticker (str): The ticker symbol of the company.
            password (str): The password for the company account.
            initial_money_wallet_balance (float): The initial money wallet balance for the company.
            initial_credits_wallet_balance (float): The initial credits wallet balance for the company.
            industry (str): The industry keyword for the company.
            fund_category (str): The fund category for the company.

        Returns:
            bool: True if the company signup details are successfully added, False otherwise.
        """
        industryID = self.return_industry_id_by_keyword(industry)[0][0]
        # logger.info("debug industry iD", industryID)
        try:
            # Call the DAO method to insert the new company into the database
            self.company_dao.add_company_signup_details(company_name,company_ticker,password,initial_money_wallet_balance,initial_credits_wallet_balance,industryID,fund_category)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error adding new company: {e}")
            return False  # Indicate failure
    
    def get_company_data_dict(self):
        """
        Retrieves company data from the database and organizes it into a dictionary.

        Returns:
            dict: A dictionary containing company data organized by ticker symbol.
                Each company entry includes name, password, initial money wallet balance,
                initial credits wallet balance, fund category, and industry ID.
        """
        company_data = self.company_dao.get_company_data()
        company_data_dict = {}
        for row in company_data:
            name, ticker,password, initial_money_wallet_balance,initial_credits_wallet_balance,fundCategory, industryID = row
            company_data_dict[ticker] = {
                'name' : name,
                'password': password,
                'money_wallet' : initial_money_wallet_balance,
                'credit_wallet' : initial_credits_wallet_balance,
                'fund_category' : fundCategory,
                'industry': industryID
                }
        company_data_dict= {'usernames': company_data_dict}
        # print('H',company_data_dict)
        return company_data_dict 
    
    def return_signup_company_data(self, name):
        """
        Retrieves the signup data for a company based on its ticker symbol.

        Args:
            name (str): The ticker symbol of the company.

        Returns:
            list: A list containing the signup data for the company.
        """
        return self.company_dao.get_signup_company_data(name)
    
    def return_update_credit_wallet_balance(self, ticker, credits):
        """
        Updates the credit wallet balance for the specified company.

        Args:
            ticker (str): The ticker symbol of the company.
            credits (int): The number of credits to subtract from the wallet balance.

        Returns:
            bool: True if the credit wallet balance is updated successfully, False otherwise.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.update_credit_wallet_balance(ticker, credits)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error updating credit wallet balance for {ticker}: {e}")
            return False  # Indicate failure

    def add_listed_credit_to_bid(self, initial_bid, min_step, credits, ticker):
        """
        Adds a new bid to the Bid table with the specified initial bid, minimum step, credits listed, and company ID.

        Args:
            initial_bid (float): The initial bid amount.
            min_step (float): The minimum step for bidding.
            credits (int): The number of credits listed in the bid.
            ticker (str): The ticker symbol of the company associated with the bid.

        Returns:
            bool: True if the bid is added successfully, False otherwise.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_listed_credit_to_bid(initial_bid, min_step, credits, ticker)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error adding listed credit to bid for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_industry_keyword_from_companySignup_ticker(self,ticker):
        """
        Retrieves the industry keyword associated with the company identified by the ticker symbol.

        Args:
            ticker (str): The ticker symbol of the company.

        Returns:
            str: The industry keyword associated with the company.
        """
        return self.company_dao.get_industry_keyword_from_companySignup_ticker(ticker)
    
    def return_wallet_balance_from_companySignup_ticker(self,ticker):
        """
        Retrieves the credits wallet balance for a company with the specified ticker.

        Args:
            ticker (str): The ticker symbol of the company.

        Returns:
            float: The credits wallet balance of the company.
        """
        return self.company_dao.get_wallet_balance_from_companySignup_ticker(ticker)
    
    def add_credits_wallet_balance_from_companySignup_ticker(self, ticker, updated_wallet_balance):
        """
        Updates the credits wallet balance for a company with the specified ticker.

        Args:
            ticker (str): The ticker symbol of the company.
            updated_wallet_balance (float): The updated credits wallet balance.

        Returns:
            bool: True if the credits wallet balance is successfully updated, False otherwise.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_credits_wallet_balance_from_companySignup_ticker(ticker, updated_wallet_balance)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error adding credits wallet balance for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_listings_for_auction(self):
        """
        Retrieves all the listings for auction.

        Returns:
            list: A list of tuples containing auction listings.
        """
        return self.company_dao.get_listings_for_auction()
    
    def return_my_biddings(self):
        """
        Retrieves all the bidding details.

        Returns:
            list: A list of tuples containing bidding details.
        """
        return self.company_dao.get_my_biddings()
    
    def return_insert_into_bidding_table(self,bidder, bidID, bid):
        """
        Inserts a bid into the Bidding table.

        Args:
            bidder (str): The name of the bidder.
            bidID (int): The ID of the bid.
            bid (float): The bid amount.

        Returns:
            bool: True if the insertion is successful, False otherwise.

        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.insert_into_bidding_table(bidder, bidID, bid)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error adding to bidding table: {e}")
            return False  # Indicate failure

    def return_max_bidding_amount(self, ticker):
        """
        Retrieves the maximum bidding amount for a given ticker.

        Args:
            ticker (str): The ticker symbol of the company.

        Returns:
            list: A list containing the maximum bidding amount.

        """
        return self.company_dao.get_max_bidding_amount(ticker)
    
    def return_companyID_from_bidID(self, bidID):
        """
        Retrieves the companyID associated with a specific bidID.

        Args:
            bidID (int): The ID of the bid.

        Returns:
            list: A list containing the companyID associated with the given bidID.

        """
        return self.company_dao.get_companyID_from_bidID(bidID)
    
    def return_bidding_details_from_ticker(self, ticker):
        """
        Retrieves bidding details for a specific company.

        Args:
            ticker (str): The ticker symbol of the company.

        Returns:
            list: A list containing bidding details including bidder, bid amount, and bidID.

        """
        return self.company_dao.get_bidding_details_from_ticker(ticker)
    
    def return_credits_listed_from_bidID(self, bidID):
        """
        Retrieves the number of credits listed for a bid.

        Args:
            bidID (str): The ID of the bid.

        Returns:
            list: A list containing the number of credits listed for the bid.

        """
        return self.company_dao.get_credits_listed_from_bidID(bidID)
    
    def return_add_money_to_wallet(self,ticker,money):
        """
        Adds money to the money wallet balance of a company in the database.

        Args:
            ticker (str): Ticker symbol of the company.
            money (float): Amount of money to add to the money wallet balance.

        Returns:
            bool: True if the addition is successful, False otherwise.

        Raises:
            Exception: If an error occurs during addition.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_money_to_wallet(ticker,money)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error  adding to money wallet balance for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_add_credit_to_credit_wallet(self,ticker,cred_listed):
        """
        Adds credit to the credit wallet balance of a company in the database.

        Args:
            ticker (str): Ticker symbol of the company.
            cred_listed (float): Amount of credit to add to the credit wallet balance.

        Returns:
            bool: True if the addition is successful, False otherwise.

        Raises:
            Exception: If an error occurs during addition.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_credit_to_credit_wallet(ticker,cred_listed)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error adding credit to credit wallet balance for {ticker}: {e}")
            return False  # Indicate failure
    
    def return_subtract_money_from_wallet(self,ticker,money):
        """
        Subtracts money from the wallet balance of a company in the database.

        Args:
            ticker (str): Ticker symbol of the company.
            money (float): Amount of money to subtract from the wallet balance.

        Returns:
            bool: True if the subtraction is successful, False otherwise.

        Raises:
            Exception: If an error occurs during subtraction.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.subtract_money_from_wallet(ticker,money)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error subtracting money from wallet balance for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_remove_bid_from_bidID(self, bidID):
        """
        Removes a bid and its details from the database.

        Args:
            bidID (int): ID of the bid to remove.

        Returns:
            bool: True if the removal is successful, False otherwise.

        Raises:
            Exception: If an error occurs during removal.
        """
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.remove_bid_from_bidID( bidID)
            return True  # Indicate success
        except Exception as e:
            logger.error(f"Error removing for {bidID}: {e}")
            return False  # Indicate failure

class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao
    
    def add_user_details(self,username, name,password,age, country, gender):
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
        return self.user_dao.add_user_details(username,name,password,age, country, gender)
    
    def add_user_email(self,username, email):
        """
        Adds an email address for a user to the User_mail table in the database.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
        """
        return self.user_dao.add_user_email(username,email)

    def get_user_data_dict(self):
        """
        Retrieves user data from the database and organizes it into a dictionary.

        Returns:
            dict: A dictionary containing user data, with usernames as keys and corresponding information as values.
                Each user's information includes name, password, balance, age, country, gender, and email.
        """
        user_data, user_mail_data= self.user_dao.get_user_data()
        user_data_dict={}
        for row in user_data:
            username, balance, name, password, age, country, gender = row
            user_data_dict[username] = {
                'name': name,
                'password': password,
                'balance': float(balance),
                'age': age,
                'country': country,
                'gender': gender
            }
        for row in user_mail_data:
            username, email = row
            if username in user_data_dict:
                user_data_dict[username]['email'] = email

        user_data_dict= {'usernames': user_data_dict}
        return user_data_dict 
    
    def add_uploaded_file_to_current_portfolio(self,uploaded_file):
        """
        Processes an uploaded file containing portfolio transactions and adds them to the database.

        Args:
            uploaded_file (pandas.DataFrame): A pandas DataFrame containing the uploaded portfolio data.
        """
        return self.user_dao.add_uploaded_file_to_current_portfolio(uploaded_file)
    
    def buy_stock(self,username, quantity, company_id):
        """
        Buys a specified quantity of stock for a given company.

        Args:
            username (str): The username of the user making the purchase.
            quantity (int): The quantity of stock to be bought.
            company_id (str): The ID of the company for which the stock is being bought.

        Returns:
            None
        """
        user_wallet = self.get_wallet_balance(username)

        price_per_stock = self.user_dao.get_current_price_for_ticker(company_id)
        
        total_price = quantity*price_per_stock
        
        if total_price > user_wallet:
            st.warning(f"Not enough balance in your wallet. Current wallet balance: ${user_wallet}")
        else:
            user_wallet -= total_price
            st.success(f"Successfully bought {quantity} stocks of {st.session_state.get('company')} for ${total_price}.")
            st.write(f"Remaining balance in your wallet: ${user_wallet}")
            
            self.user_dao.update_wallet(user_wallet)
            self.user_dao.update_transaction_history(company_id,quantity,price_per_stock,"Buy")
            self.user_dao.update_portfolio(company_id,quantity,price_per_stock,"Buy")
    
    def sell_stock(self,user_shares, company_details, quantity):
        """
        Sells a specified quantity of stock for a given company.

        Args:
            user_shares (dict): A dictionary containing the user's current stock holdings.
            company_details (dict): A dictionary containing details of the company including name and price per stock.
            quantity (int): The quantity of stock to be sold.

        Returns:
            None
        """
        company_name = company_details['name']
        price_per_stock = company_details['price_per_stock']
        
        if company_name in user_shares:
            available_shares = user_shares[company_name]
            if quantity <= available_shares:
                total_price = quantity*price_per_stock
                user_shares[company_name] -= quantity
                st.success(f"Successfully sold {quantity} shares of {company_name} for ${total_price}.")
                st.write(f"Remaining shares of {company_name}: {user_shares[company_name]}")
                
                # update user wallet
                user_wallet = self.get_wallet_balance(st.session_state.get('username'))
                user_wallet = user_wallet+total_price
                self.user_dao.update_wallet(user_wallet)
                
                # update transaction history
                self.user_dao.update_transaction_history(company_name,quantity,price_per_stock,"Sell")
                
                # update portfolio
                self.user_dao.update_portfolio(company_name,quantity,price_per_stock,"Sell")
                
            else:
                st.warning("You don't have enough shares to sell.")
        else:
            st.warning("You don't own any shares of this company.")
    
    def get_mail(self,username):
        """
        Retrieves the email address of a user.

        Args:
            username (str): The username of the user
        Returns:
            str: The email address of the user, or None if not found.
        """
        return self.user_dao.get_mail(username)
    
    def get_wallet_balance(self,username):
        """
        Retrieves the current wallet balance of a user.

        Args:
            username (str): The username of the user.

        Returns:
            float: The current wallet balance of the user.
        """
        return self.user_dao.get_wallet_balance(username)
    
    def get_portfolio_entry_for_user(self,username):
        """
        Retrieves all portfolio entries for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            pandas.DataFrame: A DataFrame containing the user's portfolio data.
        """
        return self.user_dao.get_portfolio_entry_for_user(username)
    
    def get_name_from_username(self,username):
        """
        Retrieves the full name of a user.

        Args:
            username (str): The username of the user.

        Returns:
            str: The full name of the user, or None if not found.
        """
        return self.user_dao.get_name_from_username(username)
    
    def calculate_portfolio_score(self,data=None):
        """
        Calculates the score of the portfolio based on transaction data and company scores.

        Args:
            data (pandas.DataFrame, optional): Transaction data containing information about each transaction.
                Defaults to None.

        Returns:
            tuple: A tuple containing the following elements:
                - float: The calculated portfolio score.
                - pandas.DataFrame: The transaction data DataFrame with an additional column 'Score' appended.
        """
        # Initialize portfolio score
        portfolio_score = []
        current_score = 0
        scoreData= self.user_dao.get_score_history_of_all_companies()
        df = pd.DataFrame(scoreData, columns=['tickers', 'score', 'Date'])
        start_date = '2023-01-01'
        end_date = dt.today().strftime('%Y-%m-%d')
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        df = df.pivot(index='Date', columns='tickers', values='score')
        df.fillna(method='ffill',inplace=True)
        df = df.fillna(0)
        df = df.reindex(date_range)
        df.fillna(method='ffill',inplace=True)
        df = df.fillna(0)
        current_score = 0
        logger.info(df)
        tickers = df.columns.to_numpy()
        stocks = {ticker: 0 for ticker in tickers}
        
        for index, row in data.iterrows():
            string_timestamp = row['Date'].strftime('%Y-%m-%d')
            converted_timestamp = pd.Timestamp(string_timestamp)
            if row['Order Type'] == 'Buy':
                stocks[row['Ticker']]+=float(row['Amount'])
                if stocks[row['Ticker']] != 0:
                    current_score += (float(row['Amount'])/stocks[row['Ticker']]) * float(df.loc[converted_timestamp][row['Ticker']])
            elif row['Order Type'] == 'Sell':
                if stocks[row['Ticker']] != 0:
                    current_score -= (float(row['Amount'])/stocks[row['Ticker']]) * float(df.loc[converted_timestamp][row['Ticker']])
                    stocks[row['Ticker']]-=float(row['Amount'])
                    
                
            if len((portfolio_score))!=0:
                portfolio_score.append(current_score/len(portfolio_score))
            else:
                portfolio_score.append(current_score)

        data['Score'] = portfolio_score
        if len((portfolio_score))!=0:
            return current_score/len(portfolio_score), data 
        else:
            return current_score, data 
    
    
    def calculate_portfolio_balance(self,data):
        """
        Calculates the balance and value of the portfolio based on transaction data.

        Args:
            data (pandas.DataFrame): Transaction data containing information about each transaction.

        Returns:
            tuple: A tuple containing the following elements:
                - dict: A dictionary where keys are ticker symbols and values are the number of shares held.
                - dict: A dictionary where keys are ticker symbols and values are the current value of shares held.
                - float: The current total portfolio balance.
                - float: The current total portfolio value.
                - pandas.DataFrame: The transaction data DataFrame with additional columns 'Invested Amount' 
                and 'Portfolio Value' appended.
        """
        current_portfolio = 0
        portfolio_amount = []
        portfolio_value = []
        start_date = '2023-01-01'
        end_date = dt.today().strftime('%Y-%m-%d')
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')

        priceData = self.user_dao.get_price_history_of_all_companies()
        df = pd.DataFrame(priceData, columns=['tickers', 'price', 'dates'])
        df['Date']=pd.to_datetime(df['dates'])
        df = df.pivot(index="Date", columns="tickers", values="price")
        df.fillna(method='ffill', inplace=True)
        df=df.fillna(0)
        df = df.reindex(date_range)
        df.fillna(method='ffill',inplace=True)
        df = df.fillna(0)
        
        tickers = df.columns.to_list()

        stocks = {ticker: 0 for ticker in tickers}
        shares = {ticker: 0 for ticker in tickers}
        

        for index, row in data.iterrows():
            current_value=0
            if row['Order Type'] == 'Buy':
                current_portfolio += row['Amount'] * row['Price/Quote']
                shares[row['Ticker']]+=row['Amount']
            elif row['Order Type'] == 'Sell':
                current_portfolio -= row['Amount'] * row['Price/Quote']
                shares[row['Ticker']]-=row['Amount']
            for ticker, value in shares.items():
                current_value += float(value) * float(df.loc[row['Date']][ticker])
            portfolio_amount.append(current_portfolio)
            portfolio_value.append(current_value)

        # Add 'Portfolio Amount' column to DataFrame
        data['Invested Amount'] = portfolio_amount
        data['Portfolio Value'] = portfolio_value 
                
        for ticker, amount in shares.items():
            y = df.iloc[-1][ticker]
            y = float(y)
            amount = float(amount)
            stocks[ticker]=amount*y
        

        return shares,stocks, current_portfolio, current_value,data
    
    def get_transaction_history(self,username):
        """
        Retrieves the transaction history for a specific user.

        Args:
            username (str): The username of the user.

        Returns:
            pandas.DataFrame: A DataFrame containing the user's transaction history data.
        """
        return self.user_dao.get_transaction_history(username)
    
    def get_continent_from_country(self,country_name):
        """
        Retrieves the continent name based on the given country name.

        Args:
            country_name (str): The name of the country.

        Returns:
            str: The name of the continent to which the country belongs.
        """
        country_name=string.capwords(country_name, ' ')
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
        
        
    def get_user_data_frame_for_insights(self):
        """
        Retrieves user data for the insights page.

        Returns:
            pandas.DataFrame: A DataFrame containing user data such as username, investment type, asset type, age, gender,
            country, and continent for insights.
        """

        result= self.user_dao.get_user_name_ticker_from_portfolio()
        df=pd.DataFrame(result,columns=["username","Ticker"])
        df['investment_type'] = df['Ticker'].apply(self.user_dao.get_fund_category_from_ticker).apply(lambda x: x[0][0])
        df['asset_type']= df['Ticker'].apply(self.user_dao.get_industry_keyword_from_companyID).apply(lambda x: x[0][0])
        df['age']=df['username'].apply(self.user_dao.get_age_from_username)
        df['gender']= df['username'].apply(self.user_dao.get_gender_from_username)
        df['country']= df['username'].apply(self.user_dao.get_country_from_username)
        df['continent']=df['country'].apply(self.get_continent_from_country)
        logger.info(df)
        return df
    
    def get_time_frequency_of_user(self):
        """
        Calculates the frequency of transactions made by a user over time.

        Returns:
            pandas.DataFrame: A DataFrame containing the date and number of transactions for each date.
        """
        return self.user_dao.get_time_frequency_of_user()
    
    def get_date_amount_for_avg_insights(self):
        """
        Retrieve dates and transaction amounts for calculating average investment insights.

        Returns:
            pandas.DataFrame: A DataFrame containing the date and transaction amount for each transaction.
        """
        return self.user_dao.get_date_amount_for_avg_insights()

    def get_portfolio_score_for_each_user(self):
        """
        Calculate the portfolio score for each user.

        Returns:
            pandas.DataFrame: A DataFrame containing the username and portfolio score for each user.
        """
        usernames = self.user_dao.get_usernames()

        df = pd.DataFrame(columns=['Username', 'Portfolio Score'])
    
        # Iterate over usernames
        for username in usernames:
            # Get portfolio for the user
            portfolio = self.get_portfolio_entry_for_user(username)
        
            # Calculate portfolio score
            score, _ = self.calculate_portfolio_score(portfolio)
            
            # Append username and score to result DataFrame
            df = df._append({'Username': username, 'Portfolio Score': score}, ignore_index=True)
        
        return df

        
        
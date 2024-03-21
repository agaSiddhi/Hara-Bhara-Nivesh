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
class CompanyService():
    def __init__(self, company_dao):
        self.company_dao = company_dao
    
    def return_company_name_and_description(self):
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
        return self.company_dao.get_companyID_from_company_name(company_name=companyName)

    def return_company_details_from_companyID(self,companyID=None):
        return self.company_dao.get_company_details_from_companyID(companyID=companyID)
    
    def return_ESG_score_from_companyID(self,companyID=None):
        return self.company_dao.get_ESG_score_from_companyID(companyID=companyID)

    def return_industry_description_from_companyID(self,companyID=None):
        return self.company_dao.get_industry_description_from_companyID(companyID=companyID)

    def return_score_history_from_companyID(self,companyID=None):
        return self.company_dao.get_score_history_from_companyID(companyID=companyID)

    def return_price_history_from_companyID(self,companyID=None):
        return self.company_dao.get_price_history_from_companyID(companyID=companyID)

    def return_category_percentage(self,stocks=None):
    # Calculate the percentage of each category
        total_stocks = sum(stocks.values())
        category_percentage = {'Equity': 0, 'Debt': 0, 'Hybrid': 0, 'Others': 0}
        for ticker, amount in stocks.items():
            category= self.company_dao.get_fund_category_from_ticker(ticker)
            category_percentage[category[0][0]] += amount / total_stocks
        return category_percentage

    def return_industry_percentage(self,stocks=None):
        total_stocks = sum(stocks.values())
        # Calculate the percentage of each industry
        industry_percentage = {'Capital Goods': 0, 'Financial': 0, 'Services': 0, 'HealthCare': 0, 'Consumer Staples':0, 'Other':0}
        for ticker, amount in stocks.items():
            industry = self.company_dao.get_industry_keyword_from_companyID(ticker)
            industry_percentage[industry[0][0]] += amount / total_stocks
        return industry_percentage
    
    def calculate_portfolio_balance(self,data=None):
        return self.company_dao.calculate_portfolio_balance(data=data)

    def calculate_portfolio_score(self,data=None):
        return self.company_dao.calculate_portfolio_score(data=data)
    
    def return_companies_for_fund_category(self):
        return self.company_dao.get_companies_for_fund_category()
    
    def return_companies_for_industry_category(self):
        return self.company_dao.get_companies_for_industry_category()
    
    def return_company_name_from_ticker(self):
        return self.company_dao.get_company_name_from_ticker()
    
    def return_industry_from_ticker(self,companyID=None):
        return self.company_dao.get_industry(companyID)
    
    def return_fund_category_from_ticker(self,companyID=None):
        return self.company_dao.get_fund_category_from_ticker(companyID)
    
    def return_average_score_from_ticker(self,companyID=None):
         return self.company_dao.get_average_score_from_ticker(companyID)
     
    def return_companies(self,stocks,category):
        companies = []
        
        for ticker, amount in stocks.items():
            if not ticker:
                break
            fund_category=self.company_dao.get_fund_category_from_ticker(ticker)
            if category == fund_category[0][0]:
                companies.append({ticker: amount})
        return companies

    def return_ticker_percentages(self,companies):
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
        return self.company_dao.get_company_details_for_credits()
    
    def carry_over(self,score_data,field):
        
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
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.update_wallet_balance(ticker, updated_wallet_balance)
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating wallet balance for {ticker}: {e}")
            return False  # Indicate failure
    
    def return_industry_keyword_from_companyID(self,companyID=None):
        return self.company_dao.get_industry_keyword_from_companyID(companyID=companyID)
    

    def return_wallet_balance_from_companyID(self,companyID=None):
        return self.company_dao.get_wallet_balance_from_companyID(companyID=companyID)
    
    def return_add_new_company(self, ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category):
        try:
            # Call the DAO method to insert the new company into the database
            self.company_dao.add_new_company(ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category)
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding new company: {e}")
            return False  # Indicate failure

    def return_industry_id_by_keyword(self, industry_keyword):
        return self.company_dao.get_industry_id_by_keyword(industry_keyword)
    
    def return_companies_by_industry(self,stocks,industry):
        return self.company_dao.get_companies_by_industry(stocks,industry)

    def filter_companies(self,selected_categories, selected_sectors):
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
        industryID = self.return_industry_id_by_keyword(industry)[0][0]
        # print(industryID)
        try:
            # Call the DAO method to insert the new company into the database
            self.company_dao.add_company_signup_details(company_name,company_ticker,password,initial_money_wallet_balance,initial_credits_wallet_balance,industryID,fund_category)
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding new company: {e}")
            return False  # Indicate failure
    
    def get_company_data_dict(self):
        query = '''SELECT * FROM CompanySignup;'''
        company_data = self.execute_query(query)

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
        return self.company_dao.get_signup_company_data(name)
    
    def return_update_credit_wallet_balance(self, ticker, credits):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.update_credit_wallet_balance(ticker, credits)
            return True  # Indicate success
        except Exception as e:
            print(f"Error updating credit wallet balance for {ticker}: {e}")
            return False  # Indicate failure

    def add_listed_credit_to_bid(self, initial_bid, min_step, credits, ticker):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_listed_credit_to_bid(initial_bid, min_step, credits, ticker)
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding listed credit to bid for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_industry_keyword_from_companySignup_ticker(self,ticker):
        return self.company_dao.get_industry_keyword_from_companySignup_ticker(ticker)
    
    def return_wallet_balance_from_companySignup_ticker(self,ticker):
        return self.company_dao.get_wallet_balance_from_companySignup_ticker(ticker)
    
    def add_credits_wallet_balance_from_companySignup_ticker(self, ticker, updated_wallet_balance):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_credits_wallet_balance_from_companySignup_ticker(ticker, updated_wallet_balance)
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding credits wallet balance for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_listings_for_auction(self):
        return self.company_dao.get_listings_for_auction()
    
    def return_my_biddings(self):
        return self.company_dao.get_my_biddings()
    
    def return_insert_into_bidding_table(self,bidder, bidID, bid):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.insert_into_bidding_table(bidder, bidID, bid)
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding to bidding table: {e}")
            return False  # Indicate failure

    def return_max_bidding_amount(self, ticker):
        return self.company_dao.get_max_bidding_amount(ticker)
    
    def return_companyID_from_bidID(self, bidID):
        return self.company_dao.get_companyID_from_bidID(bidID)
    
    def return_bidding_details_from_ticker(self, ticker):
        return self.company_dao.get_bidding_details_from_ticker(ticker)
    
    def return_credits_listed_from_bidID(self, bidID):
        return self.company_dao.get_credits_listed_from_bidID(bidID)
    
    def return_add_money_to_wallet(self,ticker,money):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_money_to_wallet(ticker,money)
            return True  # Indicate success
        except Exception as e:
            print(f"Error  adding to money wallet balance for {ticker}: {e}")
            return False  # Indicate failure
    def return_add_credit_to_credit_wallet(self,ticker,cred_listed):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.add_credit_to_credit_wallet(ticker,cred_listed)
            return True  # Indicate success
        except Exception as e:
            print(f"Error adding credit to credit wallet balance for {ticker}: {e}")
            return False  # Indicate failure
    
    def return_subtract_money_from_wallet(self,ticker,money):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.subtract_money_from_wallet(ticker,money)
            return True  # Indicate success
        except Exception as e:
            print(f"Error subtracting money from wallet balance for {ticker}: {e}")
            return False  # Indicate failure
        
    def return_remove_bid_from_bidID(self, bidID):
        try:
            # Call the DAO method to update the wallet balance in the database
            self.company_dao.remove_bid_from_bidID( bidID)
            return True  # Indicate success
        except Exception as e:
            print(f"Error removing for {bidID}: {e}")
            return False  # Indicate failure

class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao
    
    def add_user_details(self,username, name,password,age, country, gender):
        return self.user_dao.add_user_details(username,name,password,age, country, gender)
    
    def add_user_email(self,username, email):
        return self.user_dao.add_user_email(username,email)

    def get_user_data_dict(self):
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
        return self.user_dao.add_uploaded_file_to_current_portfolio(uploaded_file)
    
    def buy_stock(self,username, quantity, company_id):
        user_wallet = self.get_wallet_balance(username)

        price_per_stock = self.get_current_price_for_ticker(company_id)
        
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
    
    def get_current_price_for_ticker(self,company_id):
        return self.user_dao.get_current_price_for_ticker(company_id)
    
    def get_mail(self,username):
        return self.user_dao.get_mail(username)
    
    def get_wallet_balance(self,username):
        return self.user_dao.get_wallet_balance(username)
    
    def get_portfolio_entry_for_user(self,username):
        return self.user_dao.get_portfolio_entry_for_user(username)
    
    def get_name_from_username(self,username):
        return self.user_dao.get_name_from_username(username)
    
    def calculate_portfolio_score(self,data=None):
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
        
        tickers = df.columns.to_numpy()
        stocks = {ticker: 0 for ticker in tickers}
        
        for index, row in data.iterrows():
            
            if row['Order Type'] == 'Buy':
                stocks[row['Ticker']]+=float(row['Amount'])
                current_score += (float(row['Amount'])/stocks[row['Ticker']]) * float(df.loc[row['Date']][row['Ticker']])
            elif row['Order Type'] == 'Sell':
                stocks[row['Ticker']]-=float(row['Amount'])
                current_score -= (float(row['Amount'])/stocks[row['Ticker']]) * float(df.loc[row['Date']][row['Ticker']])
                
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
        return self.user_dao.get_transaction_history(username)
    
    def get_continent_from_country(self,country_name):
        country_name=string.capwords(country_name, ' ')
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
        
        
    def get_user_data_frame_for_insights(self):
        result= self.user_dao.get_user_name_ticker_from_portfolio()
        df=pd.DataFrame(result,columns=["username","Ticker"])
        df['investment_type'] = df['Ticker'].apply(self.user_dao.get_fund_category_from_ticker).apply(lambda x: x[0][0])
        df['asset_type']= df['Ticker'].apply(self.user_dao.get_industry_keyword_from_companyID).apply(lambda x: x[0][0])
        df['age']=df['username'].apply(self.user_dao.get_age_from_username)
        df['gender']= df['username'].apply(self.user_dao.get_gender_from_username)
        df['country']= df['username'].apply(self.user_dao.get_country_from_username)
        df['continent']=df['country'].apply(self.get_continent_from_country)
        print(df)
        return df
    
    def get_time_frequency_of_user(self):
        return self.user_dao.get_time_frequency_of_user()
    
    def get_date_amount_for_avg_insights(self):
        return self.user_dao.get_date_amount_for_avg_insights()
        
        
import mysql.connector
# from backend.database import return_price_and_date, return_score_and_date
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime as dt
from backend.dao.dao import CompanyDao


class UserDao(CompanyDao):
    def __init__(self, host, user, password, database,port):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port = port
        )
        
    def execute_query(self, query, params=None):
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
    
    def add_user_details(self,username,name,password,age,country,gender):
        query= f'''INSERT INTO User (username, name, password, balance, age, country, gender) VALUES ("{username}", "{name}", "{password}", {10000}, "{age}", "{country}", "{gender}");'''
        self.execute_query(query)
        
    def add_user_email(self,username,email):
        query=f'''INSERT INTO User_mail (username, email) VALUES ("{username}", "{email}");'''
        self.execute_query(query)
        
    def get_user_data_dict(self):
        query='''SELECT * FROM User;'''
        user_data= self.execute_query(query)

        
        query= '''SELECT * FROM User_mail;'''

        user_mail_data=self.execute_query(query)
        
        
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
        for _, row in uploaded_file.iterrows():
          
            
            query = f'''
                INSERT INTO Portfolio_entry (date, order_type, Ticker, amount, price_quote,username)
                VALUES ("{row['Date'].strftime('%Y-%m-%d')}","{row['Order Type']}", "{row['Ticker']}", {float(row['Amount'])}, {float(row['Price/Quote'])}, "{st.session_state.get('username')}");
            '''
      
            self.execute_query(query)
    
    def get_wallet_balance(self,username):
        query=f'''SELECT balance
                FROM User
                WHERE username = "{username}";'''
        result=self.execute_query(query)

        return result[0][0]
            
    def update_transaction_history(self,company_id,quantity,price_per_stock,order_type):
    # update user transaction history
        today_date = dt.today()
        today_date_str = today_date.strftime('%Y-%m-%d')
        
        query=f'''INSERT INTO Transaction_history (order_type, date, amount, ticker, username, price_quote) 
        VALUES ("{order_type}","{today_date_str}",{quantity},"{company_id}","{st.session_state.get('username')}",{price_per_stock});'''
        self.execute_query(query)
    
    def update_portfolio(self,company_id,quantity,price_per_stock,order_type):
        today_date = dt.today()
        today_date_str = today_date.strftime('%Y-%m-%d')
        # update user transaction history)
        query=f'''INSERT INTO Portfolio_entry (order_type, date, amount, ticker, username, price_quote) 
        VALUES ("{order_type}","{today_date_str}",{quantity},"{company_id}","{st.session_state.get('username')}",{price_per_stock});'''
        self.execute_query(query)

    def get_current_price_for_ticker(self,company_id):
        query=f'''SELECT price
            FROM PriceHistory
            WHERE companyID = "{company_id}"
            ORDER BY updatedAt DESC
            LIMIT 1;'''
        result=self.execute_query(query)
        return result[0][0]
 
    def update_wallet(self,user_wallet):
        query=f'''UPDATE User
                 SET balance = {user_wallet}
                 WHERE username = "{st.session_state.get('username')}"; '''
        self.execute_query(query)       
    
    def get_mail(self,username):
        query=f'''SELECT email from User_mail
                WHERE username="{username}";'''
        result=self.execute_query(query)
        return result[0][0]
        
    # Function to handle the buy functionality
    def buy_stock(self,username, quantity, company_id):
        user_wallet = self.get_wallet_balance(username)

        price_per_stock = self.get_current_price_for_ticker(company_id)
        
        total_price = quantity*price_per_stock
        
        if total_price > user_wallet:
            st.warning("Not enough balance in your wallet. Current wallet balance: ${user_wallet}")
        else:
            user_wallet -= total_price
            st.success(f"Successfully bought {quantity} stocks of {st.session_state.get('company')} for ${total_price}.")
            st.write(f"Remaining balance in your wallet: ${user_wallet}")
            
            self.update_wallet(user_wallet)
            self.update_transaction_history(company_id,quantity,price_per_stock,"Buy")
            self.update_portfolio(company_id,quantity,price_per_stock,"Buy")
    
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
                self.update_wallet(user_wallet)
                
                # update transaction history
                self.update_transaction_history(company_name,quantity,price_per_stock,"Sell")
                
                # update portfolio
                self.update_portfolio(company_name,quantity,price_per_stock,"Sell")
                
            else:
                st.warning("You don't have enough shares to sell.")
        else:
            st.warning("You don't own any shares of this company.")
    
    def get_portfolio_entry_for_user(self,username):
        query = f'''SELECT amount, date, order_type, price_quote, Ticker
            FROM Portfolio_entry WHERE username="{username}"; '''
        result=self.execute_query(query)
        df = pd.DataFrame(result, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"])
        df = df.sort_values(by='Date')

        return df
    
    def get_name_from_username(self,username):
        query=f'''SELECT name FROM User WHERE username="{username}";'''
        result=self.execute_query(query)
    

    
    def calculate_portfolio_balance(self,data):
        current_portfolio = 0
        
        start_date = '2023-01-01'
        end_date = dt.today().strftime('%Y-%m-%d')
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        query = f'''SELECT companyID, price, updatedAt
                FROM PriceHistory;'''
        priceData = self.execute_query(query)
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
                
        for ticker, amount in shares.items():
            y = df.iloc[-1][ticker]
            y = float(y)
            amount = float(amount)
            stocks[ticker]=amount*y

        return shares,stocks, current_portfolio, current_value
    
    def get_transaction_history(self,username):
        query = f'''
        SELECT amount, date, order_type, price_quote, Ticker
        FROM Transaction_history
        WHERE username = '{username}';'''
        result= self.execute_query(query)
        df = pd.DataFrame(result, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"])
        df = df.sort_values(by='Date')
        return df
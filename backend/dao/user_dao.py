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
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            # port = port
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
        
    def get_user_data(self):
        query='''SELECT * FROM User;'''
        user_data= self.execute_query(query)
        query= '''SELECT * FROM User_mail;'''
        user_mail_data=self.execute_query(query)
        return user_data,user_mail_data
    
    def get_user_name_ticker_from_portfolio(self):
        query = f'''
        SELECT username, Ticker
        FROM Portfolio_entry;'''
        result=self.execute_query(query)
        return result
    
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
    
    def get_transaction_history(self,username):
        query = f'''
        SELECT amount, date, order_type, price_quote, Ticker
        FROM Transaction_history
        WHERE username = '{username}';'''
        result= self.execute_query(query)
        df = pd.DataFrame(result, columns=["Amount", "Date", "Order Type", "Price/Quote", "Ticker"])
        df = df.sort_values(by='Date')
        return df
    
    def get_age_from_username(self,username):
        query=f'''SELECT age from User
                WHERE username="{username}";'''
        result=self.execute_query(query)
        return result[0][0]
    
    def get_gender_from_username(self,username):
        query=f'''SELECT gender from User
                WHERE username="{username}";'''
        result=self.execute_query(query)
        return result[0][0]
    
    def get_country_from_username(self,username):
        query=f'''SELECT country from User
                WHERE username="{username}";'''
        result=self.execute_query(query)
        return result[0][0]
    
    def get_time_frequency_of_user(self):
        query = f'''SELECT date, COUNT(transactionID) AS num_transactions
                    FROM Transaction_history
                    GROUP BY date;'''
        result=self.execute_query(query)
        df = pd.DataFrame(result, columns=['date', 'num_transactions'])
        print("time distribution",df)
        return df
    
    def get_date_amount_for_avg_insights(self):
        query = f'''SELECT date, amount FROM Transaction_history;'''
        result=self.execute_query(query)
        df = pd.DataFrame(result, columns=['date', 'amount'])
        print("amount distribution",df)
        return df
    


        
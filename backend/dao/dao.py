import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from datetime import datetime as dt

class CompanyDao:
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
    
    def get_industry_descriptions(self):
        query = "SELECT industryID, description FROM Industry;"
        results = self.execute_query(query)
        descriptions = {}
        for row in results:
            descriptions[row[0]] = row[1]
        return descriptions
    
    def get_company_name_and_description(self):
        query = "SELECT name,currentScore, (SELECT description FROM Industry WHERE Company.industryID = Industry.industryID)  FROM Company ORDER BY currentScore DESC;"
        results = self.execute_query(query)
        return results
    
    def get_companyID_from_company_name(self,company_name=None):
        
        query = f'SELECT companyID FROM Company WHERE name = "{company_name}";'
        result = self.execute_query(query)
        
        return result
    
    def get_ESG_score_from_companyID(self,companyID):
        query = f'''SELECT c.Environmental, c.Social , c.Governance
                FROM ESG c WHERE c.companyID = {f"'{companyID}'"};'''
        try:
            result = self.execute_query(query)
            return result
        except Exception as e:
            print(e)
    
        

    def get_company_details_from_companyID(self, companyID):
        query = f'''SELECT c.companyID, c.name AS companyName, c.createdAt, c.updatedAt, c.totalAssets, c.revenue, c.employeeCount, c.currentScore, c.foundedYear, w.url 
                FROM Company c 
                LEFT JOIN CompanyWebsite w ON c.companyID = w.companyID WHERE c.companyID = {f"'{companyID}'"};'''
        try:
            result = self.execute_query(query)
        except Exception as e:
            print(e)
        return result
    
    def get_industry_description_from_companyID(self,companyID=None):
        query = f''' SELECT i.description
                FROM Company c
                JOIN Industry i ON c.industryID = i.industryID
                WHERE c.companyID = "{companyID}"; '''
        result = self.execute_query(query)
        return result
    
    def get_price_history_from_companyID(self, companyID=None):
        query = f'''SELECT price, updatedAt
                FROM PriceHistory
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result
        

    def get_score_history_from_companyID(self, companyID=None):
        query = f'''SELECT score, updatedAt
                FROM ScoreHistory
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result
    
    def get_fund_category_from_ticker(self,companyID=None):
        query = f'''SELECT fundCategory
                FROM Company
                WHERE companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result
    
    def get_industry(self, companyID=None):
        query = f'''SELECT Industry.description
                FROM Company
                JOIN Industry ON Company.industryID = Industry.industryID
                WHERE Company.companyID = "{companyID}";'''
        result = self.execute_query(query)
        return result[0][0]
   
    def get_score_history_of_all_companies(self):
        
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        scoreData = self.execute_query(query)
        return scoreData
    
    def get_price_history_of_all_companies(self,data=None):

        query = f'''SELECT companyID, price, updatedAt
                FROM PriceHistory;'''
        priceData = self.execute_query(query)
        return priceData

    def get_companies_for_fund_category(self):
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
        query=f'SELECT companyID, name  FROM Company;'
        result=self.execute_query(query)
        ticker_company_dict = {ticker: company_name for ticker, company_name in result}
        return ticker_company_dict
        
    def get_average_score_from_ticker(self, companyID=None):

        if isinstance(companyID,list):
            companyID=companyID[0]

        query=f'SELECT AVG(score) FROM ScoreHistory WHERE companyID="{companyID}";'
        result=self.execute_query(query)

        return float(result[0][0])

    def get_companies(self,stocks,category):
        companies = []
        
        for ticker, amount in stocks.items():
            if not ticker:
                break
            fund_category=self.get_fund_category_from_ticker(ticker)
            if category == fund_category[0][0]:
                companies.append({ticker: amount})
        return companies

    def get_company_details_for_credits(self):
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
        query = f'''UPDATE Company SET wallet = {updated_wallet_balance} WHERE companyID = "{ticker}";'''
        try:
            self.execute_query(query)
            print(f"Wallet balance updated successfully for {ticker}")
        except Exception as e:
            print(f"Error updating wallet balance for {ticker}: {e}")
            raise
    
    def get_industry_keyword_from_companyID(self,companyID=None):
        query = f'''SELECT i.keyword
                FROM Company c
                JOIN Industry i ON c.industryID = i.industryID
                WHERE c.companyID = "{companyID}"; '''
        result = self.execute_query(query)

        return result

    def get_wallet_balance_from_companyID(self,companyID=None):
        query = f'''SELECT wallet
                FROM Company
                WHERE companyID = "{companyID}"; '''
        result = self.execute_query(query)

        return result
    
    def add_new_company(self, ticker, name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category):
        query = """
            INSERT INTO Company (companyID, name, createdAt, updatedAt, totalAssets, revenue, employeeCount, currentScore, foundedYear, industryID, fundCategory, wallet)
            VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, 0.00 , %s, %s, %s, 0.00)
        """
        # current_datetime = datetime.now()
        # created_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        # updated_at = created_at
        params = (ticker.upper(), name, total_assets, revenue, employee_count, founded_year, industry_id, fund_category)
        try:
            self.execute_query(query, params)
            print("New company added successfully.")
        except Exception as e:
            print(f"Error adding new company: {e}")
            raise

    def get_industry_id_by_keyword(self, industry_keyword):
        query = f'''SELECT industryID FROM Industry WHERE keyword = "{industry_keyword}";'''
        result = self.execute_query(query)

        return result
    
    def get_companies_by_industry(self,stocks,industry):
        companies = []
        for ticker, amount in stocks.items():
            print(ticker+"  "+str(amount)+"  "+industry)
            result= self.get_industry_keyword_from_companyID(ticker)
            if industry == result[0][0]:
                companies.append({ticker: amount})
        return companies
    
    def get_score_and_ticker_map(self):
        query=""" SELECT companyID, AVG(score) AS average_score
            FROM ScoreHistory
            GROUP BY companyID """
        result=self.execute_query(query)
        score_dict = {company_id: average_score for company_id, average_score in result}

        return score_dict
    
    def add_company_signup_details(self, company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance,industryID,fund_category):
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
        query = f'''SELECT * FROM CompanySignup WHERE CompanyTicker = '{name}';'''
        result = self.execute_query(query)
        return result
    
    def update_credit_wallet_balance(self, ticker, credits):
        query = f'''UPDATE CompanySignup
                    SET InitialCreditsWalletBalance = InitialCreditsWalletBalance - {credits}
                    WHERE CompanyTicker = '{ticker}';'''
        try:
            self.execute_query(query)
            print("updated credit wallet balance successfully.")
        except Exception as e:
            print(f"Error updating credit wallet balance : {e}")

    def add_listed_credit_to_bid(self, initial_bid, min_step, credits, ticker):
        query= f'''INSERT INTO Bid (initial_Bid, minimum_Step, credits_Listed, companyID)
                VALUES ({initial_bid}, {min_step}, {credits}, '{ticker}');'''
        try:
            self.execute_query(query)
            print("added listed credit to bid successfully")
        except Exception as e:
            print(f"Error adding listed credit to bid : {e}")

    def get_industry_keyword_from_companySignup_ticker(self,ticker):
        query = f'''SELECT i.keyword
                FROM CompanySignup cs
                JOIN Industry i ON cs.industryID = i.industryID
                WHERE cs.CompanyTicker = "{ticker}"; '''
        result = self.execute_query(query)

        return result
    
    def get_wallet_balance_from_companySignup_ticker(self,ticker):
        query = f'''SELECT InitialCreditsWalletBalance
                FROM CompanySignup
                WHERE CompanyTicker = "{ticker}"; '''
        result = self.execute_query(query)

        return result
    
    def add_credits_wallet_balance_from_companySignup_ticker(self, ticker, updated_wallet_balance):
        query = f'''UPDATE CompanySignup SET InitialCreditsWalletBalance = {updated_wallet_balance} WHERE CompanyTicker = "{ticker}";'''
        try:
            self.execute_query(query)
            print(f"Credits Wallet balance updated successfully for {ticker}")
        except Exception as e:
            print(f"Error updating credits wallet balance for {ticker}: {e}")
            raise

    def get_listings_for_auction(self):
        query = "SELECT * FROM Bid;"
        result = self.execute_query(query)
        return result

    def get_my_biddings(self):
        query = "SELECT * FROM Bidding;"
        result = self.execute_query(query)
        return result
    
    def insert_into_bidding_table(self,bidder, bidID, bid):
        query = f"""INSERT INTO Bidding (bidder, bidID, bid)
        VALUES ('{bidder}', {bidID}, {bid});"""
        try:
            self.execute_query(query)
            print("added to bidding table successfully")
        except Exception as e:
            print(f"Error adding to bidding table : {e}")

    def get_max_bidding_amount(self, ticker):
        query = f'''SELECT MAX(b.bid) AS max_bid
                    FROM Bidding b
                    JOIN Bid bd ON b.bidID = bd.bidID
                    WHERE bd.companyID = '{ticker}';'''
        result = self.execute_query(query)
        return result

    def get_companyID_from_bidID(self, bidID):
        query = f'''SELECT companyID AS cID
                    FROM Bid as bd
                    JOIN Bidding b on b.bidID = bd.bidID
                    WHERE b.bidID = '{bidID}';'''
        result = self.execute_query(query)
        return result
    
    def get_bidding_details_from_ticker(self, ticker):
        query = f'''SELECT b.bidder, b.bid, b.bidID
                    FROM Bidding as b
                    JOIN Bid bd on b.bidID = bd.bidID
                    WHERE bd.companyID = '{ticker}';'''
        result = self.execute_query(query)
        return result
    
    def get_credits_listed_from_bidID(self, bidID):
        query = f'''SELECT credits_Listed
                    FROM Bid
                    WHERE bidID = '{bidID}';'''
        result = self.execute_query(query)
        return result
    
    def add_money_to_wallet(self,ticker,money):
        query = f'''UPDATE CompanySignup
                    SET InitialMoneyWalletBalance = InitialMoneyWalletBalance + {money}
                    WHERE CompanyTicker = '{ticker}';'''
        try:
            self.execute_query(query)
            print("added to money wallet balance successfully")
        except Exception as e:
            print(f"Error adding to money wallet balance : {e}")

    def add_credit_to_credit_wallet(self,ticker,cred_listed):
        query = f'''UPDATE CompanySignup
                    SET InitialCreditsWalletBalance = InitialCreditsWalletBalance + {cred_listed}
                    WHERE CompanyTicker = '{ticker}';'''
        try:
            self.execute_query(query)
            print("added credit to credit balance successfully")
        except Exception as e:
            print(f"Error adding credit to credit wallet balance : {e}")

    def subtract_money_from_wallet(self,ticker,money):
        query = f'''UPDATE CompanySignup
                    SET InitialMoneyWalletBalance = InitialMoneyWalletBalance - {money}
                    WHERE CompanyTicker = '{ticker}';'''
        try:
            self.execute_query(query)
            print("subtracted money from wallet balance successfully")
        except Exception as e:
            print(f"Error subtracting money from wallet balance : {e}")

    def remove_bid_from_bidID(self, bidID):
        query = f'''DELETE B, BD
                    FROM Bidding B
                    JOIN Bid BD ON B.bidID = BD.bidID
                    WHERE B.bidID = {bidID};'''
        try:
            self.execute_query(query)
            print("removed successfully")
        except Exception as e:
            print(f"Error removing : {e}")
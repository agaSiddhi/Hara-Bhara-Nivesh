import mysql.connector
# from backend.database import return_price_and_date, return_score_and_date
import pandas as pd
import numpy as np
from datetime import datetime

class CompanyDao:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
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
        descriptions = {}
        rank = 1
        for row in results:
            # print(list(row[1:]))
            temp = list(row[1:])
            temp.append(rank)
            descriptions[row[0]] = temp
            rank += 1
            # print(descriptions)
        return descriptions
    
    def get_companyID_from_company_name(self,company_name=None):
        
        query = f'SELECT companyID FROM Company WHERE name = "{company_name}";'
        result = self.execute_query(query)
        
        return result

    def get_company_details_from_companyID(self, companyID):
        query = f'''SELECT c.companyID, c.name AS companyName, c.createdAt, c.updatedAt, c.totalAssets, c.revenue, c.employeeCount, c.currentScore, c.foundedYear, w.url 
                FROM Company c 
                LEFT JOIN CompanyWebsite w ON c.companyID = w.companyID WHERE c.companyID = {f"'{companyID}'"};'''
        try:
            result = self.execute_query(query)
        except Exception as e:
            print(e)
        
        # print(result)
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
    
    def get_category_percentage(self,stocks=None):
    # Calculate the percentage of each category
        total_stocks = sum(stocks.values())
        category_percentage = {'Equity': 0, 'Debt': 0, 'Hybrid': 0, 'Others': 0}
        for ticker, amount in stocks.items():
            query = f'''SELECT fundCategory
                FROM Company
                WHERE companyID = "{ticker}";'''
            category= self.execute_query(query)
            # print(category[0][0])
            category_percentage[category[0][0]] += amount / total_stocks
        return category_percentage
    
    def get_industry_percentage(self,stocks=None):
        total_stocks = sum(stocks.values())
        # Calculate the percentage of each industry
        industry_percentage = {'Capital Goods': 0, 'Financial': 0, 'Services': 0, 'HealthCare': 0, 'Consumer Staples':0, 'Other':0}
        for ticker, amount in stocks.items():
            query = f'''SELECT Industry.keyword
                    FROM Company
                    JOIN Industry ON Company.industryID = Industry.industryID
                    WHERE Company.companyID = "{ticker}";'''
            industry = self.execute_query(query)
            industry_percentage[industry[0][0]] += amount / total_stocks
        return industry_percentage
    
    def calculate_portfolio_score(self,data=None):
        # Initialize portfolio score
        portfolio_score = []
        current_score = 0
        
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        scoreData = self.execute_query(query)
        df = pd.DataFrame(scoreData, columns=['tickers', 'score', 'dates'])
        df['dates'] = pd.to_datetime(df['dates'])
        df = df.pivot(index='dates', columns='tickers', values='score')
        df = df.fillna(0)
        
        for index, row in data.iterrows():
            current_value = 0
            if row['Order Type'] == 'Buy':
                current_score += float(row['Amount']) * float(df.loc[row['Date']][row['Ticker']])
            elif row['Order Type'] == 'Sell':
                current_score -= float(row['Amount']) * float(df.loc[row['Date']][row['Ticker']])
            portfolio_score.append(current_score)

        data['Score'] = portfolio_score
        return current_score, data 
    
    
    def calculate_portfolio_balance(self,data=None):
        # Initialize portfolio balance
        query = f'''SELECT companyID, price, updatedAt
                FROM PriceHistory;'''
        priceData = self.execute_query(query)
        df = pd.DataFrame(priceData, columns=['tickers', 'price', 'dates'])
        df['dates'] = pd.to_datetime(df['dates'])
        df = df.pivot(index='dates', columns='tickers', values='price')
        df = df.fillna(0)
        
        portfolio_amount = []
        portfolio_value = []
        current_portfolio = 0
        
        # dates = pd.date_range(start=min(data['Date']), end=max(data['Date']))
        tickers = df.columns.to_numpy()
        stocks = {ticker: 0 for ticker in tickers}
        # prices = np.random.randint(100, 500, size=(len(dates), len(tickers)))  # Generating random prices -> this is something we ll get from the database

        # Create the DataFrame
        # df = pd.DataFrame(prices, index=dates, columns=tickers)

        for index, row in data.iterrows():
            current_value = 0
            if row['Order Type'] == 'Buy':
                current_portfolio += row['Amount'] * row['Price/Quote']
                stocks[row['Ticker']]+=row['Amount']
            elif row['Order Type'] == 'Sell':
                current_portfolio -= row['Amount'] * row['Price/Quote']
                stocks[row['Ticker']]-=row['Amount']
            for ticker, value in stocks.items():
                # print(type(value))
                # print(type(df.loc[row['Date']][ticker]))
                current_value += float(value) * float(df.loc[row['Date']][ticker])
            portfolio_amount.append(current_portfolio)
            portfolio_value.append(current_value)

        # Add 'Portfolio Amount' column to DataFrame
        data['Invested Amount'] = portfolio_amount
        data['Portfolio Value'] = portfolio_value 
        return stocks,data
    
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
            # print(result_dict)
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
                # print(result_dict)
            df = pd.DataFrame.from_dict(result_dict, orient='index').transpose()
            # print(result_dict)
            return result_dict
    
    def get_company_name_from_ticker(self):
        query=f'SELECT companyID, name  FROM Company;'
        result=self.execute_query(query)
        ticker_company_dict = {ticker: company_name for ticker, company_name in result}
        return ticker_company_dict
        
    def get_average_score_from_ticker(self, companyID=None):
        print(companyID)
        print(type(companyID))
        if isinstance(companyID,list):
            companyID=companyID[0]
        # print(companyID)
        query=f'SELECT AVG(score) FROM ScoreHistory WHERE companyID="{companyID}";'
        result=self.execute_query(query)
        # print(query)
        
        # print(result)
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

    def get_ticker_percentages(self,companies):
        # Getting composition of each ticker in out category
        # print(companies)
        total_amount = sum(amount for company in companies for amount in company.values())
        # print(total_amount)
        ticker_percentages = {}
        for company in companies:
            # print(company)
            for ticker, amount in company.items():
                # print(ticker)
                if not ticker:
                    break
                percentage = (amount / total_amount) 
                if percentage!=0:
                    ticker_percentages[ticker] = percentage
                    
        ticker_percentages = dict(sorted(ticker_percentages.items(), key=lambda item: item[1], reverse=True))
        return ticker_percentages
    

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
        # print(result)
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
        # print(result)
        return result

    def get_wallet_balance_from_companyID(self,companyID=None):
        query = f'''SELECT wallet
                FROM Company
                WHERE companyID = "{companyID}"; '''
        result = self.execute_query(query)
        # print(result)
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
        # print(result)
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
        print(score_dict)
        return score_dict

    def filter_companies(self,selected_categories, selected_sectors):
        data1=  self.get_companies_for_fund_category()
        data2= self.get_companies_for_industry_category()
        scores_dict=self.get_score_and_ticker_map()
        print(scores_dict)
        print(data1)
        print(data2)
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
    
    def add_company_signup_details(self, company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance):
        query = """
            INSERT INTO companysignup (CompanyName, CompanyTicker, Password, InitialMoneyWalletBalance, InitialCreditsWalletBalance)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (company_name, company_ticker, password, initial_money_wallet_balance, initial_credits_wallet_balance)
        try:
            self.execute_query(query, params)
            print("Company signup details added successfully.")
        except Exception as e:
            print(f"Error adding company signup details: {e}")



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
        
        print(result)
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
    
    def get_price_and_date(self):
        query = f'''SELECT companyID, price, updatedAt
                FROM PriceHistory;'''
        result = self.execute_query(query)
        return result
    
    def get_score_and_date(self):
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        result = self.execute_query(query)
        return result
    def get_fund_category_from_ticker(self,companyID=None):
        query = f'''SELECT companyID, score, updatedAt
                FROM ScoreHistory;'''
        result = self.execute_query(query)
        return result
    
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
        print(result)
        return result

    def get_wallet_balance_from_companyID(self,companyID=None):
        query = f'''SELECT wallet
                FROM Company
                WHERE companyID = "{companyID}"; '''
        result = self.execute_query(query)
        print(result)
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
        print(result)
        return result
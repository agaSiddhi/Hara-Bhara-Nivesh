class CompanyService:
    def __init__(self, company_dao):
        self.company_dao = company_dao
    
    def return_company_name_and_description(self):
        return self.company_dao.get_company_name_and_description()

    def return_companyID_from_company_name(self,companyName=None):
        return self.company_dao.get_companyID_from_company_name(company_name=companyName)

    def return_company_details_from_companyID(self,companyID=None):
        return self.company_dao.get_company_details_from_companyID(companyID=companyID)

    def return_industry_description_from_companyID(self,companyID=None):
        return self.company_dao.get_industry_description_from_companyID(companyID=companyID)

    def return_score_history_from_companyID(self,companyID=None):
        return self.company_dao.get_score_history_from_companyID(companyID=companyID)

    def return_price_history_from_companyID(self,companyID=None):
        return self.company_dao.get_price_history_from_companyID(companyID=companyID)

    def return_category_percentage(self,stocks=None):
        return self.company_dao.get_category_percentage(stocks=stocks)

    def return_industry_percentage(self,stocks=None):
        return self.company_dao.get_industry_percentage(stocks=stocks)
    
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
     
    def return_companies(self,stocks=None, category=None):
         return self.company_dao.get_companies(stocks, category)
    
    def return_ticker_percentages(self,companies=None):
         return self.company_dao.get_ticker_percentages(companies)
    
    def return_company_details_for_credits(self):
        return self.company_dao.get_company_details_for_credits()
    
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
        return self.company_dao.filter_companies(selected_categories,selected_sectors)      

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
        return self.company_dao.get_company_data_dict()
    
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
        return self.user_dao.get_user_data_dict()
    
    def add_uploaded_file_to_current_portfolio(self,uploaded_file):
        return self.user_dao.add_uploaded_file_to_current_portfolio(uploaded_file)
    
    def buy_stock(self,username, quantity, company_id):
        return self.user_dao.buy_stock(username,quantity,company_id)
    
    def get_current_price_for_ticker(self,company_id):
        return self.user_dao.get_current_price_for_ticker(company_id)
    
    def sell_stock(self,username, quantity, company_id):
        return self.user_dao.sell_stock(username,quantity,company_id)
    
    def get_mail(self,username):
        return self.user_dao.get_mail(username)
    
    def get_wallet_balance(self,username):
        return self.user_dao.get_wallet_balance(username)
    
    def get_portfolio_entry_for_user(self,username):
        return self.user_dao.get_portfolio_entry_for_user(username)
    
    def get_name_from_username(self,username):
        return self.user_dao.get_name_from_username(username)
    
    def calculate_portfolio_balance(self,data):
        return self.user_dao.calculate_portfolio_balance(data)
    
    def get_transaction_history(self,username):
        return self.user_dao.get_transaction_history(username)
        
        
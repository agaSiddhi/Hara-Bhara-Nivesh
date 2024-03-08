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

    def return_price_and_date(self):
        return self.company_dao.get_price_and_date()

    def return_score_and_date(self):
        return self.company_dao.get_score_and_date()
    
    def return_fund_category_from_ticker(self,companyID=None):
        return self.return_companyID_from_company_name(companyID=companyID)
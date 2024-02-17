import pandas as pd 
import mysql.connector
from backend.ConfigLoader import ConfigLoader
from backend.DatabaseConnector import DatabaseConnector
from backend.DatabaseQueries import QueryRunner
import os


filepath= f"{os.path.dirname(__file__)}/config.ini"
config_loader = ConfigLoader(filepath)  
connector = DatabaseConnector(config_loader)

connection = connector.connect()

QueryObject = QueryRunner(connection)

def return_company_name_and_description():
    return QueryObject.get_company_name_and_description()

def return_companyID_from_company_name(companyName=None):
    return QueryObject.get_companyID_from_company_name(company_name=companyName)

def return_company_details_from_companyID(companyID=None):
    return QueryObject.get_company_details_from_companyID(companyID=companyID)

def return_industry_description_from_companyID(companyID=None):
    return QueryObject.get_industry_description_from_companyID(companyID=companyID)

def return_score_history_from_companyID(companyID=None):
    return QueryObject.get_score_history_from_companyID(companyID=companyID)

def return_price_history_from_companyID(companyID=None):
    return QueryObject.get_price_history_from_companyID(companyID=companyID)

# print(return_company_details_from_companyID(1))
# list_industries_with_details()
# connector.disconnect()


def read_company_data():
    company_data=pd.read_csv("/home/agasiddhi/Documents/desis/project/DesisSG-2/backend/ListOfCompanies.csv")
    json_data= company_data.to_json( orient='records')
    return json_data


    





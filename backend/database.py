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

print(QueryObject.get_industry_descriptions())

connector.disconnect()



def read_company_data():
    company_data=pd.read_csv("/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/backend/ListOfCompanies.csv")
    json_data= company_data.to_json( orient='records')
    return json_data


    





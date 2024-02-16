import pandas as pd


def read_company_data():
    company_data=pd.read_csv("/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/backend/ListOfCompanies.csv")
    json_data= company_data.to_json( orient='records')
    return json_data





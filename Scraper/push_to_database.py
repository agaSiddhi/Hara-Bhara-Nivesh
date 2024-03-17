from backend.dao.dao import CompanyDao
import pandas as pd
import configparser

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def push_esg_data_to_database(csv_file='Scraper/final_data.csv', config_path='backend/config.ini'):
    try:
        config = read_config(config_path)
        
        company_dao = CompanyDao(host=config['DATABASE']['host'],
                                 user=config['DATABASE']['user'],
                                 password=config['DATABASE']['password'],
                                 database=config['DATABASE']['database'])

        esg_data = pd.read_csv(csv_file)

        for _, row in esg_data.iterrows():
            company_name, environment, social, governance, year, final_esg = row['Company Name'], row['Environment'], row['Social'], row['Governance'], row['Year'], row['Final_ESG']
            query = "INSERT INTO esg_data (company_name, environment, social, governance, year, final_esg) VALUES (%s, %s, %s, %s, %s, %s)"
            params = (company_name, environment, social, governance, year, final_esg)
            company_dao.execute_query(query, params)
        
        print("ESG data pushed to the database successfully.")
    except Exception as e:
        print(f"Error: {e}")


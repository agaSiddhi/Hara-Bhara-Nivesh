import pandas as pd
import configparser
from backend.dao.dao import CompanyDao

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

def execute_sql_query(company_dao, query, params):
    try:
        company_dao.execute_query(query, params)
    except Exception as e:
        print(f"Error: {e}")

def push_data_to_database(csv_file, config_path, table_name, column_names):
    try:
        config = read_config(config_path)
        company_dao = CompanyDao(host=config['DATABASE']['host'],
                                 user=config['DATABASE']['user'],
                                 password=config['DATABASE']['password'],
                                 database=config['DATABASE']['database'])
        data = pd.read_csv(csv_file)
        for _, row in data.iterrows():
            values = tuple(row[column] for column in column_names)
            placeholders = ', '.join(['%s'] * len(values))
            query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
            execute_sql_query(company_dao, query, values)
        print(f"{table_name} data pushed to the database successfully.")
    except Exception as e:
        print(f"Error: {e}")

def push_esg_data_to_database(csv_file='Scraper/final_data.csv', config_path='backend/config.ini'):
    column_names = ['Company Name', 'Date', 'Environment', 'Social', 'Governance', 'ESG_ratings', 'Final_ESG_Score', 'Historical_esg_score']
    push_data_to_database(csv_file, config_path, 'esg_data', column_names)

def push_article_data_to_database(csv_file='Scraper/Article_data.csv', config_path='backend/config.ini'):
    column_names = ['Heading', 'Text', 'Datetime', 'Company', 'Category', 'Score', 'Score_blob']
    push_data_to_database(csv_file, config_path, 'article_data', column_names)

def push_ratings_data_to_database(csv_file='Scraper/sustainalytics_data.csv', config_path='backend/config.ini'):
    column_names = ['Company Name', 'ESG Risk Rating', 'Score']
    push_data_to_database(csv_file, config_path, 'esg_ratings', column_names)

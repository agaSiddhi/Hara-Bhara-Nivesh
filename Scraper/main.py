import pandas as pd
from backend.ConfigLoader import ConfigLoader
from backend.DatabaseConnector import DatabaseConnector
from backend.DatabaseQueries import QueryRunner
from scraper_1 import scrape_and_save_articles
from scraper_2 import scrape_sustainalytics_data
from clean import process_articles_and_save
from scoring_algo import process_and_save_data


def insert_articles_to_database(data, query_runner):
    for article in data:
        query = "INSERT INTO companydata (articleHeading, articleText, articleDatetime) VALUES (%s, %s, %s)"
        params = (article['heading'], article['text'], article['datetime'])
        query_runner.execute_query(query, params)

if __name__ == "__main__":

    scrape_and_save_articles()

    process_articles_and_save()

    scrape_sustainalytics_data()

    process_and_save_data()

    esg_data = pd.read_csv('final_data.csv')

    filepath = "../backend/config.ini"
    config_loader = ConfigLoader(filepath)
    connector = DatabaseConnector(config_loader)
    connection = connector.connect()

    query_runner = QueryRunner(connection)

    insert_articles_to_database(esg_data, query_runner)

    # Close database connection
    connection.close()
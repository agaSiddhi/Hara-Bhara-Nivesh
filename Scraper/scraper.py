import requests
from bs4 import BeautifulSoup
import datetime
import csv
import os
from backend.ConfigLoader import ConfigLoader
from backend.DatabaseConnector import DatabaseConnector
from backend.DatabaseQueries import QueryRunner

def scrape_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article')
        scraped_data = []
        print("yes")
        for article in articles:
            heading = article.find('h2').text.strip()
            text_element = article.find('div', class_='entry-summary no-thumb')
            if text_element:
                text = text_element.text.strip()
            else:
                text = "N/A" 

            datetime_element = article.find('time')
            if datetime_element:
                datetime_str = datetime_element['datetime']
                article_datetime = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
            else:
                article_datetime = datetime.datetime.now()

            scraped_data.append({
                'heading': heading,
                'text': text,
                'datetime': article_datetime
            })

        return scraped_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

def save_to_csv(data, filename='articles.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Heading', 'Text', 'Datetime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in data:
            writer.writerow({'Heading': article['heading'],'Text': article['text'],'Datetime': article['datetime']})

def insert_articles_to_database(data, query_runner):
    for article in data:
        query = "INSERT INTO companydata (articleHeading, articleText, articleDatetime) VALUES (%s, %s, %s)"
        params = (article['heading'], article['text'], article['datetime'])
        query_runner.execute_query(query, params)

if __name__ == "__main__":
    # Load database configuration from config.ini file
    filepath = "../backend/config.ini"
    config_loader = ConfigLoader(filepath)
    print(config_loader.get_host)
    connector = DatabaseConnector(config_loader)

    # Establish database connection
    connection = connector.connect()

    # Initialize QueryRunner
    query_runner = QueryRunner(connection)

    # Scrape articles
    base_url = 'https://www.esginvesting.co.uk/category/news/companies/page/'
    all_articles_data = []
    for page_number in range(1, 28):
        print(page_number)
        url = f"{base_url}{page_number}/"
        articles_data = scrape_articles(url)
        all_articles_data.extend(articles_data)

    # Insert articles into the database
    save_to_csv(all_articles_data, filename='articles.csv')
    insert_articles_to_database(all_articles_data, query_runner)

    # Close database connection
    connection.close()
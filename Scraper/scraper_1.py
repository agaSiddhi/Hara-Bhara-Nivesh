import requests
from bs4 import BeautifulSoup
import datetime
import csv

def scrape_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all('article')
        scraped_data = []

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
            writer.writerow({
                'Heading': article['heading'],
                'Text': article['text'],
                'Datetime': article['datetime']
        })

def scrape_and_save_articles_base(base_url ='https://www.esginvesting.co.uk/category/news/companies/page/', total_pages = 27, filename='Scraper/Article_data.csv'):
    all_articles_data = []
    for page_number in range(1, total_pages + 1):
        url = f"{base_url}{page_number}/"
        articles_data = scrape_articles(url)
        all_articles_data.extend(articles_data)

    save_to_csv(all_articles_data, filename)


def scrape_and_save_articles_daily(base_url ='https://www.esginvesting.co.uk/category/news/companies/page/', total_pages = 1, filename='Scraper/Article_data.csv'):
    all_articles_data = []
    
    # Get yesterday's date
    yesterday_date = datetime.datetime.now().date() - datetime.timedelta(days=1)

    for page_number in range(1, total_pages + 1):
        url = f"{base_url}{page_number}/"
        articles_data = scrape_articles(url)
        
        # Filter articles with yesterday's date
        yesterday_articles = [article for article in articles_data if article['datetime'].date() == yesterday_date]
        
        all_articles_data.extend(yesterday_articles)

    save_to_csv(all_articles_data, filename)

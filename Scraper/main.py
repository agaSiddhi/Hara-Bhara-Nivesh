import schedule
import time

from Scraper.scraper_esg_investing import scrape_and_save_articles_daily
from Scraper.clean import process_articles_and_save
from Scraper.scraper_sustainalytics import scrape_sustainalytics_data
from Scraper.scoring_algo import scoring_algorithm
from Scraper.push_to_database import (
    push_esg_data_to_database,
    push_article_data_to_database,
    push_ratings_data_to_database,
)
from backend.dao.dao import read_config


def run_daily_tasks():
    print("Running daily tasks...")

    # Scrape Articles
    scrape_and_save_articles_daily()

    # Clean the Data and Extract the Sentiment
    process_articles_and_save()

    # Store these articles in the database
    push_article_data_to_database()

    # Scrape Live ESG Ratings
    scrape_sustainalytics_data()

    # Store these ratings in the database
    push_ratings_data_to_database()

    # Apply the scoring algorithm
    scoring_algorithm()

    # Store the Final Scores in the database
    push_esg_data_to_database()

    print("Daily tasks completed.")


def main():
    schedule.every().day.at("12:00").do(run_daily_tasks)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()

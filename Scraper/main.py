import pandas as pd
import schedule
import time
import requests
from bs4 import BeautifulSoup
import datetime
import http.client
from backend.dao.dao import CompanyDao
import configparser
import csv
import os
from datetime import datetime
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from Scraper.abbreviations import abbreviations_to_full_names
from Scraper.keywords import  environment_keywords, social_keywords, governance_keywords
from Scraper.scraper_1 import scrape_and_save_articles , scrape_articles , save_to_csv
from Scraper.scraper_2 import scrape_sustainalytics_data , parse_and_save_to_csv
from Scraper.clean import process_articles_and_save 
from Scraper.scoring_algo import process_and_save_data , normalize_score
from Scraper.push_to_database import push_esg_data_to_database, read_config

def run_weekly_tasks():
    print("Running weekly tasks...")
    #Scrape Articles 
    scrape_and_save_articles()
    #Clean the Data and Extract the Sentiment
    process_articles_and_save()
    #Scrape Live ESG Ratings
    scrape_sustainalytics_data()
    #Use data in the scoring algorithm
    process_and_save_data()
    #Save the data
    push_esg_data_to_database()
    print("Weekly tasks completed.")

schedule.every().monday.at("12:00").do(run_weekly_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)
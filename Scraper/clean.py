import pandas as pd
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from abbreviations import abbreviations_to_full_names
from keywords import  environment_keywords, social_keywords, governance_keywords

def process_articles_and_save(data_filename='Article_data.csv', 
                               abbreviations_to_full_names=abbreviations_to_full_names, 
                               environment_keywords=environment_keywords, 
                               social_keywords=social_keywords, 
                               governance_keywords=governance_keywords):

    data = pd.read_csv(data_filename)

    data['Company'] = data['Heading'].apply(lambda x: x.split()[0])

    if abbreviations_to_full_names:
        data['Company'] = data['Company'].replace(abbreviations_to_full_names)

    def classify_category(heading):
        for keyword in environment_keywords:
            if keyword in heading.lower():
                return 'Environment'
        for keyword in social_keywords:
            if keyword in heading.lower():
                return 'Social'
        for keyword in governance_keywords:
            if keyword in heading.lower():
                return 'Governance'
        return 'Unknown'

    data['Category'] = data['Heading'].apply(classify_category)

    sid = SentimentIntensityAnalyzer()

    def get_sentiment_score_vader(text):
        sentiment_score = sid.polarity_scores(text)
        return sentiment_score['compound']

    data['Score'] = data['Text'].apply(get_sentiment_score_vader)

    def get_sentiment_score_blob(text):
        blob = TextBlob(text)
        return blob.sentiment.polarity

    data['Score_blob'] = data['Text'].apply(get_sentiment_score_blob)

    data.to_csv(data_filename)

    

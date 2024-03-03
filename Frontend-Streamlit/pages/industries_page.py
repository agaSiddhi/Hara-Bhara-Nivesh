import streamlit as st
import pandas as pd
import numpy as np
import random
import string


def get_avg(ticker):
    return random.randint(10,20)

# Function to generate random company names
def generate_random_company_name():
    name_length = random.randint(5, 10)  # Random length between 5 and 10 characters
    return ''.join(random.choices(string.ascii_uppercase, k=name_length))  # Random uppercase letters

# Create the dictionary with random company names
randomm = {chr(65 + i): generate_random_company_name() for i in range(12)}  # A to L


# Create a dictionary with categories as keys and top industries as values
# Sample data for the DataFrame
data = {
    'Capital Goods': ['A','B'],
    'HealthCare':['D','E'],
    'Financial':['G','H'],
    'Services':['J','K'],
    'Other':['C','F'],
    'Consumer Staples': ['I','L']
}

# Create DataFrame from dictionary
companies_sorted = pd.DataFrame(data)

# company names from ticker 
company_mapping = {'AAPL': 'Apple','GOOG':'Google','MSFT':'Microsoft','AMZN':'Amazon','FB':'Facebook','NFLX':'Netflix'}
company_mapping.update(randomm)

ratings = {'AAPL': 1,'GOOG':2,'MSFT':3,'AMZN':3,'FB':4,'NFLX':4.5}

# Assuming you have a function to map tickers to their categories
def get_category(ticker):
    # Implement your logic here to determine the category for a given ticker
    # This is a placeholder function, you need to replace it with your actual logic
    if ticker in ['AAPL', 'GOOGL', 'MSFT']:
        return 'Equity'
    elif ticker == 'AMZN':
        return 'Hybrid'
    elif ticker == 'FB':
        return 'Debt'
    else :
        return 'Others'

# Assuming you have a function to map tickers to their industries
def get_industry(ticker):
    # Implement your logic here to determine the category for a given ticker
    # This is a placeholder function, you need to replace it with your actual logic
    if ticker in ['AAPL', 'GOOGL', 'MSFT']:
        return 'Capital Goods'
    elif ticker == 'GOOG':
        return 'HealthCare'
    elif ticker == 'AMZN':
        return 'Financial'
    elif ticker == 'FB':
        return 'Services'
    else :
        return 'Other'

def get_companies(stocks,industry):
    companies = []
    for ticker, amount in stocks.items():
        if industry == get_industry(ticker):
            companies.append({ticker: amount})
    return companies

def get_ticker_percentages(companies):
    # Getting composition of each ticker in out industry
    total_amount = sum(amount for company in companies for amount in company.values())
    ticker_percentages = {}
    for company in companies:
        for ticker, amount in company.items():
            percentage = (amount / total_amount) 
            if percentage!=0:
                ticker_percentages[ticker] = percentage

    # presenting current state of portfolio crategory
    ticker_percentages = dict(sorted(ticker_percentages.items(), key=lambda item: item[1], reverse=True))
    return ticker_percentages

def main():
    if st.button("Back to Home"):
            st.switch_page("Landing.py")

    industry = st.session_state['industry']
    stocks = st.session_state['stocks']

    companies = get_companies(stocks,industry)

    ticker_percentages = get_ticker_percentages(companies)

    if len(ticker_percentages)==0:
        st.subheader(f'There are no {industry} funds in your portfolio')
        st.write('---')

    for ticker, percent in ticker_percentages.items():
        company_name = company_mapping[ticker]
        company_category = get_category(ticker)
        rating = ratings[ticker]
        col1,col2 = st.columns([3,1])
        col1.markdown(f"### {company_name}")
        col1.write(f"{company_category} ●")
        col2.markdown(f'### {percent:.2%}')
        col2.write(f"{rating}★")
        st.write('---')

    st.subheader(f"High Scoring {industry} funds")
    for ticker in companies_sorted[{industry}].values:
        company_name = company_mapping[ticker[0]]
        company_category = get_category(ticker[0])
        score = get_avg(ticker)
        st.markdown(f"##### {company_name}")
        col1,col2 =st.columns([3,1])
        col1.write(f"{company_category} ●")
        col2.write(f"Average Score: {score}")

    st.write('---')
    if st.button("Go back"):
        st.switch_page("pages/2_PortfolioAnalyser.py")

if __name__ == "__main__":
    main()
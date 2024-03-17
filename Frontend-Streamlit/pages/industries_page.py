import streamlit as st
import pandas as pd
import numpy as np
import random
import string

from backend.configuration import initialize_system
company_service = initialize_system()

# Create DataFrame from dictionary
companies_sorted = company_service.return_companies_for_industry_category()
companies_sorted= pd.DataFrame.from_dict(companies_sorted, orient='index').transpose()
company_mapping =company_service.return_company_name_from_ticker()


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

    industry = st.session_state['industry']
    stocks = st.session_state['stocks']

    companies = company_service.return_companies_by_industry(stocks,industry)
    # print(companies)
    # print("jajaha")
    ticker_percentages = company_service.return_ticker_percentages(companies)

    if len(ticker_percentages)==0:
        st.subheader(f'There are no {industry} funds in your portfolio')
        st.write('---')

    for ticker, percent in ticker_percentages.items():
        if not ticker:
            break
        company_name = company_mapping[ticker]
        company_category = company_service.return_fund_category_from_ticker(ticker)[0][0]
        rating = company_service.return_average_score_from_ticker(ticker)
        col1,col2 = st.columns([3,1])
        col1.markdown(f"### {company_name}")
        col1.write(f"{company_category} ●")
        col2.markdown(f'### {percent:.2%}')
        col2.write(f"{rating}★")
        st.write('---')

    st.subheader(f"High Scoring {industry} funds")
    for ticker in companies_sorted[f"{industry}"].values:
        if not ticker:
            break
        company_name = company_mapping[ticker]
        company_category = (ticker)
        score = company_service.return_average_score_from_ticker(ticker)
        st.markdown(f"##### {company_name}")
        col1,col2 =st.columns([3,1])
        col1.write(f"{company_category} ●")
        col2.write(f"Average Score: {score}")

    st.write('---')
    
if __name__ == "__main__":
    main()
    col1,col2 = st.columns(2)
    
    if col1.button("Back to Home"):
        st.switch_page("Landing.py")
        
    if col2.button("Go back"):
        st.switch_page("pages/2_PortfolioAnalyser.py")


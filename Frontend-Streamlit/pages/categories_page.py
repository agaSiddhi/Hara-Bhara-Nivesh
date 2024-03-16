import streamlit as st
import pandas as pd
import numpy as np
import random
import string

from backend.configuration import initialize_system
company_service = initialize_system()

companies_sorted = company_service.return_companies_for_fund_category()
companies_sorted=pd.DataFrame.from_dict(companies_sorted, orient='index').transpose()
company_mapping = company_service.return_company_name_from_ticker()


# ratings = {'AAPL': 1,'GOOG':2,'MSFT':3,'AMZN':3,'FB':4,'NFLX':4.5}

# # Assuming you have a function to map tickers to their categories
# def get_category(ticker):
#     # Implement your logic here to determine the category for a given ticker
#     # This is a placeholder function, you need to replace it with your actual logic
#     if ticker in ['AAPL', 'GOOGL', 'MSFT']:
#         return 'Equity'
#     elif ticker == 'AMZN':
#         return 'Hybrid'
#     elif ticker == 'FB':
#         return 'Debt'
#     else :
#         return 'Others'

# # Assuming you have a function to map tickers to their industries
# def get_industry(ticker):
#     # Implement your logic here to determine the category for a given ticker
#     # This is a placeholder function, you need to replace it with your actual logic
#     if ticker in ['AAPL', 'GOOGL', 'MSFT']:
#         return 'Capital Goods'
#     elif ticker == 'GOOG':
#         return 'HealthCare'
#     elif ticker == 'AMZN':
#         return 'Financial'
#     elif ticker == 'FB':
#         return 'Services'
#     else :
#         return 'Other'
    
# def get_avg(ticker):
#     return random.randint(10,20)

# def get_companies(stocks,category):
#     companies = []
#     for ticker, amount in stocks.items():
#         if category == get_category(ticker):
#             companies.append({ticker: amount})
#     return companies

# def get_ticker_percentages(companies):
#     # Getting composition of each ticker in out category
#     total_amount = sum(amount for company in companies for amount in company.values())
#     ticker_percentages = {}
#     for company in companies:
#         for ticker, amount in company.items():
#             percentage = (amount / total_amount) 
#             if percentage!=0:
#                 ticker_percentages[ticker] = percentage

#     # presenting current state of portfolio crategory
#     ticker_percentages = dict(sorted(ticker_percentages.items(), key=lambda item: item[1], reverse=True))

#     return ticker_percentages

def main():

    if st.button("Back to Home"):
            st.switch_page("Landing.py")

    category = st.session_state['category']
    stocks = st.session_state['stocks']
    # print(category)
    # print(stocks)
    companies = company_service.return_companies(stocks,category)

    ticker_percentages = company_service.return_ticker_percentages(companies)

    if len(ticker_percentages)==0:
        st.subheader(f'There are no {category} funds in your portfolio')
        st.write('---')

    for ticker, percent in ticker_percentages.items():
        company_name = company_mapping[ticker]
        company_industry =company_service.return_industry_from_ticker(ticker)
        rating = company_service.return_average_score_from_ticker(ticker)
        col1,col2 = st.columns([3,1])
        col1.markdown(f"### {company_name}")
        col1.write(f"{company_industry} ●")
        col2.markdown(f'### {percent:.2%}')
        col2.write(f"{rating}★")
        st.write('---')

    st.subheader(f"High Scoring {category} funds")
    for ticker in companies_sorted[{category}].values:
        if not ticker:
            break
        company_name = company_mapping[ticker[0]]
        company_industry =company_service.return_industry_from_ticker(ticker[0])
        score = company_service.return_average_score_from_ticker(ticker[0])
        st.markdown(f"##### {company_name}")
        col1,col2 =st.columns([3,1])
        col1.write(f"{company_industry} ●")
        col2.write(f"Average Score: {score}")

    st.write('---')
    if st.button("Go back"):
        st.switch_page("pages/2_PortfolioAnalyser.py")


if __name__ == "__main__":
    main()


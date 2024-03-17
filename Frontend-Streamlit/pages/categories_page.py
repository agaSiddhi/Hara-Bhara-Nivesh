import streamlit as st
import pandas as pd
import numpy as np
import random
import string

from backend.configuration import initialize_system
company_service = initialize_system()

companies_sorted = company_service.return_companies_for_fund_category()
company_mapping = company_service.return_company_name_from_ticker()



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


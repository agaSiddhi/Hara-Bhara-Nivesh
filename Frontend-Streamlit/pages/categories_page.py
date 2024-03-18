import streamlit as st
import pandas as pd

from backend.configuration import initialize_system
company_service = initialize_system()[0]

companies_sorted = company_service.return_companies_for_fund_category()
companies_sorted=pd.DataFrame.from_dict(companies_sorted, orient='index').transpose()
company_mapping = company_service.return_company_name_from_ticker()



def main():

    category = st.session_state['category']
    stocks = st.session_state['stocks']

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


if __name__ == "__main__":
    main()
    col1,col2 = st.columns(2)
    
    if col1.button("Back to Home"):
        st.switch_page("Landing.py")
        
    if col2.button("Go back"):
        st.switch_page("pages/2_PortfolioAnalyser.py")



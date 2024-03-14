import streamlit as st
import pandas as pd
from backend.configuration import initialize_system
company_service = initialize_system()
import decimal

# Mock cap values for industries
industry_caps = {
    'Technology': 1000.00,
    'Financial': 500.00,
    'Services': 700.00,
    'HealthCare': 400.00,
    'Consumer Staples': 300.00,
    'Capital Goods':100.00,
    'Other': 600.00
}

# Define options for fund category and industry
fund_category_options = ['Equity', 'Hybrid', 'Debt', 'Other']
industry_options = ['Capital Goods', 'Financial', 'Services', 'HealthCare', 'Consumer Staples', 'Other']


def add_emissions(df,ticker, emissions):
    industry = company_service.return_industry_keyword_from_companyID(companyID=ticker)
    # print("industry = ",industry[0][0])
    cap = industry_caps.get(industry[0][0], 0)

    if emissions <= cap:
        # Add the remainder to the company's wallet
        remainder = decimal.Decimal(cap - emissions)
        wallet_balance = company_service.return_wallet_balance_from_companyID(companyID=ticker)[0][0]
        updated_wallet_balance = wallet_balance + remainder
        success = company_service.return_update_wallet_balance(ticker, updated_wallet_balance)
        if success:
            st.success(f'Emissions added successfully. Wallet balance updated: ${updated_wallet_balance}')
        else:
            st.error('Failed to update wallet balance.')
    else:
        st.error(f'Emissions ({emissions}) exceed the industry cap ({cap}). Not eligible to issue Carbon Credits.')

def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    
    ticker = st.session_state['ticker'].upper()
    # df = st.session_state['data']
    data1 = company_service.return_company_details_for_credits()
    df = pd.DataFrame(data1, columns=['Ticker', 'Name', 'Total Assets', 'Employee Count', 'Revenue', 'Wallet', 'Fund Category', 'Industry', 'Founded Year'])
    df = df[['Ticker', 'Name', 'Industry', 'Total Assets', 'Revenue', 'Employee Count', 'Founded Year', 'Fund Category', 'Wallet']]
    st.write(df)
    emissions = st.number_input('Enter Carbon Emissions (in tons):')
    if st.button('Add Emissions'):
        add_emissions(df,ticker, emissions)
        data1 = company_service.return_company_details_for_credits()
        df = pd.DataFrame(data1, columns=['Ticker', 'Name', 'Total Assets', 'Employee Count', 'Revenue', 'Wallet', 'Fund Category', 'Industry', 'Founded Year'])
        df = df[['Ticker', 'Name', 'Industry', 'Total Assets', 'Revenue', 'Employee Count', 'Founded Year', 'Fund Category', 'Wallet']]
        st.write(df)


    st.write('---')
    if st.button("Go back"):
        st.switch_page("pages/3_CarbonCredit.py")

if __name__ == "__main__":
    main()

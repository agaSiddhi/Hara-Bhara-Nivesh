import streamlit as st
import pandas as pd

# Mock cap values for industries
industry_caps = {
    'Technology': 1000,
    'Financial': 500,
    'Services': 700,
    'HealthCare': 400,
    'Consumer Staples': 300,
    'Capital Goods':100,
    'Other': 600
}

# Define options for fund category and industry
fund_category_options = ['Equity', 'Hybrid', 'Debt', 'Other']
industry_options = ['Capital Goods', 'Financial', 'Services', 'HealthCare', 'Consumer Staples', 'Other']


def add_emissions(df,ticker, emissions):
    industry = df[df['Ticker'] == ticker]['Industry'].iloc[0]
    cap = industry_caps.get(industry, 0)

    if emissions <= cap:
        # Add the remainder to the company's wallet
        remainder = cap - emissions
        wallet_balance = df[df['Ticker'] == ticker]['Wallet'].iloc[0]
        df.loc[df['Ticker'] == ticker, 'Wallet'] = wallet_balance + remainder
        st.success(f'Emissions added successfully. Wallet balance updated: ${wallet_balance + remainder}')
    else:
        st.error(f'Emissions ({emissions}) exceed the industry cap ({cap}). Not eligible to issue Carbon Credits.')

def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    
    ticker = st.session_state['ticker']
    df = st.session_state['data']
    st.write(df)
    emissions = st.number_input('Enter Carbon Emissions (in tons):')
    if st.button('Add Emissions'):
        add_emissions(df,ticker, emissions)
        st.write(df)


    st.write('---')
    if st.button("Go back"):
        st.switch_page("pages/3_CarbonCredit.py")

if __name__ == "__main__":
    main()

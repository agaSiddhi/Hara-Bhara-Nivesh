import streamlit as st
import pandas as pd

# Mock data for demonstration
data = {
    'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
    'Name': ['Apple Inc.', 'Alphabet Inc.', 'Microsoft Corporation'],
    'Industry': ['Capital Goods', 'Financial', 'Services'],
    'Total Assets': ['$338.52B', '$310.8B', '$317.37B'],
    'Revenue': ['$274.52B', '$221.1B', '$168.09B'],
    'Employee Count': [147000, 135301, 181000],
    'Founded Year': [1976, 1998, 1975],
    'Fund Category': ['Equity', 'Hybrid', 'Debt'],
    'Wallet': [100, 200, 150]  # Initial wallet balance for each company
}

df = pd.DataFrame(data)

# Define options for fund category and industry
fund_category_options = ['Equity', 'Hybrid', 'Debt', 'Other']
industry_options = ['Capital Goods', 'Financial', 'Services', 'HealthCare', 'Consumer Staples', 'Other']

def add_company(ticker, name, industry, total_assets, revenue, employee_count, founded_year, fund_category):
    # Append new company details to the data
    df.loc[len(df)] = [ticker.upper(), name, industry, total_assets, revenue, employee_count, founded_year, fund_category,0]
    st.success('Company added successfully!')

def form_callback():
    add_company(st.session_state.ticker, st.session_state.name, st.session_state.industry, st.session_state.total_assets, st.session_state.revenue, st.session_state.employee_count, st.session_state.founded_year, st.session_state.fund_category)
    st.session_state['ticker']=st.session_state.ticker
    st.session_state['data']=df
    st.switch_page("pages/add_credits.py")



def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

    # Page title  
    st.title('Carbon Credit Marketplace')
    ticker=None
    st.session_state['submitted'] = False
    ticker = st.text_input('Enter Ticker:')
    st.session_state.ticker=ticker
    if st.button('Check Ticker'):
        if ticker.upper() not in df['Ticker'].str.upper().tolist():
            with st.form("Add Company"):
                st.subheader(f'Company Details for Ticker: {ticker.upper()}')
                name = st.text_input("Enter Company Name",key=name)
                industry = st.selectbox('Industry:', industry_options,key=industry)
                total_assets = st.text_input('Total Assets:',key=total_assets)
                revenue = st.text_input('Revenue:',key=revenue)
                employee_count = st.number_input('Employee Count:', min_value=0,key=employee_count)
                founded_year = st.number_input('Founded Year:', min_value=0,key=founded_year)
                fund_category = st.selectbox('Fund Category:', fund_category_options,key=fund_category)
                st.form_submit_button("Add Company", on_click=form_callback) 

        else:   
            st.session_state['ticker']=ticker
            st.session_state['data']=df
            st.switch_page("pages/add_credits.py")

        
            

if __name__ == "__main__":
    main()

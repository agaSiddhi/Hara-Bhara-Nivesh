import streamlit as st
import pandas as pd

from backend.configuration import initialize_system
company_service = initialize_system()

data1 = company_service.return_company_details_for_credits()
# Mock data for demonstration
# data = {
#     'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
#     'Name': ['Apple Inc.', 'Alphabet Inc.', 'Microsoft Corporation'],
#     'Industry': ['Capital Goods', 'Financial', 'Services'],
#     'Total Assets': ['$338.52B', '$310.8B', '$317.37B'],
#     'Revenue': ['$274.52B', '$221.1B', '$168.09B'],
#     'Employee Count': [147000, 135301, 181000],
#     'Founded Year': [1976, 1998, 1975],
#     'Fund Category': ['Equity', 'Hybrid', 'Debt'],
#     'Wallet': [100, 200, 150]  # Initial wallet balance for each company
# }

# df = pd.DataFrame(data)
df = pd.DataFrame(data1, columns=['Ticker', 'Name', 'Total Assets', 'Employee Count', 'Revenue', 'Wallet', 'Fund Category', 'Industry', 'Founded Year'])
# Reorder columns as per the desired output
df = df[['Ticker', 'Name', 'Industry', 'Total Assets', 'Revenue', 'Employee Count', 'Founded Year', 'Fund Category', 'Wallet']]

# Define options for fund category and industry
fund_category_options = ['Equity', 'Hybrid', 'Debt', 'Other']
industry_options = ['Capital Goods', 'Financial', 'Services', 'HealthCare', 'Consumer Staples', 'Other']

def add_company(ticker, name, industry, total_assets, revenue, employee_count, founded_year, fund_category):
    industry_id = company_service.return_industry_id_by_keyword(industry)
    # print("industry_id = ",industry_id[0][0])

    success = company_service.return_add_new_company(ticker, name, total_assets, revenue, employee_count, founded_year, industry_id[0][0], fund_category)
    if success:
        st.success('Company added successfully!')
    else:
        st.error('Failed to add company.')

    # Append new company details to the data
    # df.loc[len(df)] = [ticker.upper(), name, industry, total_assets, revenue, employee_count, founded_year, fund_category,0]
    # st.success('Company added successfully!')
    # print("updated df", df)

def form_callback():
    add_company(st.session_state.ticker, st.session_state.name, st.session_state.industry, st.session_state.total_assets, st.session_state.revenue, st.session_state.employee_count, st.session_state.founded_year, st.session_state.fund_category)



def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

    # Page title  
    st.title('Carbon Credit Marketplace')
    ticker=None
    st.session_state['submitted'] = False
    ticker = st.text_input('Enter Ticker:')
    st.session_state.ticker=ticker
    # print("org df",df)
    if st.button('Check Ticker'):
        if ticker.upper() not in df['Ticker'].str.upper().tolist():
            with st.form("Add Company"):
                st.subheader(f'Company Details for Ticker: {ticker.upper()}')
                st.text_input("Enter Company Name",key="name")
                st.selectbox('Industry:', industry_options,key="industry")
                st.text_input('Total Assets:',key="total_assets")
                st.text_input('Revenue:',key="revenue")
                st.number_input('Employee Count:', min_value=0,key="employee_count")
                st.number_input('Founded Year:', min_value=0,key="founded_year")
                st.selectbox('Fund Category:', fund_category_options,key="fund_category")
                submitted = st.form_submit_button("Add Company", on_click=form_callback) 
                
        else:
            st.success('Company data present')

    if st.button('Get Credits'):
        st.session_state['ticker']=ticker
        st.session_state['data']=df
        st.switch_page("pages/add_credits.py")

        
            

if __name__ == "__main__":
    main()

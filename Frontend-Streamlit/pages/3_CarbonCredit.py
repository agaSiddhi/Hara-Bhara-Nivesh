import streamlit as st
import pandas as pd
import os
import yaml
from yaml import SafeLoader


from backend.configuration import initialize_system
company_service = initialize_system()

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

# sidebar page links
def authenticated_menu_company():
    st.sidebar.empty()
    st.sidebar.page_link("pages/3_CarbonCredit.py", label="List your Credits")
    st.sidebar.page_link("pages/4_AuctionPage.py", label="Credits Auction")
    if 'username' in st.session_state and st.session_state.username is not None:
        authenticator = st.session_state.get('authenticator')
        st.sidebar.page_link("pages/11_CompanyAccount.py", label="My Account")
        with st.sidebar:
            authenticator.logout('Logout', 'main', key='unique_key')     
    else:
        st.sidebar.page_link("pages/9_LoginCompany.py", label="Login")
        st.sidebar.page_link("pages/10_SignupCompany.py", label="Signup")    

# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=SafeLoader)
        return data
    except FileNotFoundError:
        return {}

# Import the company details into your script
company_data = read_yaml('company_details.yaml')

def get_credits_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['credits_wallet']

def add_emissions(ticker, emissions):
    industry = company_service.return_industry_keyword_from_companyID(companyID=ticker)
    # print("industry = ",industry[0][0])
    cap = industry_caps.get(industry[0][0], 0)

    if emissions <= cap:
        # Add the remainder to the company's wallet
        remainder = (cap - emissions)
        wallet_balance = company_service.return_wallet_balance_from_companyID(companyID=ticker)[0][0]
        wallet_balance = get_credits_balance(ticker)
        updated_wallet_balance = wallet_balance + remainder
        # success = company_service.return_update_wallet_balance(ticker, updated_wallet_balance)
        company_data['credentials']['usernames'][ticker]['credits_wallet']=updated_wallet_balance
        # Write the updated data back to the YAML file
        with open("company_details.yaml", 'w') as file:
            yaml.dump(company_data, file)
        st.success(f'Emissions added successfully. Wallet balance updated: ${updated_wallet_balance}')
    else:
        st.error(f'Emissions ({emissions}) exceed the industry cap ({cap}). Not eligible to issue Carbon Credits.')


def main():

    st.title('Carbon Credit Marketplace')
    ticker = st.session_state['company_ticker'].upper()
    emissions = st.number_input('Enter Carbon Emissions (in tons):')
    if st.button('Add Emissions'):
        add_emissions(ticker, emissions)
            

if __name__ == "__main__":
    if 'company_ticker'in st.session_state and st.session_state.company_ticker is not None:
        main()
    else:
        st.warning('Please login to list your credits')
      
    authenticated_menu_company()
    # back to home  
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
        
   


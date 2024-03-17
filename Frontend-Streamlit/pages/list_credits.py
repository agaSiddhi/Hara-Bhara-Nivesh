import streamlit as st
import pandas as pd
import os
import yaml
from yaml import SafeLoader

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

def get_company_name(ticker):
    return company_data['credentials']['usernames'][ticker]['name']

def get_wallet_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['money_wallet']

def get_credit_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['credits_wallet']

def update_wallet(company_ticker,credits_to_list):
    company_data['credentials']['usernames'][company_ticker]['credits_wallet'] -= credits_to_list
        # Write the updated data back to the YAML file
    with open("company_details.yaml", 'w') as file:
        yaml.dump(company_data, file)

def list_credits():
    st.title("List Credits")

    # Check if the company details are in the session state
    if 'company_ticker' in st.session_state:
        company_ticker=st.session_state.company_ticker
        company_ticker=company_ticker.upper()
        
        # Display company details
        st.subheader(f"{get_company_name(company_ticker)}")
        
        col1,col2 = st.columns(2)
        col1.write(f"Money Wallet Balance: ${get_wallet_balance(company_ticker)}")
        col2.write(f"Credits Wallet Balance: {get_credit_balance(company_ticker)} credits")

        # Form to list credits
        st.subheader("List Credits:")
        credits_to_list = st.number_input("Number of Credits to List", min_value=1)
        initial_bid = st.number_input("Initial Bid", min_value=0)
        minimum_step = st.number_input("Minimum Step", min_value=0.1)

        if st.button("List Credits"):
            # Validate if the company has enough credits in the wallet
            if credits_to_list <= get_credit_balance(company_ticker):
                # Prepare data for CSV
                data = {
                    'company_ticker': [company_ticker],
                    'credits_to_list': [credits_to_list],
                    'initial_bid': [initial_bid],
                    'minimum_step': [minimum_step]
                }

                # Create DataFrame
                df = pd.DataFrame(data)

                # Save to CSV file
                csv_filename = "your_listing_file.csv"
                if os.path.exists(csv_filename):
                    existing_df = pd.read_csv(csv_filename)
                    df = pd.concat([existing_df, df], ignore_index=True)

                df.to_csv(csv_filename, index=False)
                update_wallet(company_ticker,credits_to_list)
                st.success("Credits listed successfully!")
            else:
                st.error("Insufficient credits in the wallet.")
    else:
        st.warning("No company details found in the session state. Please log in.")
    
    if st.button("Go Back"):
        st.switch_page("pages/11_CompanyAccount.py")

if __name__ == "__main__":

    list_credits()

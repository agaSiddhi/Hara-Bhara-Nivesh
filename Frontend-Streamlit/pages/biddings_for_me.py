import streamlit as st
import pandas as pd
import yaml
from yaml import SafeLoader
import os

# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=SafeLoader)
        return data
    except FileNotFoundError:
        return {}


def update_wallets(company_ticker, bidder_company, bid_amount):
    # Load data from YAML file
    data=read_yaml('company_details.yaml')

    company_ticker = str(company_ticker)
    credits_listed = 0
    listing_file = pd.read_csv("your_listing_file.csv")
    matching_data = listing_file[listing_file['company_ticker'] == company_ticker]
    if not matching_data.empty:
        # st.write(matching_data)   
        credits_listed = int(matching_data.iloc[0].credits_to_list)
    
    money = bid_amount * credits_listed

    # Update credits_wallet and money_wallet for the company_ticker
    data['credentials']['usernames'][company_ticker]['money_wallet'] += money

    data['credentials']['usernames'][bidder_company]['credits_wallet'] += credits_listed
    data['credentials']['usernames'][bidder_company]['money_wallet'] -= money
 
    # Write the updated data back to the YAML file
    with open("company_details.yaml", 'w') as file:
        yaml.dump(data, file)


def display_bids_by_company(company_ticker):
    # Load the bidding data from the CSV file
    bidding_data = pd.read_csv("bidding_list.csv")
    company_ticker = str(company_ticker)
    matching_bids = bidding_data[bidding_data['company_ticker'] == company_ticker]

    if not matching_bids.empty:
        for index, row in matching_bids.iterrows():
            st.write(row)
            if st.button(f"Process Bid {index}"):
                process_bid(row)
                st.success("Bid processed!")
                # st.switch_page('pages/5_Login.py')
    else:
        st.warning("No biddings done yet")
                
def remove_company_ticker(company_ticker):
    # Load data from CSV file
    filename1 = "bidding_list.csv"

    df1 = pd.read_csv(filename1)
    
    # Filter out the row with the given company_ticker
    df1 = df1[df1['company_ticker'] != company_ticker]
    
    # Save the updated DataFrame back to the CSV file
    df1.to_csv(filename1, index=False)
    filename2 = "your_listing_file.csv"

    df2 = pd.read_csv(filename2)
    
    # Filter out the row with the given company_ticker
    df2 = df2[df2['company_ticker'] != company_ticker]
    
    # Save the updated DataFrame back to the CSV file
    df2.to_csv(filename2, index=False)


def process_bid(row):
    update_wallets(row.company_ticker, row.bidder_company, row.bid_amount)
    remove_company_ticker(row.company_ticker)
     

if __name__ == "__main__":
    if 'company_ticker' in st.session_state:
        company_ticker = st.session_state.company_ticker.upper()
        if not os.path.exists("bidding_list.csv"):
            st.warning("No biddings done yet")
        else:
            display_bids_by_company(company_ticker)
    else:
        st.error('Please login')

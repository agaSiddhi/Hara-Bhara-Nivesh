import streamlit as st
import pandas as pd
import os
from datetime import datetime

from backend.configuration import initialize_system
company_service = initialize_system()[0]
def get_current_price(company_ticker):
    listings = company_service.return_listings_for_auction()
    df1 = pd.DataFrame(listings, columns=["bidID", "initial_Bid", "minimum_Step", "credits_Listed", "companyID"])
    ini_bid = max(df1[df1['companyID'] == company_ticker]['initial_Bid'])
    return ini_bid 

def get_maximum_bidding_price(company_ticker,company_details):
    max_amount = company_service.return_max_bidding_amount(company_ticker)[0][0]
    if max_amount:
        return max_amount
    else:
        return get_current_price(company_details.get('companyID'))  # Return the initial bid if no bids are placed

def get_step_size(company_ticker):
    your_listing_file_path = "your_listing_file.csv"  # Replace with the actual path
    your_listing_df = pd.read_csv(your_listing_file_path)
    company_data = your_listing_df[your_listing_df['company_ticker'] == company_ticker]
    if not company_data.empty:
        return company_data['minimum_step'].values[0]
    else:
        return 0 
    
def bid_price():
    st.title("Bid Price")

    # Check if the company details are in the session state
    if 'cer_company' in st.session_state:
        company_details = st.session_state.cer_company

        # Form to list credits
        st.subheader("Bid Price:")
        print(get_maximum_bidding_price(company_details.get('companyID'),company_details))
        mini = float(get_maximum_bidding_price(company_details.get('companyID'),company_details))
        step_size = float(company_details.get('minimum_Step',0))

        credits_to_bid = st.number_input("Enter Bidding price", min_value=mini,step=step_size) 

        col1,col2=st.columns(2)
        if col1.button("Bid Price"):
            bidder = st.session_state.company_ticker.upper()
            bidID = company_details.get('bidID')
            bid = credits_to_bid
            company_service.return_insert_into_bidding_table(bidder, bidID, bid)
                
            st.success("Success!")
        if col2.button("Go back"):
            st.switch_page("pages/4_AuctionPage.py")
    else:
        st.warning("No company details found in the session state. Please log in.")

if __name__ == "__main__":
    bid_price()

import streamlit as st
import pandas as pd
import os
from datetime import datetime

def get_current_price(company_ticker):
    your_listing_file_path = "your_listing_file.csv"  # Replace with the actual path
    your_listing_df = pd.read_csv(your_listing_file_path)

    company_data = your_listing_df[your_listing_df['company_ticker'] == company_ticker]
    if not company_data.empty:
        return company_data['initial_bid'].values[0]
    else:
        return 0 

def get_maximum_bidding_price(company_ticker):
    bidding_list_file_path = "bidding_list.csv"  # Replace with the actual path
    if not os.path.exists(bidding_list_file_path):
        return get_current_price(company_ticker) 
    bidding_list_df = pd.read_csv(bidding_list_file_path)

    company_bids = bidding_list_df[bidding_list_df['company_ticker'] == company_ticker]
    if not company_bids.empty:
        return company_bids['bid_amount'].max()
    else:
        return get_current_price(company_ticker)  # Return the initial bid if no bids are placed

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
        mini = float(get_maximum_bidding_price(company_details.get('company_ticker')))
        step_size = get_step_size(company_details.get('company_ticker'))
        credits_to_bid = st.number_input("Enter Bidding price", min_value=mini,step=step_size) 

        col1,col2=st.columns(2)
        if col1.button("Bid Price"):
            data = {
                    'company_ticker': [company_details.get('company_ticker', 'N/A')],
                    'bid_amount': [credits_to_bid],
                    'bidder_company': [st.session_state.company_ticker.upper()],
                    'bid_time': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                    }

            # Create DataFrame
            df = pd.DataFrame(data)

            # Save to CSV file
            csv_filename = "bidding_list.csv"
            if os.path.exists(csv_filename):
                existing_df = pd.read_csv(csv_filename)
                df = pd.concat([existing_df, df], ignore_index=True)

                df.to_csv(csv_filename, index=False)

                
            else:
                df.to_csv(csv_filename, index=False)
                
            st.success("Success!")
        if col2.button("Go back"):
            st.switch_page("pages/4_AuctionPage.py")
    else:
        st.warning("No company details found in the session state. Please log in.")

if __name__ == "__main__":
    bid_price()

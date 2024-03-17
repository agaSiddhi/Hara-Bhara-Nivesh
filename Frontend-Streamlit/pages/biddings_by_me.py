import streamlit as st
import pandas as pd
import os

def display_bids_by_company(company_ticker):
    # Load the bidding data from the CSV file
    bidding_data = pd.read_csv("bidding_list.csv")
    filtered_bids = bidding_data[bidding_data['bidder_company'] == company_ticker]

    if not filtered_bids.empty:
        # Display the filtered bidding data
        st.write(filtered_bids)
    else:
        st.warning("No biddings done yet")

if __name__ == "__main__":
    company_ticker = st.session_state.company_ticker# Replace with the desired company ticker
    company_ticker = company_ticker.upper()
    if not os.path.exists("bidding_list.csv"):
        st.warning("No biddings done yet")
    else:
        display_bids_by_company(company_ticker)

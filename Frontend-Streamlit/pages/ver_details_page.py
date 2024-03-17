import streamlit as st
import pandas as pd
import os

def append(company,user_bid):
    company['Bids'].append({'Bidder': st.session_state.bidder, 'Bid': user_bid})
    st.success(f"Bid placed successfully! Current highest bid: ${user_bid} by {st.session_state.bidder}")

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


def main():
    if st.button("Back to Home"):
            st.switch_page("Landing.py")
    
    # Check if the cer_company details are in the session state
    if 'cer_company' in st.session_state:
        company_details = st.session_state.cer_company

        # Display company details
        # st.subheader(f"Company Name: {company_details.get('Name', 'N/A')}")
        st.subheader(f"{company_details.get('company_ticker', 'N/A')}")
        st.write(f"Initial Bidding Price: ${get_current_price(company_details['company_ticker'])}")
        st.write(f"Current highest bid: ${get_maximum_bidding_price(company_details['company_ticker'])}")

        col1,col2 =st.columns(2)
        # Step 1: Click "Place Bid" button to initiate the bid placement
        place_bid_button = col1.button("Place Bid")

        if place_bid_button:
            st.switch_page('pages/bid_price.py')

    else:
        st.warning("No company details found in the session state. Please select a company from the auction page.")
            
    if col2.button("Go back"):
        st.switch_page("pages/4_AuctionPage.py")
if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import os

from backend.configuration import initialize_system
company_service = initialize_system()[0]  

def append(company,user_bid):
    company['Bids'].append({'Bidder': st.session_state.bidder, 'Bid': user_bid})
    st.success(f"Bid placed successfully! Current highest bid: ${user_bid} by {st.session_state.bidder}")

def get_current_price(company_ticker):

    listings = company_service.return_listings_for_auction()
    df1 = pd.DataFrame(listings, columns=["bidID", "initial_Bid", "minimum_Step", "credits_Listed", "companyID"])
    ini_bid = max(df1[df1['companyID'] == company_ticker]['initial_Bid'])
    return ini_bid 

def get_maximum_bidding_price(company_ticker,company_details):
    max_amount = company_service.return_max_bidding_amount(company_ticker)[0][0]
    print("max bid price",max_amount)
    if max_amount:
        return max_amount
    else:
        return get_current_price(company_details.get('companyID'))


def main():
    if st.button("Back to Home"):
            st.switch_page("Landing.py")
    
    # Check if the cer_company details are in the session state
    if 'cer_company' in st.session_state:
        company_details = st.session_state.cer_company

        # Display company details
        st.subheader(f"{company_details.get('companyID', 'N/A')}")
        st.write(f"Initial Bidding Price: $ {company_details.get('initial_Bid',0)}")

        st.write(f"Current highest bid: $ {get_maximum_bidding_price(company_details['companyID'],company_details)}")

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
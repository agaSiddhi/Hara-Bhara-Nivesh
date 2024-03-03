import streamlit as st
import pandas as pd
import time
import threading

def append(company,user_bid):
    company['Bids'].append({'Bidder': st.session_state.bidder, 'Bid': user_bid})
    st.success(f"Bid placed successfully! Current highest bid: ${user_bid} by {st.session_state.bidder}")

def get_current_price(company):
    if company['Bids']:
        return max(company['Bids'], key=lambda x: x['Bid'])['Bid']
    else:
        return company['Initial Bid']


def main():
    if st.button("Back to Home"):
            st.switch_page("Landing.py")
    
    company = st.session_state['company']

    current_price = get_current_price(company)
    num_bids = len(company['Bids'])
    bid_history = company['Bids']
    st.subheader(f"**{company['Name']}**")
    st.markdown(f"##### {company['Description']}")
    col1,col2 = st.columns(2)
    col1.write(f"Ticker: {company['Ticker']}")
    col2.write(f"Initial Bid: ${company['Initial Bid']}")
    col1.write(f"Current Price: ${current_price}")
    col2.write(f"Number of Bids: {num_bids}")
    if st.button('View Bid History'):
        for bid in bid_history:
            st.markdown(f"###### Bidder: {bid['Bidder']}, Bid: ${bid['Bid']}")

    initial_bid = company['Initial Bid']
    minimum_step = company['Minimum Step']

    user_bid = st.number_input('Your Bid:', min_value=current_price, step=minimum_step)
    st.text_input('Enter your Name:',key='bidder')
    if st.button('Place Bid'):
        append(company, user_bid)
            
    if st.button("Go back"):
        st.switch_page("pages/4_AuctionPage.py")
if __name__ == "__main__":
    main()
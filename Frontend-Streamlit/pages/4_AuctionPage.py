import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os

from backend.configuration import initialize_system
company_service = initialize_system()[0]
    
def get_maximum_bidding_price(company_ticker,ini_bid):
    max_amount = company_service.return_max_bidding_amount(company_ticker)[0][0]
    print("max bid price",max_amount)
    if max_amount:
        return max_amount
    else:
        # return get_current_price(company_details)
        print("ini bid",ini_bid)
        return ini_bid  # Return the initial bid if no bids are placed

def filter_companies(search_query, data):
    return data[data['Name'].str.contains(search_query, case=False)]

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

def main():
    
    # --- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    listings = company_service.return_listings_for_auction()
    df1 = pd.DataFrame(listings, columns=["bidID", "initial_Bid", "minimum_Step", "credits_Listed", "companyID"])
    search_query = st.text_input('Search Companies:', value='', key='search_input')

    # Display listings
    if df1.empty:
        st.write("Auction Market is empty")
    else:
        for index, row in df1.iterrows():
            company_ticker = row['companyID']
            bidID = row['bidID']
            st.subheader(f"**{company_ticker}**")
            col1, col2, col3 = st.columns([1, 1, 0.5])
            ini_bid = max(df1[df1['companyID'] == company_ticker]['initial_Bid'])
            # print(ini_bid)
            st.write(f"##### Current highest bid: $ {get_maximum_bidding_price(company_ticker,ini_bid)}")
            st.write(f"##### Credits Listed: {row['credits_Listed']}")
            # Add detail button to view company details
            button_label = "Details"
            button_key = f"{button_label}_{bidID}_{company_ticker}_CER"
            if col3.button(button_label, key=button_key):
                st.session_state['cer_company'] = row
                st.switch_page("pages/cer_details_page.py") 
            st.write("---")

    


if __name__ == "__main__":
    listings_data = company_service.return_listings_for_auction()
    if len(listings_data) > 0:
        main()
    else:
        st.warning("Auction Market is empty")
    
    authenticated_menu_company()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")





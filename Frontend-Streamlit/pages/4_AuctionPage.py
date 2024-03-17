import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os

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

    # Load data from CSV file
    # Replace with the actual path to your CSV file
    df = pd.read_csv(filename)
    
    # --- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["CER", "VER"],
        icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # --- CER Tab ---
    if selected == "CER":

        # Search bar with search icon
        search_query = st.text_input('Search Companies:', value='', key='search_input')

        # Display listings
        if len(df) == 0:
            st.write('No results found.')
        else:
            for index, row in df.iterrows():
                st.subheader(f"**{row['company_ticker']}**")
                col1, col2, col3 = st.columns([1, 1, 0.5])
                col1.markdown(f"##### Current highest bid: ${get_maximum_bidding_price(row['company_ticker'])}")
                col2.markdown(f"##### Credits Listed: {row['credits_to_list']}")
                # Add detail button to view company details
                button_label = "Details"
                button_key = f"{button_label}_{row['company_ticker']}_CER"
                if col3.button(button_label, key=button_key):
                    st.session_state['cer_company'] = row
                    st.switch_page("pages/cer_details_page.py") 
                st.write("---")

    # --- VER Tab ---
    if selected == "VER":

        # Search bar with search icon
        search_query = st.text_input('Search Companies:', value='', key='search_input')

        # Display listings
        if len(df) == 0:
            st.write('No results found.')
        else:
            for index, row in df.iterrows():
                st.subheader(f"**{row['company_ticker']}**")
                col1, col2, col3 = st.columns([1, 1, 0.5])
                col1.markdown(f"##### Current highest bid: ${get_maximum_bidding_price(row['company_ticker'])}")
                col2.markdown(f"##### Credits Listed: {row['credits_to_list']}")
                # Add detail button to view company details
                button_label = "Details"
                button_key = f"{button_label}_{row['company_ticker']}_CER"
                if col3.button(button_label, key=button_key):
                    st.session_state['cer_company'] = row
                    st.switch_page("pages/cer_details_page.py") 
                st.write("---")
        



if __name__ == "__main__":
    filename = "your_listing_file.csv"
    if os.path.exists(filename):
        main()
    else:
        st.warning("Auction Market is empty")
    
    authenticated_menu_company()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")





import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
import os
import pandas as pd
import streamlit_shadcn_ui as ui
from backend.configuration import initialize_system
company_service= initialize_system()[0]

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
        
# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            company_data = yaml.load(file, Loader=SafeLoader)
        return company_data
    except FileNotFoundError:
        return {}

# Import the company details into your script
company_data = read_yaml('company_details.yaml')

def update_wallets(company_ticker, bidder_company, bid_amount,bidID):

    company_ticker = str(company_ticker)
    # credits_listed = 0
    credits_listed = company_service.return_credits_listed_from_bidID(bidID)[0][0]
    
    money = bid_amount * credits_listed

    # Update credits_wallet and money_wallet for the company_ticker
    company_service.return_add_money_to_wallet(company_ticker, money)
    company_service.return_add_credit_to_credit_wallet(bidder_company, money)
    company_service.return_subtract_money_from_wallet(bidder_company, money)
    # company_data['credentials']['usernames'][company_ticker]['money_wallet'] += money

    # company_data['credentials']['usernames'][bidder_company]['credits_wallet'] += credits_listed
    # company_data['credentials']['usernames'][bidder_company]['money_wallet'] -= money
 
    # Write the updated company_data back to the YAML file
    # with open("company_details.yaml", 'w') as file:
    #     yaml.dump(company_data, file)
        
def display_bids_by_company(company_ticker):
    # Load the bidding company_data from the CSV file
    # bidding_data = pd.read_csv("bidding_list.csv")
    company_ticker = str(company_ticker)
    bidding_details_from_ticker = company_service.return_bidding_details_from_ticker(company_ticker)
    matching_bids= pd.DataFrame(bidding_details_from_ticker, columns=['bidder','bid_amnt','bidID'])

    # matching_bids = bidding_details_from_ticker_df[bidding_details_from_ticker_df['company_ticker'] == company_ticker]

    if not matching_bids.empty:
        for index, row in matching_bids.iterrows():
            Bidder_company=row['bidder']
            amount=row['bid_amnt']
            # time=row['bid_time']
            ui.metric_card(title=Bidder_company, content=f"Bid: ${amount}")
            if st.button(f"Process Bid"):
                process_bid(row,company_ticker)
                st.success("Bid processed!")
                # st.switch_page('pages/5_Login.py')
    else:
        st.warning("No biddings done yet")
                
def remove_company_ticker(company_ticker, bidID):
    # Load company_data from CSV file
    company_service.return_remove_bid_from_bidID(bidID)


def process_bid(row,company_ticker):
    update_wallets(company_ticker, row.bidder, row.bid_amnt,row.bidID)
    remove_company_ticker(company_ticker,row.bidID)

def get_company_name(ticker):
    return st.session_state.company[0][0]

def get_wallet_balance(ticker):
    return st.session_state.company[0][3]
def get_credit_balance(ticker):
    return st.session_state.company[0][4]

def update_wallet(company_ticker,credits_to_list):
    company_data['credentials']['usernames'][company_ticker]['credits_wallet'] -= credits_to_list
        # Write the updated company_data back to the YAML file
    with open("company_details.yaml", 'w') as file:
        yaml.dump(company_data, file)

def my_account():
    # --- NAVIGATION MENU ---
    
    selected = option_menu(
        menu_title=None,
        options=["My Account","List Credits", "My Biddings","My Bids"],
        icons=["person-fill","bar-chart-fill","currency-exchange","wallet-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
        menu_icon="cast",
        styles={    
        "nav-link-selected": {"background-color": "#2B8C0C"},
        }   
    )
    
    if selected=="My Account":

        # Check if the company details are in the session state
        if 'company_ticker' in st.session_state and st.session_state.company_ticker is not None:
            
            company_ticker = st.session_state.get('company_ticker').upper()
            company_ticker=company_ticker.upper()
            company_details = company_service.return_signup_company_data(company_ticker)
            company_details_df = pd.DataFrame(company_details,columns=['companyName','ticker','password','walletBalance','creditBalance','fundCat','industryID'])

            # image is to be replaced by actual image of the company ehich we ll keep downloaded for presenation purpose
            user_image_url = '../assets/username.jpeg'
            # Display user image and name on the main page
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(user_image_url, caption=company_ticker, use_column_width=True)
                
            # Display company details
            st.subheader(f"{get_company_name(company_ticker)}")
            
            col1,col2 = st.columns(2)
            col1.write(f"Money Wallet Balance: ${company_details_df['walletBalance'][0]}")
            col2.write(f"Credits Wallet Balance: {company_details_df['creditBalance'][0]} credits")
            
            st.write("---")
            add_vertical_space(2)
            
        else:
            st.warning("No company details found in the session state. Please log in.")
            
    # List Credits
    if selected=="List Credits":
        
        # Check if the company details are in the session state
        if 'company_ticker' in st.session_state:
            company_ticker=st.session_state.company_ticker
            company_ticker=company_ticker.upper()
            company_details = company_service.return_signup_company_data(company_ticker)
            company_details_df = pd.DataFrame(company_details,columns=['companyName','ticker','password','walletBalance','creditBalance','fundCat','industryID'])
            
            # Display company details
            st.subheader(f"{get_company_name(company_ticker)}")
            
            col1,col2 = st.columns(2)
            col1.write(f"Money Wallet Balance: ${company_details_df['walletBalance'][0]}")
            col2.write(f"Credits Wallet Balance: {company_details_df['creditBalance'][0]} credits")

            # Form to list credits
            st.subheader("List Credits:")
            credits_to_list = st.number_input("Number of Credits to List", min_value=1)
            initial_bid = st.number_input("Initial Bid", min_value=0)
            minimum_step = st.number_input("Minimum Step", min_value=0.1)

            if st.button("List Credits"):
                # Validate if the company has enough credits in the wallet
                if credits_to_list <= get_credit_balance(company_ticker):
                    # Prepare company_data for CSV
                    company_service.add_listed_credit_to_bid(initial_bid,minimum_step,credits_to_list,company_ticker)
                   
                    company_service.return_update_credit_wallet_balance(company_ticker, credits_to_list)
                    st.success("Credits listed successfully!")

                    company_details = company_service.return_signup_company_data(company_ticker)
                    company_details_df = pd.DataFrame(company_details,columns=['companyName','ticker','password','walletBalance','creditBalance','fundCat','industryID'])
                    updated_credit_balance = company_details_df['creditBalance'][0]  # Get the updated credit balance from the database
                    col2.write(f"Updated Credit Balance: {updated_credit_balance} credits") 
                else:
                    st.error("Insufficient credits in the wallet.")
        else:
            st.warning("No company details found in the session state. Please log in.")

     
    # my biddings     
    if selected=="My Biddings":
        if 'company_ticker' in st.session_state:
            biddings_data1 = company_service.return_my_biddings()
            if len(biddings_data1) == 0:
            # if not os.path.exists("bidding_list.csv"):
                st.warning("No biddings done yet")

            
            else:
                company_ticker = st.session_state.company_ticker# Replace with the desired company ticker
                company_ticker = company_ticker.upper()
                # Load the bidding company_data from the CSV file
                # print(biddings_data1)
                biddings_data1_df= pd.DataFrame(biddings_data1, columns=['bidder', 'bidID', 'bid_amnt'])
                
                filtered_bids = biddings_data1_df[biddings_data1_df['bidder'] == company_ticker]

                if not filtered_bids.empty:
                    # Display the filtered bidding company_data
                    for index,row in filtered_bids.iterrows():
                        # Bidder_ticker=row['company_ticker']
                        Bidder_ticker = company_service.return_companyID_from_bidID(row['bidID'])
                        # time = row['bid_time']
                        amount = row['bid_amnt']
                        ui.metric_card(title=Bidder_ticker, content=f"Bid: ${amount}")
                else:
                    st.warning("No biddings done yet")
        else:
            st.warning('No company details found in the session state. Please log in.')
    
    # biddings for me
    if selected=="My Bids":
        if 'company_ticker' in st.session_state:
            company_ticker = st.session_state.company_ticker.upper()
            # if not os.path.exists("bidding_list.csv"):
            #     st.warning("No biddings done yet")
            biddings_data1 = company_service.return_my_biddings()
            if len(biddings_data1) == 0:
                st.warning("No biddings done yet")
            else:
                display_bids_by_company(company_ticker)
        else:
            st.warning('No company details found in the session state. Please log in.')
            

if __name__ == "__main__":
    my_account()
    
    authenticated_menu_company()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

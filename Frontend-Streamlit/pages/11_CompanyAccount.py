import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_option_menu import option_menu
import os
import pandas as pd
import streamlit_shadcn_ui as ui


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

def update_wallets(company_ticker, bidder_company, bid_amount):

    company_ticker = str(company_ticker)
    credits_listed = 0
    listing_file = pd.read_csv("your_listing_file.csv")
    matching_data = listing_file[listing_file['company_ticker'] == company_ticker]
    if not matching_data.empty:
        # st.write(matching_data)   
        credits_listed = int(matching_data.iloc[0].credits_to_list)
    
    money = bid_amount * credits_listed

    # Update credits_wallet and money_wallet for the company_ticker
    company_data['credentials']['usernames'][company_ticker]['money_wallet'] += money

    company_data['credentials']['usernames'][bidder_company]['credits_wallet'] += credits_listed
    company_data['credentials']['usernames'][bidder_company]['money_wallet'] -= money
 
    # Write the updated company_data back to the YAML file
    with open("company_details.yaml", 'w') as file:
        yaml.dump(company_data, file)


def display_bids_by_company(company_ticker):
    # Load the bidding company_data from the CSV file
    bidding_data = pd.read_csv("bidding_list.csv")
    company_ticker = str(company_ticker)
    matching_bids = bidding_data[bidding_data['company_ticker'] == company_ticker]

    if not matching_bids.empty:
        for index, row in matching_bids.iterrows():
            Bidder_company=row['bidder_company']
            amount=row['bid_amount']
            time=row['bid_time']
            ui.metric_card(title=Bidder_company, content=f"Bid: ${amount}", description=f"{time}")
            if st.button(f"Process Bid"):
                process_bid(row)
                st.success("Bid processed!")
                # st.switch_page('pages/5_Login.py')
    else:
        st.warning("No biddings done yet")
                
def remove_company_ticker(company_ticker):
    # Load company_data from CSV file
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

def get_company_name(ticker):
    return company_data['credentials']['usernames'][ticker]['name']

def get_wallet_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['money_wallet']

def get_credit_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['credits_wallet']

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

            # image is to be replaced by actual image of the company ehich we ll keep downloaded for presenation purpose
            user_image_url = '../assets/username.jpeg'
            # Display user image and name on the main page
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(user_image_url, caption=company_ticker, use_column_width=True)
                
            # Display company details
            st.subheader(f"{get_company_name(company_ticker)}")
            
            col1,col2 = st.columns(2)
            col1.write(f"Money Wallet Balance: ${get_wallet_balance(company_ticker)}")
            col2.write(f"Credits Wallet Balance: {get_credit_balance(company_ticker)} credits")
            
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
            
            # Display company details
            st.subheader(f"{get_company_name(company_ticker)}")
            
            col1,col2 = st.columns(2)
            col1.write(f"Money Wallet Balance: ${get_wallet_balance(company_ticker)}")
            col2.write(f"Credits Wallet Balance: {get_credit_balance(company_ticker)} credits")

            # Form to list credits
            st.subheader("List Credits:")
            credits_to_list = st.number_input("Number of Credits to List", min_value=1)
            initial_bid = st.number_input("Initial Bid", min_value=0)
            minimum_step = st.number_input("Minimum Step", min_value=0.1)

            if st.button("List Credits"):
                # Validate if the company has enough credits in the wallet
                if credits_to_list <= get_credit_balance(company_ticker):
                    # Prepare company_data for CSV
                    company_data = {
                        'company_ticker': [company_ticker],
                        'credits_to_list': [credits_to_list],
                        'initial_bid': [initial_bid],
                        'minimum_step': [minimum_step]
                    }

                    # Create DataFrame
                    df = pd.DataFrame(company_data)

                    # Save to CSV file
                    csv_filename = "your_listing_file.csv"
                    if os.path.exists(csv_filename):
                        existing_df = pd.read_csv(csv_filename)
                        df = pd.concat([existing_df, df], ignore_index=True)

                    df.to_csv(csv_filename, index=False)
                    update_wallet(company_ticker,credits_to_list)
                    st.success("Credits listed successfully!")
                else:
                    st.error("Insufficient credits in the wallet.")
        else:
            st.warning("No company details found in the session state. Please log in.")

     
    # my biddings     
    if selected=="My Biddings":
        if 'company_ticker' in st.session_state:
            if not os.path.exists("bidding_list.csv"):
                st.warning("No biddings done yet")
            else:
                company_ticker = st.session_state.company_ticker# Replace with the desired company ticker
                company_ticker = company_ticker.upper()
                # Load the bidding company_data from the CSV file
                bidding_data = pd.read_csv("bidding_list.csv")
                filtered_bids = bidding_data[bidding_data['bidder_company'] == company_ticker]

                if not filtered_bids.empty:
                    # Display the filtered bidding company_data
                    for index,row in filtered_bids.iterrows():
                        Bidder_ticker=row['company_ticker']
                        time = row['bid_time']
                        amount = row['bid_amount']
                        ui.metric_card(title=Bidder_ticker, content=f"Bid: ${amount}", description=f"{time}")
                else:
                    st.warning("No biddings done yet")
        else:
            st.warning('No company details found in the session state. Please log in.')
    
    # biddings for me
    if selected=="My Bids":
        if 'company_ticker' in st.session_state:
            company_ticker = st.session_state.company_ticker.upper()
            if not os.path.exists("bidding_list.csv"):
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

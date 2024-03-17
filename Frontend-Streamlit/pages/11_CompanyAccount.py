import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_extras.add_vertical_space import add_vertical_space

# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=SafeLoader)
        return data
    except FileNotFoundError:
        return {}

# Import the company details into your script
company_data = read_yaml('company_details.yaml')

def get_company_name(ticker):
    return company_data['credentials']['usernames'][ticker]['name']

def get_wallet_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['money_wallet']

def get_credit_balance(ticker):
    return company_data['credentials']['usernames'][ticker]['credits_wallet']


def my_account():
    st.title("My Account Page")

    # Check if the company details are in the session state
    if 'company_ticker' in st.session_state and st.session_state.company_ticker is not None:
        
        company_ticker = st.session_state.get('company_ticker').upper()
        company_ticker=company_ticker.upper()

        # image is to be replaced by actual image of the company ehich we ll keep downloaded for presenation purpose
        user_image_url = '/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/assets/username.jpeg'
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
        
        # Bids Placed 
        
        col1,col2,col3=st.columns(3)
        if col1.button("Add credits for auction"):
            st.switch_page("pages/list_credits.py")
        if col2.button("My Biddings"):
            st.switch_page("pages/biddings_by_me.py")
        if col3.button("Biddings for my credits"):
            st.switch_page("pages/biddings_for_me.py")
    else:
        st.warning("No company details found in the session state. Please log in.")

if __name__ == "__main__":
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    my_account()

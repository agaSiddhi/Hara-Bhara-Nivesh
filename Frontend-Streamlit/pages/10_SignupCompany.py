import streamlit as st
import re
import yaml
import streamlit_authenticator as stauth
from backend.configuration import initialize_system

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
        
# Function to validate email format
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

# Function to write data to YAML file
def write_to_yaml(data, filename):
    with open(filename, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data
    except FileNotFoundError:
        return {}

company_service= initialize_system()[0]

def company_signup():
    st.title("Company Sign Up")

    # Input fields for company details
    name = st.text_input("Company Name")
    ticker = st.text_input("Company Ticker")
    password = st.text_input("Password", type="password", key="signup_password")
    verify_password = st.text_input("Verify Password", type="password", key="signup_verify_password")
    initial_money_wallet = st.number_input("Initial Money Wallet Balance", value=0)
    initial_credits_wallet = st.number_input("Initial Credits Wallet Balance", value=0)
    industry_options = ['Capital Goods','Financial', 'Services','Health Care','Consumer Staples','Others']
    industry = st.selectbox("Industry Type:", industry_options)
    fund_category_options = ['Equity', 'Hybrid', 'Debt', 'Others']
    fund_category = st.selectbox("Fund Category Type:", fund_category_options)

    # Button to submit the signup form
    if st.button("Sign Up"):
        # Validate if all fields are not empty
        if name and ticker and password and password == verify_password:
            # Load existing data or create a new dictionary if the file doesn't exist
            company_data = read_yaml('company_details.yaml')
            if company_data is None:
                company_data = {}
                
            # if 'credentials' not in company_data:
            #     company_data['credentials'] = {'usernames': {}}
                
            hashed_password = stauth.Hasher([password]).generate()
            
            # Add company details to the dictionary

            # Write company details to YAML file
            company_service.return_add_new_company_signup(name,ticker, hashed_password[0],initial_money_wallet,initial_credits_wallet,industry,fund_category)
            # write_to_yaml(company_data, 'company_details.yaml')
            st.success("You have successfully signed up as a company!")
        elif password != verify_password:
            st.error("Passwords do not match. Please verify your password.")
        else:
            st.error("All fields are required.")

if __name__ == "__main__":
    company_signup()
    authenticated_menu_company()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

import streamlit as st
import re
import yaml
import streamlit_authenticator as stauth
import pandas as pd


# sidebar page links
def authenticated_menu_user():
    st.sidebar.empty()
    st.sidebar.page_link("pages/1_Listings.py", label="Companies List")
    st.sidebar.page_link("pages/2_PortfolioAnalyser.py", label="Portfolio Analyser")
    if 'username' in st.session_state and st.session_state.username is not None:
        authenticator = st.session_state.get('authenticator')
        st.sidebar.page_link("pages/8_UserAccount.py", label="My Account")
        st.sidebar.page_link("pages/12_SellStocks.py", label="Sell Shares")
        st.sidebar.page_link("pages/13_UploadPortfolio.py", label="Upload External Portfolio")
        st.sidebar.page_link("pages/14_TargetSection.py", label="Set Target")
        with st.sidebar:
            authenticator.logout('Logout', 'main', key='unique_key')     
    else:
        st.sidebar.page_link("pages/5_LoginUser.py", label="Login")
        st.sidebar.page_link("pages/6_SignupUser.py", label="Signup")  
        
# Function to validate email format
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

# Function to write data to YAML file
def write_to_yaml(data):
    with open('user_details.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

# Function to read YAML file
def read_yaml():
    try:
        with open('user_details.yaml', 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        return data
    except FileNotFoundError:
        return {}

def signup():
    st.title("Sign Up")

    # Input fields for name, email, username, and password
    name = st.text_input("Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Button to submit the signup form
    if st.button("Sign Up"):
        # Validate if all fields are not empty
        if name and email and username and password:
            # Check email format consistency
            if validate_email(email):
                # Hash the password
                hashed_password = stauth.Hasher([password]).generate()
                # binary_hashed_password = hashed_password[0].encode()

                # Load existing data or create a new dictionary if the file doesn't exist
                user_data = read_yaml()
                if user_data is None:
                    user_data = {}

                if 'credentials' not in user_data:
                    user_data['credentials'] = {'usernames': {}}
                    user_data['cookie'] = {'expiry_days': 30,
                                           'key': 'abc',
                                           'name': 'cookie'}
                    user_data['preauthorized'] = {'emails': ['o_chopra@ee.iitr.ac.in']}

                # Add user details to the dictionary
                user_data['credentials']['usernames'][username] = {
                    'email': email,
                    'name': name,
                    'password': hashed_password[0],
                    'balance': 10000,
                    'transaction_history':None,
                    'current_portfolio': None
                }

                # Write user details to YAML file
                write_to_yaml(user_data)
                st.success("You have successfully signed up!")
            else:
                st.error("Please enter a valid email address.")
        else:
            st.error("All fields are required.")

if __name__ == "__main__":
    signup()
    authenticated_menu_user()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

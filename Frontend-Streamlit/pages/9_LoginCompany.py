import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

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

# Create the authenticator object
authenticator = stauth.Authenticate(
    company_data['credentials'],
    'company_cookie',
    'company_key',
    30,
    {}
)

def company_login():
            
    name, authentication_status, username = authenticator.login()
    if authentication_status:
        company_ticker=username
        company_details = company_data['credentials']['usernames'].get(company_ticker, {})
        st.session_state['authenticator']=authenticator
        st.session_state['company_ticker']=username
        st.session_state['company'] = company_details
        st.switch_page("Landing.py")
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')


if __name__ == "__main__":
    company_login()
    
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

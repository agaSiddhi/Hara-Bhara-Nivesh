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

# Import the YAML file into your script
user_data=read_yaml('user_details.yaml')

# Create the authenticator object
authenticator = stauth.Authenticate(
    user_data['credentials'],
    user_data['cookie']['name'],
    user_data['cookie']['key'],
    user_data['cookie']['expiry_days'],
    user_data['preauthorized']
)

def main():
    # Render the login module
    name, authentication_status, username = authenticator.login()
    if authentication_status:
        st.session_state['authenticator']=authenticator
        st.switch_page("Landing.py")
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    main()


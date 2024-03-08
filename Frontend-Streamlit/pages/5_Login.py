import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st

# Import the YAML file into your script
with open('user_details.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

def main():
    # Render the login module
    name, authentication_status, username = authenticator.login()
    if authentication_status:
        authenticator.logout('Logout', 'main', key='unique_key')
        st.write(f'Welcome *{name}*')
        st.title('Some content')
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

if __name__ == "__main__":
    main()


import streamlit_authenticator as stauth
import streamlit as st

from backend.configuration import initialize_system
user_service = initialize_system()[1]

authenticator = stauth.Authenticate(
    user_service.get_user_data_dict(),
    'company_cookie',
    'company_key',
   30,
    {}
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

    main()
    
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")


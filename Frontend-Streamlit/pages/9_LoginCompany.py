import streamlit_authenticator as stauth
import streamlit as st

from backend.configuration import initialize_system
company_service = initialize_system()[0]

# Create the authenticator object
authenticator = stauth.Authenticate(
    company_service.get_company_data_dict(),
    'company_cookie',
    'company_key',
    30,
    {}
)

def main():
    name, authentication_status, username = authenticator.login()
    print("Authentication status:",authentication_status, "username",username,'name', name)
    if authentication_status:
        company_ticker=username
        st.session_state['authenticator']=authenticator
        st.session_state['company_ticker']=username
        company_details = company_service.return_signup_company_data(username.upper())
        st.session_state['company'] = company_details
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

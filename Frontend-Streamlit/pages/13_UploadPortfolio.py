import streamlit as st
import pandas as pd

from backend.configuration import initialize_system
user_service = initialize_system()[1]



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

@st.cache_data
def save_uploaded_file(uploaded_file,username):
    uploaded = pd.read_excel(uploaded_file)
        
    user_service.add_uploaded_file_to_current_portfolio(uploaded)

def main():

    st.title('Upload External Portfolio')
    uploaded_file= st.file_uploader('Upload your portfolio here', type=['xlsx'])

    if uploaded_file is not None:
        
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = uploaded_file

        # Save excel file
        save_uploaded_file(uploaded_file,username)


if __name__ == "__main__":
    if 'username' in st.session_state and st.session_state.username is not None:
        username = st.session_state.get('username')
        main()
    else:
        st.warning("Please login to upload external portfolio")
        
    authenticated_menu_user()
    #back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
        
        
    

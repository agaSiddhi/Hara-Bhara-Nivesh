import streamlit as st
import random
import pandas as pd
from backend.configuration import initialize_system

company_service = initialize_system()

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
        
def get_fund_categories():
    st.write("Which category fund(s) would you like to invest in?")
    selected_categories = []
    categories = ['Equity', 'Debt', 'Hybrid', 'Others']
    for category in categories:
        if st.checkbox(category):
            selected_categories.append(category)
    return selected_categories

# Function to get user input for interested sectors
def get_interested_sectors():
    st.write("Which sector fund(s) would you like to invest in?")
    selected_sectors = []
    sectors = ['Capital Goods', 'HealthCare', 'Financial', 'Services', 'Consumer Staples', 'Other']
    for sector in sectors:
        if st.checkbox(sector):
            selected_sectors.append(sector)
    return selected_sectors

def main():
    current_score = st.session_state['current_score']
    
    # Page title
    st.title('Wanna Set Your Target!')    
    
    # Main function for the target section
    target_score = st.number_input("Enter your score target:")
    if current_score < target_score:
        placeholder = st.empty()
        suggestions_button = None
        with placeholder.container():
            selected_categories = get_fund_categories()
            selected_sectors = get_interested_sectors()
            if selected_categories and selected_sectors:
                suggestions_button = st.button("Get Suggestions")
            st.write("---")

        if suggestions_button:
            placeholder.empty()
            filtered_companies =company_service.filter_companies(selected_categories,selected_sectors)
            print(filtered_companies)
            for company_id, company_info in filtered_companies.items():
                company_name = company_id  # Assuming the company name is the same as the ID
                category = company_info['category']
                sector = company_info['sector']
                average_score = company_info['score']
                
                col1, col2 = st.columns([3, 1])
                col1.markdown(f"#### {company_name}")
                col1.write(f"{category} ● {sector}")
                col2.markdown(f"##### Average score: {average_score}")
                st.write("---")


    else:
        st.write("Hurray!! You meet your sustainability Targets")
        st.write("---")
        

if __name__ == "__main__":
    main()
    authenticated_menu_user()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

import streamlit as st

# Define a list of companies
from backend.configuration import initialize_system
company_service = initialize_system()[0]
details = company_service.return_company_name_and_description()

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
        
# Create a Streamlit app
def main():
    
    # Page title    
    st.title("Top Sustainable Companies")

    # Search bar
    search_term = st.text_input("", placeholder="Enter Company Name")
    search_button = st.button("Search")

    filtered_companies = [company for company in details.keys() if search_term.lower() in company.lower()]

    # Filter companies based on search term
    for company in filtered_companies:
        company_detail = details[company]
        company_name = f"{company_detail[2]}. {company}"
        st.subheader(company_name)
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(company_detail[1])
        col2.write(company_detail[0])

        # Add detail button to view company details
        button_label = "Details"
        button_key = f"{button_label}_{company_name}"
        if col3.button(button_label, key=button_key):
            st.session_state['company'] = company
            st.switch_page("pages/details_page.py") 
    



if __name__ == "__main__":
    authenticated_menu_user()
    main()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

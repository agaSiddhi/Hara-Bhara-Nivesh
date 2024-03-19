import streamlit as st
from backend.configuration import initialize_system

curr_price = {
'AAPL':10,
'GOOGL':20,
'MSFT':30,
'AMZN':40,
'JPM':50,
'BRK.A':12,
'FB':11,
'NFLX':54,
}

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
        
        
def main():
    st.title("Sell Shares")
    user_service= initialize_system()[1]
    company_names = [company for company, shares in shares.items() if shares > 0]
    selected_company = st.selectbox("Select a company to sell shares:", company_names)
    quantity = st.number_input(f"Enter quantity to sell for {selected_company}:", min_value=0, max_value=int(shares[selected_company]), step=1)
    
    # Display company details and allow user to select quantity
    st.write(f"Company: {selected_company}")
    st.write(f"Number of shares owned: {shares[selected_company]}")
    
    # Button to sell shares
    if st.button("Sell"):
        company_details = {
            'name': selected_company,
            'price_per_stock': user_service.get_current_price_for_ticker(selected_company)  # You can fetch the actual price from your data source
        }
        user_service.sell_stock(shares, company_details, quantity)

if __name__ == "__main__":
    if 'username' in st.session_state and st.session_state.username is not None:
        username = st.session_state.get('username')
        if 'shares' in st.session_state:
            shares = st.session_state.get('shares')
            main()
        else:
            st.warning("Your portfolio is empty")
    else:
        st.warning("Login to buy stocks")
        
    authenticated_menu_user()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
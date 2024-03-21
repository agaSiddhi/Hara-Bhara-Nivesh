import streamlit as st
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit_shadcn_ui as ui
from streamlit_option_menu import option_menu
from backend.configuration import initialize_system
# company names from ticker 
company_service=initialize_system()[0]
user_service=initialize_system()[1]
company_mapping = company_service.return_company_name_from_ticker()

# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=SafeLoader)
        return data
    except FileNotFoundError:
        return {}
    
    
# Import the user details into your script

user_data = read_yaml('user_details.yaml')

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

def my_account():

    if 'username' in st.session_state and st.session_state.username is not None:
            
        username = st.session_state.get('username')
        authentication_status = st.session_state.get('authentication_status')
        authenticator = st.session_state.get('authenticator')
        user_image_url = '../assets/username.jpeg'
        current_portfolio = user_service.get_portfolio_entry_for_user(username)
        stocks=None
        if current_portfolio is not None and len(current_portfolio)>0:
            current_portfolio = pd.DataFrame(current_portfolio)
            current_portfolio['Date'] = pd.to_datetime(current_portfolio['Date'],infer_datetime_format=True)
            shares, stocks, invested, current,data = user_service.calculate_portfolio_balance(current_portfolio)
        
        # --- NAVIGATION MENU ---
        selected = option_menu(
            menu_title=None,
            options=["My Account","Investments", "Transaction History"],
            icons=["person-fill","bar-chart-fill","currency-exchange"],  # https://icons.getbootstrap.com/
            orientation="horizontal",
            menu_icon="cast",
            styles={    
            "nav-link-selected": {"background-color": "#2B8C0C"},
            }   
        )
        
        
        if selected=="My Account":
                
            # Display user image and name on the main page
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(user_image_url, caption=username, use_column_width=True)
            
            st.subheader(f"{user_service.get_name_from_username(username)}")

            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Email Address: {user_service.get_mail(username)}")
            with col2:
                st.write(f"Wallet Balance : {user_service.get_wallet_balance(username)}")
            st.write("---")
            add_vertical_space(2)
            if stocks is not None:
                st.subheader("Your ideal portfolio should look like this!")
                add_vertical_space(2)
                for ticker,amount in stocks.items():
                    if amount<=0:
                        continue
                    category = company_service.return_fund_category_from_ticker(ticker)
                    sector = company_service.return_industry_keyword_from_companyID(ticker)
                    selected_category=[category[0][0]]
                    selected_sector=[sector[0][0]]
                    filtered_companies =company_service.filter_companies(selected_category,selected_sector)
                    col1,col2 = st.columns([3,1])
                    if len(filtered_companies)!=0:
                        suggested_ticker=next(iter(filtered_companies))
                        details=filtered_companies[suggested_ticker]
                        score = round(details[next(iter(details))],2)
                        col1.markdown(f"### {suggested_ticker}")
                    else:
                        score = round(company_service.return_average_score_from_ticker(ticker),2)
                        col1.markdown(f"#### {suggested_ticker}")
                        
                    col2.markdown(f'##### {score}')
                    st.write('---')
                        
                    
        
        if selected=="Investments":
            # show investment summary
            st.subheader(f"Investments")

            if stocks is not None:
                st.session_state.shares=shares
                returns = (float(current)-float(invested))/float(invested)
                col1, col2, col3 = st.columns(3)
                col1.info(f"Current: ${current:.7}")
                if returns>0:
                    col2.success(f"Total Returns: {returns:.2%}")
                else:
                    col2.warning(f"Total Returns: {returns:.2%}")
                col3.info(f"Invested: ${invested:.6}")
                add_vertical_space(2)
                for ticker, amount in stocks.items():
                    if amount==0:
                        continue
                    company_name = company_mapping[ticker]
                    col1,col2 = st.columns([3,1])
                    col1.markdown(f"### {company_name}")
                    col2.markdown(f'### ${amount:.6}')
                    st.write('---')
                # st.write(current_portfolio)
            else:
                st.warning("You haven't made any investments yet!!")
                st.write("---")
        
            add_vertical_space(2)

        if selected=="Transaction History":
            # show transaction history
            st.subheader(f"Transaction History")

            transaction_history = user_service.get_transaction_history(username)
            if transaction_history is not None and len(transaction_history)>0:                # Iterate over each transaction
                initial = 10000
                i=1
                for index, row in transaction_history.iterrows():
                    ticker = row['Ticker']
                    date = row['Date']
                    qty = row ['Amount']
                    type = row['Order Type']
                    price = row['Price/Quote']
                    if(type=='Buy'):
                        diff=-qty*price
                    else:
                        diff=qty*price
                    percent = diff/initial
                    balance=initial+diff
                    company_name = company_mapping[ticker]
                    st.write(date)
                    ui.metric_card(title=company_name, content=f"{qty} shares", description=f"{percent:.2%} Amount Left in Wallet: {balance}", key=f"card{i}")
                    initial=balance
                    add_vertical_space(2)
                    i=i+1
            else:
                st.warning("You haven't made any transactions yet!!")
        
        
    else:
        st.warning("Please login to get your account details")



if __name__ == "__main__":
    my_account()
    
    authenticated_menu_user()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
        
        

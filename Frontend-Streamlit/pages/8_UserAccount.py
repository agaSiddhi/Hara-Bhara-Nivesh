import streamlit as st
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space
import streamlit_shadcn_ui as ui

# company names from ticker 
company_mapping = {'AAPL': 'Apple','GOOGL':'Google','MSFT':'Microsoft','AMZN':'Amazon','FB':'Facebook','NFLX':'Netflix'}

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

def get_name(username):
    return user_data['credentials']['usernames'][username]['name']

def get_mail(username):
    return user_data['credentials']['usernames'][username]['email']

def get_walletBalance(username):
    return user_data['credentials']['usernames'][username]['balance']

def get_transactionHistory(username):
    return user_data['credentials']['usernames'][username]['transaction_history']

def get_portfolio(username):
    return user_data['credentials']['usernames'][username]['current_portfolio']

def calculate_portfolio_balance(data):
    # Initialize portfolio balance
    portfolio_amount = []
    portfolio_value = []
    current_portfolio = 0
    
    dates = pd.date_range(start=min(data['Date']), end=max(data['Date']))
    tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB','NFLX']
    stocks = {ticker: 0 for ticker in tickers}
    shares = {ticker: 0 for ticker in tickers}
    
    
    prices = np.random.randint(100, 500, size=(len(dates), len(tickers)))  # Generating random prices -> this is something we ll get from the database

    # Create the DataFrame
    df = pd.DataFrame(prices, index=dates, columns=tickers)

    for index, row in data.iterrows():
        current_value = 0
        if row['Order Type'] == 'Buy':
            current_portfolio += row['Amount'] * row['Price/Quote']
            shares[row['Ticker']]+=row['Amount']
        elif row['Order Type'] == 'Sell':
            current_portfolio -= row['Amount'] * row['Price/Quote']
            shares[row['Ticker']]-=row['Amount']
        for ticker, value in shares.items():
            current_value += value * df.loc[row['Date']][ticker]
            
    for ticker, amount in shares.items():
        stocks[ticker]=amount*df.iloc[-1][ticker]

    return shares,stocks, current_portfolio, current_value


def my_account():

    if 'username' in st.session_state and st.session_state.username is not None:
        
        username = st.session_state.get('username')
        authentication_status = st.session_state.get('authentication_status')
        authenticator = st.session_state.get('authenticator')
        user_image_url = 'assets/username.jpeg'

        # Display user image and name on the main page
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(user_image_url, caption=username, use_column_width=True)
        
        st.subheader(f"{get_name(username)}")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Email Address: {get_mail(username)}")
        with col2:
            st.write(f"Wallet Balance : {get_walletBalance(username)}")
        st.write("---")
        add_vertical_space(2)
        
        # show investment summary
        st.subheader(f"Investments")

        current_portfolio = get_portfolio(username)
        if current_portfolio is not None:
            current_portfolio = pd.DataFrame(current_portfolio)
            current_portfolio['Date'] = pd.to_datetime(current_portfolio['Date'],infer_datetime_format=True)
            shares, stocks, invested, current = calculate_portfolio_balance(current_portfolio)
            returns = (current-invested)/invested
            col1, col2, col3 = st.columns(3)
            col1.info(f"Current: ${current}")
            if returns>0:
                col2.success(f"Total Returns: {returns:.2%}")
            else:
                col2.warning(f"Total Returns: {returns:.2%}")
            col3.info(f"Invested: ${invested}")
            add_vertical_space(2)
            for ticker, amount in stocks.items():
                if amount==0:
                    continue
                company_name = company_mapping[ticker]
                col1,col2 = st.columns([3,1])
                col1.markdown(f"### {company_name}")
                col2.markdown(f'### ${amount}')
                st.write('---')
            # st.write(current_portfolio)
        else:
            st.warning("You haven't made any investments yet!!")
            st.write("---")
        
        # Button to upload external portfolio
        upload_portfolio = st.button("Upload External Portfolio")
        if upload_portfolio:
            st.switch_page("pages/upload_portfolio.py")
        add_vertical_space(2)

        # show transaction history
        st.subheader(f"Transaction History")

        transaction_history = get_transactionHistory(username)

        if transaction_history is not None:
            transaction_history = pd.DataFrame(transaction_history, columns=['Date','Order Type','Ticker','Amount','Price/Quote','Wallet Balance'])
            # Iterate over each transaction
            initial = 10000
            i=1
            for index, row in transaction_history.iterrows():
                ticker = row['Ticker']
                date = row['Date']
                qty = row ['Amount']
                wallet = row['Wallet Balance']
                diff = wallet-initial
                percent = diff/initial
                company_name = company_mapping[ticker]
                st.write(date)
                ui.metric_card(title=company_name, content=f"{qty} shares", description=f"{percent:.2%} Amount Left in Wallet: {wallet}", key=f"card{i}")
                initial=wallet
                add_vertical_space(2)
                i=i+1
            # st.write(transaction_history)
        else:
            st.warning("You haven't made any transactions yet!!")
        
        # Sell stocks functionality
        if st.button("Sell"):
            st.session_state['shares']=shares
            st.switch_page("pages/sell_stocks.py")
        
            


    
    else:
        st.warning("Please login to get your account details")



if __name__ == "__main__":
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    my_account()

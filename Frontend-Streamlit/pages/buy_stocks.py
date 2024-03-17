import streamlit as st
from backend.configuration import initialize_system
import yaml
from yaml.loader import SafeLoader
import pandas as pd

retail_volume = {
'AAPL':1000,
'GOOGL':1000,
'MSFT':1000,
'AMZN':1000,
'JPM':1000,
'BRK.A':1000,
'FB':1000,
'NFLX':1000,
}

position_limit = {
'AAPL':10,
'GOOGL':10,
'MSFT':10,
'AMZN':10,
'JPM':10,
'BRK.A':10,
'FB':10,
'NFLX':10,
}

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

# Function to read YAML file
def read_yaml(filename):
    try:
        with open(filename, 'r') as file:
            data = yaml.load(file, Loader=SafeLoader)
        return data
    except FileNotFoundError:
        return {}
    
def get_price(company_id):
    return curr_price[company_id]
    
# Import the user details into your script
user_data = read_yaml('user_details.yaml')

# Function to calculate the total price based on quantity and price per stock
def calculate_price(quantity, price_per_stock):
    return quantity * price_per_stock

def get_walletBalance(username):
    return user_data['credentials']['usernames'][username]['balance']

def get_transaction_history(username):
    return user_data['credentials']['usernames'][username]['transaction_history']

def get_portfolio(username):
    return user_data['credentials']['usernames'][username]['current_portfolio']

def update_wallet(user_wallet):
    # update user wallet balance
    user_data['credentials']['usernames'][username]['balance']=user_wallet
    
def update_transaction_history(company_id,quantity,price_per_stock,user_wallet):
    # update user transaction history

    new_transaction = [{'Date':'29-02-24','Order Type':'Buy','Ticker':company_id,'Amount':quantity,'Price/Quote':price_per_stock,'Wallet Balance':user_wallet}]
    new_transaction=pd.DataFrame(new_transaction)
    new_transaction['Date'] = pd.to_datetime(new_transaction['Date'],infer_datetime_format=True)
    
    curr_history = get_transaction_history(username)
    curr_history = pd.DataFrame(curr_history, columns=['Date','Order Type','Ticker','Amount','Price/Quote','Wallet Balance'])
    curr_history['Date'] = pd.to_datetime(curr_history['Date'],infer_datetime_format=True)
        
    # Concatenate the two DataFrames
    new = pd.concat([curr_history,new_transaction ])
    df = new.sort_values(by='Date')
    #Using dt.strftime() method by passing the specific string format as an argument.
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y') 
    user_data['credentials']['usernames'][username]['transaction_history']=df.to_dict('list')
    
def update_portfolio(company_id,quantity,price_per_stock):
    # update user transaction history
    curr_portfolio = get_portfolio(username)
    curr_portfolio = pd.DataFrame(curr_portfolio, columns=['Date','Order Type','Ticker','Amount','Price/Quote'])
    curr_portfolio['Date'] = pd.to_datetime(curr_portfolio['Date'],infer_datetime_format=True)
    new_transaction = [{'Date':'29-02-24','Order Type':'Buy','Ticker':company_id,'Amount':quantity,'Price/Quote':price_per_stock}]
    new_transaction=pd.DataFrame(new_transaction)
    new_transaction['Date'] = pd.to_datetime(new_transaction['Date'],infer_datetime_format=True)
    # Concatenate the two DataFrames
    new = pd.concat([curr_portfolio,new_transaction])
    df = new.sort_values(by='Date')
    #Using dt.strftime() method by passing the specific string format as an argument.
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
    user_data['credentials']['usernames'][username]['current_portfolio']=df.to_dict('list')

# Function to handle the buy functionality
def buy_stock(username, quantity, company_id):
    user_wallet = get_walletBalance(username)

    price_per_stock = get_price(company_id)
    
    total_price = calculate_price(quantity, price_per_stock)
    
    if total_price > user_wallet:
        st.warning("Not enough balance in your wallet. Current wallet balance: ${user_wallet}")
    else:
        user_wallet -= total_price
        st.success(f"Successfully bought {quantity} stocks of {company_name} for ${total_price}.")
        st.write(f"Remaining balance in your wallet: ${user_wallet}")
        
        update_wallet(user_wallet)
        update_transaction_history(company_id,quantity,price_per_stock,user_wallet)
        update_portfolio(company_id,quantity,price_per_stock)
        
        # Save the updated YAML file
        with open('user_details.yaml', 'w') as file:
            yaml.dump(user_data, file)
            
        

def main():
    company_service = initialize_system()
    company_id = company_service.return_companyID_from_company_name(company_name)[0][0]

    st.subheader(f"Buy: {company_name}")
    st.write(f"Price per stock: ${get_price(company_id)}")
    quantity = st.number_input("Enter quantity to buy:", min_value=position_limit[company_id], max_value=retail_volume[company_id], step=1)

    # Button to buy stocks
    if st.button("Buy"):
        buy_stock(username, quantity, company_id)

if __name__ == "__main__":
    col1,col2 = st.columns(2)
    if 'username' in st.session_state and st.session_state.username is not None:
        username = st.session_state.get('username')
        company_name = st.session_state.get('company')
        main()
        if col2.button("Go Back"):
            st.switch_page("pages/details_page.py")
    else:
        st.warning("Login to buy stocks")
        # back to home
    
    if col1.button("Back to Home"):
        st.switch_page("Landing.py")
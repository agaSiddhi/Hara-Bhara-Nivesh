import streamlit as st
from backend.configuration import initialize_system
import yaml
from yaml.loader import SafeLoader
import pandas as pd

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
        
# Function to read YAML file
# def read_yaml(filename):
#     try:
#         with open(filename, 'r') as file:
#             data = yaml.load(file, Loader=SafeLoader)
#         return data
#     except FileNotFoundError:
#         return {}
    
# def get_price(company_id):
#     return curr_price[company_id]

# def get_walletBalance(username):
#     return user_data['credentials']['usernames'][username]['balance']

# def get_transaction_history(username):
#     return user_data['credentials']['usernames'][username]['transaction_history']

# def get_portfolio(username):
#     return user_data['credentials']['usernames'][username]['current_portfolio']

# # Import the user details into your script
# user_data = read_yaml('user_details.yaml')

# def update_wallet(user_wallet):
#     # update user wallet balance
#     user_data['credentials']['usernames'][username]['balance']=user_wallet
    
# def update_transaction_history(company_id,quantity,price_per_stock,user_wallet):
#     # update user transaction history

#     new_transaction = [{'Date':'29-02-24','Order Type':'Sell','Ticker':company_id,'Amount':quantity,'Price/Quote':price_per_stock,'Wallet Balance':user_wallet}]
#     new_transaction=pd.DataFrame(new_transaction)
#     new_transaction['Date'] = pd.to_datetime(new_transaction['Date'],infer_datetime_format=True)
    
#     curr_history = get_transaction_history(username)
#     curr_history = pd.DataFrame(curr_history, columns=['Date','Order Type','Ticker','Amount','Price/Quote','Wallet Balance'])
#     curr_history['Date'] = pd.to_datetime(curr_history['Date'],infer_datetime_format=True)
        
#     # Concatenate the two DataFrames
#     new = pd.concat([curr_history,new_transaction])
#     df = new.sort_values(by='Date')
#     #Using dt.strftime() method by passing the specific string format as an argument.
#     df['Date'] = df['Date'].dt.strftime('%d-%m-%Y') 
#     user_data['credentials']['usernames'][username]['transaction_history']=df.to_dict('list')
    
# def update_portfolio(company_id,quantity,price_per_stock):
#     # update user transaction history
#     curr_portfolio = get_portfolio(username)
#     curr_portfolio = pd.DataFrame(curr_portfolio, columns=['Date','Order Type','Ticker','Amount','Price/Quote'])
#     curr_portfolio['Date'] = pd.to_datetime(curr_portfolio['Date'],infer_datetime_format=True)
#     new_transaction = [{'Date':'29-02-24','Order Type':'Sell','Ticker':company_id,'Amount':quantity,'Price/Quote':price_per_stock}]
#     new_transaction=pd.DataFrame(new_transaction)
#     new_transaction['Date'] = pd.to_datetime(new_transaction['Date'],infer_datetime_format=True)
#     # Concatenate the two DataFrames
#     new = pd.concat([ curr_portfolio,new_transaction])
#     df = new.sort_values(by='Date')
#     #Using dt.strftime() method by passing the specific string format as an argument.
#     df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
#     user_data['credentials']['usernames'][username]['current_portfolio']=df.to_dict('list')
    
    
# # Function to calculate the total price based on quantity and price per stock
# def calculate_price(quantity, price_per_stock):
#     return quantity * price_per_stock

# # Function to handle the sell functionality
# def sell_stock(user_shares, company_details, quantity):
#     company_name = company_details['name']
#     price_per_stock = company_details['price_per_stock']
    
#     if company_name in user_shares:
#         available_shares = user_shares[company_name]
#         if quantity <= available_shares:
#             total_price = calculate_price(quantity, price_per_stock)
#             user_shares[company_name] -= quantity
#             st.success(f"Successfully sold {quantity} shares of {company_name} for ${total_price}.")
#             st.write(f"Remaining shares of {company_name}: {user_shares[company_name]}")
            
#             # update user wallet
#             user_wallet = get_walletBalance(username)
#             user_wallet = user_wallet+total_price
#             update_wallet(user_wallet)
            
#             # update transaction history
#             update_transaction_history(company_name,quantity,price_per_stock,user_wallet)
            
#             # update portfolio
#             update_portfolio(company_name,quantity,price_per_stock)
            
#             # Save the updated YAML file
#             with open('user_details.yaml', 'w') as file:
#                 yaml.dump(user_data, file)
            
#         else:
#             st.warning("You don't have enough shares to sell.")
#     else:
#         st.warning("You don't own any shares of this company.")
        
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
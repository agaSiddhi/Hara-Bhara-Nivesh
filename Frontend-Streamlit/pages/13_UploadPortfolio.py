import streamlit as st
import yaml
from yaml.loader import SafeLoader
import pandas as pd

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
    uploaded['Date'] = pd.to_datetime(uploaded['Date'],infer_datetime_format=True)
    current = user_data['credentials']['usernames'][username]['current_portfolio']
    current = pd.DataFrame(current, columns=['Date','Order Type','Ticker','Amount','Price/Quote'])
    current['Date'] = pd.to_datetime(current['Date'],infer_datetime_format=True)
    # Concatenate the two DataFrames
    new = pd.concat([current,uploaded])
    df = new.sort_values(by='Date')
    #Using dt.strftime() method by passing the specific string format as an argument.
    df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
    user_data['credentials']['usernames'][username]['current_portfolio']=df.to_dict('list')
    # Save the updated YAML file
    with open('user_details.yaml', 'w') as file:
        yaml.dump(user_data, file)

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
        
        
    

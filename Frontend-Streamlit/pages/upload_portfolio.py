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
    if st.button("Go Back"):
        st.switch_page("pages/8_UserAccount.py")

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

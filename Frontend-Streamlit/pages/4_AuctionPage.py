import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Mock data for demonstration
data = {
    'Ticker': ['AAPL', 'GOOGL', 'MSFT'],
    'Name': ['Apple Inc.', 'Alphabet Inc.', 'Microsoft Corporation'],
    'Initial Bid': [100, 200, 150],
    'Minimum Step': [10, 20, 15],
    'Credits Listed': [5000, 3000, 4000],
    'Description': ['Description of Apple Inc.','Description of Alphabet Inc.','Description of Microsoft Corporation'],
    'Bids':[[],[],[]],
    'Industry':['Capital Goods','Financial','Services']
}

df = pd.DataFrame(data)

def get_current_price(company):
    if company['Bids']:
        return max(company['Bids'], key=lambda x: x['Bid'])['Bid']
    else:
        return company['Initial Bid']


def filter_companies(search_query, data):
    return data[data['Name'].str.contains(search_query, case=False)]

def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    
    # --- HIDE STREAMLIT STYLE ---
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["CER", "VER"],
        icons=["pencil-fill", "bar-chart-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # --- CER Tab ---
    if selected == "CER":

        # Search bar with search icon
        search_query = st.text_input('Search Companies:', value='', key='search_input')
        # Dropdown for filtering by industry
        selected_industries = st.multiselect('Filter by Industry:', options=df['Industry'].unique())
        filtered_df = filter_companies(search_query, df)
        # Apply industry filter
        if selected_industries:
            filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industries)]
        # Display listings
        if len(filtered_df) == 0:
            st.write('No results found.')
        else:
            for index, row in filtered_df.iterrows():
                st.subheader(f"**{row['Name']}**")
                col1,col2,col3 = st.columns([1,1,0.5])
                col1.markdown(f"##### Current Price: ${get_current_price(row)}")
                col2.markdown(f"##### Credits Listed: {row['Credits Listed']}")
                # Add detail button to view company details
                button_label = "Details"
                button_key = f"{button_label}_{row['Name']}_CER"
                if col3.button(button_label, key=button_key):
                    st.session_state['company'] = row
                    st.switch_page("pages/cer_details_page.py") 
                st.write("---")

    # --- VER Tab ---
    if selected == "VER":

        # Search bar with search icon
        search_query = st.text_input('Search Companies:', value='', key='search_input')
        # Dropdown for filtering by industry
        selected_industries = st.multiselect('Filter by Industry:', options=df['Industry'].unique())
        filtered_df = filter_companies(search_query, df)
        # Apply industry filter
        if selected_industries:
            filtered_df = filtered_df[filtered_df['Industry'].isin(selected_industries)]
        # Display listings
        if len(filtered_df) == 0:
            st.write('No results found.')
        else:
            for index, row in filtered_df.iterrows():
                st.subheader(f"**{row['Name']}**")
                col1,col2,col3 = st.columns([1,1,0.5])
                col1.markdown(f"##### Current Price: ${get_current_price(row)}")
                col2.markdown(f"##### Credits Listed: {row['Credits Listed']}")
                # Add detail button to view company details
                button_label = "Details"
                button_key = f"{button_label}_{row['Name']}_VER"
                if col3.button(button_label, key=button_key):
                    st.session_state['company'] = row
                    st.switch_page("pages/ver_details_page.py") 
                st.write("---")
        



if __name__ == "__main__":
    main()





import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import matplotlib.colors as mcolors
import yaml
from yaml.loader import SafeLoader

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

def get_portfolio(username):
    return user_data['credentials']['usernames'][username]['current_portfolio']
from backend.configuration import initialize_system
company_service = initialize_system()

def load_excel(file):
    df = pd.read_excel(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    return df

@st.cache_data
def save_uploaded_file(uploaded_file):
    return uploaded_file

# Create a Streamlit app
def main():
    # Page title
    
    st.title('Investment Portfolio Analyzer')
    
    # if 'uploaded_file' in st.session_state:
    #     uploaded_file=st.session_state.get("uploaded_file")
    #     new_uploaded_file= st.file_uploader('Upload your portfolio here', type=['xlsx'])
    #     if new_uploaded_file is not None:
    #         uploaded_file= new_uploaded_file
    #         st.session_state.uploaded_file = uploaded_file
    # else:
    #     uploaded_file= st.file_uploader('Upload your portfolio here', type=['xlsx'])
     
    
     
    # if uploaded_file is not None:
    #     # Load excel file
    #     if 'uploaded_file' not in st.session_state:
    #         st.session_state.uploaded_file = uploaded_file
    #     portfolio = load_excel(uploaded_file)
        
    portfolio = pd.DataFrame(current_portfolio)
    portfolio['Date'] = pd.to_datetime(portfolio['Date'],infer_datetime_format=True)
    ## ----- Price and Score History

    # Price History

    stocks, portfolio = company_service.calculate_portfolio_balance(portfolio)
    fig1 = px.line(portfolio, x='Date', y=['Invested Amount', 'Portfolio Value'], 
            labels={'Date': 'Date', 'value': 'Amount/Value'}, 
            title='Portfolio Amount and Value Over Time')
    fig1.update_layout(title_x=0.3)
    st.plotly_chart(fig1)

    # Score History
    
    current_score, portfolio = company_service.calculate_portfolio_score(portfolio)
    fig2 = px.line(portfolio, x='Date', y=['Score'], 
            labels={'Date': 'Date', 'value': 'Score'}, 
            title='Portfolio Score Over Time')
    fig2.update_layout(title_x=0.4)
    st.plotly_chart(fig2)
    
    ## ----- Distribution of Stock Categories

    category_percentage= company_service.return_category_percentage(stocks)

    # Convert dictionary to lists for plotting
    categories = list(category_percentage.keys())
    percentages = list(category_percentage.values())

    # Plotting the horizontal bar graph with shades of blue
    fig, ax = plt.subplots()

    # Convert colormap to color names
    cmap = plt.get_cmap('Greens')
    colors = [mcolors.to_hex(cmap(i)) for i in np.linspace(0.2, 1, len(categories))]

    # Plot the horizontal bar graph
    y_pos = np.arange(len(categories))
    bar_height = 0.5  # Adjust the bar height here
    ax.barh(y_pos, percentages, color=colors, height=bar_height)

    # Add labels and title
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    st.write("---")
    st.markdown("### Distribution of Stock Categories")

    # Display the plot using Streamlit
    st.pyplot(fig)

    col1, col2, col3,col4 = st.columns([0.6, 3, 1, 0.5])
    # Iterate over category_percentage dictionary
    for category, percentage in category_percentage.items():
        # Display colored box in col1
        with col1:
            st.markdown(f'<div style="background-color: {colors[categories.index(category)]}; width: 30px; height: 30px; margin-top: 15px; margin-bottom: 9px;border-radius: 5px"></div> ', unsafe_allow_html=True)
        
        # Display category name in col2
        with col2:
            st.markdown(f"#### {category}")

        # Display percentage in col3
        with col3:
            st.markdown(f"#### {percentage:.2%}")
        

        button_label = "→"
        button_key = f"{button_label}_{category}"

        # Display more details in col4
        if col4.button(button_label, key=button_key ):
            st.session_state['category'] = category
            st.session_state['stocks'] = stocks
            st.switch_page("pages/categories_page.py") 


    ## ----- Distribution of Stock Industries
            
    industry_percentage=company_service.return_industry_percentage(stocks)

    # Convert dictionary to lists for plotting
    industries = list(industry_percentage.keys())
    percentages = list(industry_percentage.values())

    # Plotting the horizontal bar graph with shades of blue
    fig, ax = plt.subplots()

    # Convert colormap to color names
    cmap = plt.get_cmap('Reds')
    colors = [mcolors.to_hex(cmap(i)) for i in np.linspace(0.2, 1, len(industries))]

    # Plot the pie chart with a hole inside
    fig, ax = plt.subplots()

    # Outer pie chart
    wedges, texts, autotexts = ax.pie(percentages, colors=colors, autopct='%1.1f%%', startangle=360, wedgeprops=dict(width=0.3), pctdistance=0.85)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.set_aspect('equal')
    st.write("---")
    st.markdown("### Allocation of Stock Industries")

    # Display the plot using Streamlit
    st.pyplot(fig)

    col1, col2, col3,col4 = st.columns([0.6, 3, 1, 0.5])
    # Iterate over category_percentage dictionary
    for industry, percentage in industry_percentage.items():
        # Display colored box in col1
        with col1:
            st.markdown(f'<div style="background-color: {colors[industries.index(industry)]}; width: 30px; height: 30px; margin-top: 15px; margin-bottom: 9px;border-radius: 5px"></div> ', unsafe_allow_html=True)
        
        # Display category name in col2
        with col2:
            st.markdown(f"#### {industry}")

        # Display percentage in col3
        with col3:  
            st.markdown(f"#### {percentage:.2%}")

        button_label = "→"
        button_key = f"{button_label}_{industry}"
        
        # Display more details in col4
        if col4.button(button_label, key=button_key, ):
            st.session_state['industry'] = industry
            st.session_state['stocks'] = stocks
            st.switch_page("pages/industries_page.py")

    st.write("---")
    # Display the target section on the left sidebar
    st.markdown("### Wanna Go Sustainable?")
    if st.button("Set Target", key="target_section"):
        st.session_state['current_score'] = current_score
        st.session_state['portfolio'] = portfolio
        st.switch_page("pages/target_section.py")


if __name__ == "__main__":
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    if 'username' in st.session_state and st.session_state.username is not None:
        username = st.session_state.get('username')
        current_portfolio = get_portfolio(username)
        if current_portfolio is not None:
            main()
        else:
            st.warning("Your portfolio is empty. Kindly upload external portfolio or make transactions through our app.")
    else:
        st.warning("Please login to get your portfolio insights")


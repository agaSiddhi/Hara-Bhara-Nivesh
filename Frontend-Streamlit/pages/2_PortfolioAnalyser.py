import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import matplotlib.colors as mcolors


def load_excel(file):
    df = pd.read_excel(file)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date')
    return df

# Function to analyze the order history and calculate the portfolio balance over time
def calculate_portfolio_balance(data):
    # Initialize portfolio balance
    portfolio_amount = []
    portfolio_value = []
    current_portfolio = 0
    
    dates = pd.date_range(start=min(data['Date']), end=max(data['Date']))
    tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB','NFLX']
    stocks = {ticker: 0 for ticker in tickers}
    prices = np.random.randint(100, 500, size=(len(dates), len(tickers)))  # Generating random prices -> this is something we ll get from the database

    # Create the DataFrame
    df = pd.DataFrame(prices, index=dates, columns=tickers)
    print(df)

    for index, row in data.iterrows():
        current_value = 0
        if row['Order Type'] == 'Buy':
            current_portfolio += row['Amount'] * row['Price/Quote']
            stocks[row['Ticker']]+=row['Amount']
        elif row['Order Type'] == 'Sell':
            current_portfolio -= row['Amount'] * row['Price/Quote']
            stocks[row['Ticker']]-=row['Amount']
        for ticker, value in stocks.items():
            current_value += value * df.loc[row['Date']][ticker]
        portfolio_amount.append(current_portfolio)
        portfolio_value.append(current_value)

    # Add 'Portfolio Amount' column to DataFrame
    data['Invested Amount'] = portfolio_amount
    data['Portfolio Value'] = portfolio_value 
    return stocks,data

def calculate_portfolio_score(data):
    # Initialize portfolio score
    portfolio_score = []
    current_score = 0
    
    dates = pd.date_range(start=min(data['Date']), end=max(data['Date']))
    tickers = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'FB','NFLX']
    scores = np.random.randint(100, 500, size=(len(dates), len(tickers)))  # Generating random scores -> this is something we ll get from the database

    # Create the DataFrame
    df = pd.DataFrame(scores, index=dates, columns=tickers)

    for index, row in data.iterrows():
        current_value = 0
        if row['Order Type'] == 'Buy':
            current_score += row['Amount'] * df.loc[row['Date']][row['Ticker']]
        elif row['Order Type'] == 'Sell':
            current_score -= row['Amount'] * df.loc[row['Date']][row['Ticker']]
        portfolio_score.append(current_score)


    # Add 'Portfolio Score' column to DataFrame
    data['Score'] = portfolio_score
    return current_score, data    

# Assuming you have a function to map tickers to their categories
def get_category(ticker):
    # Implement your logic here to determine the category for a given ticker
    # This is a placeholder function, you need to replace it with your actual logic
    if ticker in ['AAPL', 'GOOGL', 'MSFT']:
        return 'Equity'
    elif ticker == 'AMZN':
        return 'Hybrid'
    elif ticker == 'FB':
        return 'Debt'
    else :
        return 'Others'
    
# Assuming you have a function to map tickers to their categories
def get_industry(ticker):
    # Implement your logic here to determine the category for a given ticker
    # This is a placeholder function, you need to replace it with your actual logic
    if ticker in ['AAPL', 'GOOGL', 'MSFT']:
        return 'Capital Goods'
    elif ticker == 'GOOG':
        return 'HealthCare'
    elif ticker == 'AMZN':
        return 'Financial'
    elif ticker == 'FB':
        return 'Services'
    else :
        return 'Other'
    
def get_category_percentage(stocks):
    # Calculate the percentage of each category
    total_stocks = sum(stocks.values())
    category_percentage = {'Equity': 0, 'Debt': 0, 'Hybrid': 0, 'Others': 0}
    for ticker, amount in stocks.items():
        category = get_category(ticker)
        category_percentage[category] += amount / total_stocks
    return category_percentage

def get_industry_percentage(stocks):
    total_stocks = sum(stocks.values())
    # Calculate the percentage of each industry
    industry_percentage = {'Capital Goods': 0, 'Financial': 0, 'Services': 0, 'HealthCare': 0, 'Consumer Staples':0, 'Other':0}
    for ticker, amount in stocks.items():
        industry = get_industry(ticker)
        industry_percentage[industry] += amount / total_stocks
    return industry_percentage

@st.cache_data
def save_uploaded_file(uploaded_file):
    return uploaded_file

# Create a Streamlit app
def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    # Page title
        
    st.title('Investment Portfolio Analyzer')
    
    if 'uploaded_file' in st.session_state:
        uploaded_file=st.session_state.get("uploaded_file")
        new_uploaded_file= st.file_uploader('Upload your portfolio here', type=['xlsx'])
        if new_uploaded_file is not None:
            uploaded_file= new_uploaded_file
            st.session_state.uploaded_file = uploaded_file
    else:
        uploaded_file= st.file_uploader('Upload your portfolio here', type=['xlsx'])
     
    
     
    if uploaded_file is not None:
        # Load excel file
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = uploaded_file
        portfolio = load_excel(uploaded_file)
        
        ## ----- Price and Score History

        # Price History
        # print(portfolio)
        stocks, portfolio = calculate_portfolio_balance(portfolio)
        fig1 = px.line(portfolio, x='Date', y=['Invested Amount', 'Portfolio Value'], 
                labels={'Date': 'Date', 'value': 'Amount/Value'}, 
                title='Portfolio Amount and Value Over Time')
        fig1.update_layout(title_x=0.3)
        st.plotly_chart(fig1)

        # Score History
        
        current_score, portfolio = calculate_portfolio_score(portfolio)
        fig2 = px.line(portfolio, x='Date', y=['Score'], 
                labels={'Date': 'Date', 'value': 'Score'}, 
                title='Portfolio Score Over Time')
        fig2.update_layout(title_x=0.4)
        st.plotly_chart(fig2)
        
        ## ----- Distribution of Stock Categories
        # print("Stocks",stocks)
        category_percentage=get_category_percentage(stocks)

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
            # print(button_key)

            # Display more details in col4
            if col4.button(button_label, key=button_key ):
                st.session_state['category'] = category
                st.session_state['stocks'] = stocks
                st.switch_page("pages/categories_page.py") 


        ## ----- Distribution of Stock Industries
                
        industry_percentage=get_industry_percentage(stocks)

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
            st.switch_page("pages/target_section.py")

    # portfolio = pd.read_excel('/Users/ojaswichopra/Downloads/MOCK.xlsx')

if __name__ == "__main__":
    main()

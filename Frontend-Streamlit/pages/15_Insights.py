import streamlit as st
import plotly.express as px
import pandas as pd
from backend.configuration import initialize_system


user_service = initialize_system()[1]


def load_data():
    return user_service.get_user_data_frame_for_insights()

def plot_continent_country_distribution(data):
    # Group users by continent and country
    grouped_data = data.groupby(['continent', 'country']).size().reset_index(name='count')

    # Create a pivot table for easier plotting
    pivot_data = grouped_data.pivot(index='continent', columns='country', values='count').fillna(0)
    
    # Create a heatmap
    fig = px.imshow(pivot_data, labels=dict(color="Number of Users"), title='Continent and Country Distribution of Users')

    st.plotly_chart(fig)

def plot_gender_distribution(data):
    # Group users by gender
    
    gender_counts = data['gender'].value_counts()

    # Create a pie chart for gender distribution
    fig = px.pie(names=gender_counts.index, values=gender_counts.values, title='Gender Distribution of Users', color_discrete_sequence=['lightgreen','lightblue','lightcoral'])

    st.plotly_chart(fig)





def plot_asset_distribution(data):
    # Group users by asset type
    asset_counts = data['asset_type'].value_counts()

    # Create a bar chart for asset distribution
    fig = px.bar(x=asset_counts.values, y=asset_counts.index, orientation='h', title='Asset Type Distribution of Users', labels={'x': 'Number of Users', 'y': 'Asset Type'},color_discrete_sequence=['lightcoral'])

    st.plotly_chart(fig)



def load_transaction_data():
    return pd.read_csv('transaction_data.csv')


def plot_time_distribution():
    # Convert 'date' column to datetime
    time_distribution_data = user_service.get_time_frequency_of_user()

    # Create a line plot for time distribution of investments
    fig = px.histogram(time_distribution_data, x='date',y='num_transactions', nbins=20, title='Time Distribution of User Investments')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Number of Transactions')

    st.plotly_chart(fig)



def plot_average_amount_invested():
    # Convert 'date' column to datetime
    data= user_service.get_date_amount_for_avg_insights()

    # Calculate the total amount invested per day
    daily_total = data.groupby(data['date'].dt.date)['amount'].sum().cumsum()

    # Calculate the number of investments per day
    daily_count = data.groupby(data['date'].dt.date)['amount'].count().cumsum()

    # Calculate the average amount invested per day
    daily_average = daily_total / daily_count

    # Create a line plot for average amount invested over time
    fig = px.line(x=daily_average.index, y=daily_average.values, title='Average Amount Invested Over Time')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Average Amount Invested')

    st.plotly_chart(fig)




def plot_monthly_invested_amount(data):
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # Extract month and year from the date and convert to string
    data['month_year'] = data['date'].dt.to_period('M').astype(str)

    # Group data by month and sum the invested amounts
    monthly_invested_amount = data.groupby('month_year')['amount'].sum().reset_index()

    # Create an area chart for month-wise invested amount
    fig = px.area(monthly_invested_amount, x='month_year', y='amount', title='Month-wise Invested Amount',color_discrete_sequence=['lightgreen'])
    fig.update_xaxes(title='Month')
    fig.update_yaxes(title='Total Invested Amount')

    st.plotly_chart(fig)



def main():
    user_data = load_data()
    user_data_investment=unique_df = user_data.drop_duplicates(subset=['age', 'username', 'investment_type'])

    # Display the data
    st.write("### Age and Investment Distribution of Users")

    # Plot the age distribution and investment type distribution using Plotly
    fig = px.histogram(user_data_investment, x='age', color='investment_type', title='Age and Investment Distribution of Users', labels={'age_group': 'Age Group', 'investment_type': 'Investment Type', 'count': 'Number of Users'})
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)
    
    # Display the continent and country distribution
    st.write("### Continent and Country Distribution of Users")
    user_data_continent_country= user_data.drop_duplicates(subset=['continent', 'username', 'country'])
    plot_continent_country_distribution(user_data_continent_country)

    # Display the gender distribution
    st.write("### Gender Distribution of Users")

    user_data_gender= user_data.drop_duplicates(subset=['gender', 'username'])
    plot_gender_distribution(user_data_gender)

        
    # Display the asset type distribution
    st.write("### Asset Type Distribution of Users")
    user_data_asset=unique_df = user_data.drop_duplicates(subset=['age', 'username', 'asset_type'])
    plot_asset_distribution(user_data_asset)
    
    transaction_data = load_transaction_data()

    # Display the time distribution of investments
    st.write("### Time Distribution of User Investments")
    plot_time_distribution()
    
    # Display the average amount invested over time
    st.write("### Average Amount Invested Over Time")
    plot_average_amount_invested()

    # Display the month-wise invested amount
    st.write("### Month-wise Invested Amount")
    plot_monthly_invested_amount(transaction_data)
    
    
if __name__ == "__main__":
    main()
    # back to home
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
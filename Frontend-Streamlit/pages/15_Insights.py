import streamlit as st
import plotly.express as px
import pandas as pd

def load_data():
    return pd.read_csv('user_data.csv')

user_data = load_data()

# Display the data
st.write("### Age and Investment Distribution of Users")
# st.write(user_data)

# Plot the age distribution and investment type distribution using Plotly
fig = px.histogram(user_data, x='age', color='investment_type', title='Age and Investment Distribution of Users', labels={'age': 'Age', 'investment_type': 'Investment Type', 'count': 'Number of Users'})
fig.update_layout(barmode='group')
st.plotly_chart(fig)



def plot_continent_country_distribution(data):
    # Group users by continent and country
    grouped_data = data.groupby(['continent', 'country']).size().reset_index(name='count')

    # Create a pivot table for easier plotting
    pivot_data = grouped_data.pivot(index='continent', columns='country', values='count').fillna(0)
    
    # Create a heatmap
    fig = px.imshow(pivot_data, labels=dict(color="Number of Users"), title='Continent and Country Distribution of Users')

    st.plotly_chart(fig)


# Display the continent and country distribution
st.write("### Continent and Country Distribution of Users")
plot_continent_country_distribution(user_data)




def plot_gender_distribution(data):
    # Group users by gender
    gender_counts = data['gender'].value_counts()

    # Create a pie chart for gender distribution
    fig = px.pie(names=gender_counts.index, values=gender_counts.values, title='Gender Distribution of Users', color_discrete_sequence=['lightgreen','lightblue'])

    st.plotly_chart(fig)


# Display the gender distribution
st.write("### Gender Distribution of Users")
plot_gender_distribution(user_data)




def plot_asset_distribution(data):
    # Group users by asset type
    asset_counts = data['asset_type'].value_counts()

    # Create a bar chart for asset distribution
    fig = px.bar(x=asset_counts.values, y=asset_counts.index, orientation='h', title='Asset Type Distribution of Users', labels={'x': 'Number of Users', 'y': 'Asset Type'},color_discrete_sequence=['lightcoral'])

    st.plotly_chart(fig)


# Display the asset type distribution
st.write("### Asset Type Distribution of Users")
plot_asset_distribution(user_data)

def load_transaction_data():
    return pd.read_csv('transaction_data.csv')


def plot_time_distribution(data):
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # Create a line plot for time distribution of investments
    fig = px.histogram(data, x='date', nbins=20, title='Time Distribution of User Investments')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Number of Transactions')

    st.plotly_chart(fig)

transaction_data = load_transaction_data()

# Display the time distribution of investments
st.write("### Time Distribution of User Investments")
plot_time_distribution(transaction_data)

def plot_average_amount_invested(data):
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

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


# Display the average amount invested over time
st.write("### Average Amount Invested Over Time")
plot_average_amount_invested(transaction_data)


def plot_monthly_invested_amount(data):
    # Convert 'date' column to datetime
    data['date'] = pd.to_datetime(data['date'])

    # Extract month and year from the date and convert to string
    data['month_year'] = data['date'].dt.to_period('M').astype(str)

    # Group data by month and sum the invested amounts
    monthly_invested_amount = data.groupby('month_year')['amount'].sum().reset_index()

    # Create a line plot for month-wise invested amount
    fig = px.line(monthly_invested_amount, x='month_year', y='amount', title='Month-wise Invested Amount')
    fig.update_xaxes(title='Month')
    fig.update_yaxes(title='Total Invested Amount')

    st.plotly_chart(fig)


# Display the month-wise invested amount
st.write("### Month-wise Invested Amount")
plot_monthly_invested_amount(transaction_data)










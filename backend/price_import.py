import yfinance as yf
import pandas as pd
from datetime import datetime as dt
import csv
import mysql.connector
from datetime import datetime as dt
import numpy as np

def insert_db(file):
    # Establish database connection
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Baba@7849",
        database="Securities"
    )
    cursor = db_connection.cursor()

    # Open and read the CSV file
    with open(file, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if it exists

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Extract data from the row
            price = row[1]
            updatedAt = row[0]
            companyID = row[2]
            # ... extract other column values as needed

            # Execute INSERT statement
            insert_query = f'''INSERT INTO PriceHistory (price, updatedAt, companyID ) VALUES ({price},"{updatedAt}","{companyID}")'''
            cursor.execute(insert_query)

    # Commit changes and close the cursor and connection
    db_connection.commit()
    cursor.close()
    db_connection.close()
# Define a dictionary mapping ticker symbols to company names
company_names = {
    'CAAMX.SA': 'China Asset Management Co.',
    'CSMF.PA': 'AXA S.A.',
    'UBSG.SW': 'UBS Group AG',
    'JEF': 'Jefferies Financial Group Inc.',
    'HNNMY': 'H&M Hennes & Mauritz AB',
    'MSCI': 'MSCI Inc.',
    'KPMGY': 'KPMG',
    'EXK': 'Endeavour Silver Corp.',
    'PM': 'Philip Morris International Inc.',
    'UBP': 'Union Bancaire Privée UBP SA',
    'MET': 'MetLife Inc.',
    'BCS': 'Barclays PLC',
    'AMZN': 'Amazon.com Inc.',
    'IMPACT.CO': 'Impact Coatings AB',
    'BLK': 'BlackRock Inc.',
    'XOM': 'Exxon Mobil Corporation',
    'NOVN.SW': 'Novartis International AG'
}

# Define a list of ticker symbols for the companies you want to get data for
ticker_symbols = list(company_names.keys())

# Define the start and end dates for the data
start_date = '2023-01-01'
end_date = dt.today().strftime('%Y-%m-%d')

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Iterate through each ticker symbol
for symbol in ticker_symbols:
    # Fetch the OHLCV data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Add a 'Symbol' column to identify the company
    data['Symbol'] = symbol
    
    # Add a 'Company Name' column with the real name of the company
    data['Company Name'] = company_names[symbol]
    
    # Append the data to the all_data DataFrame
    all_data = all_data.append(data)

# Save the data to a CSV file
all_data.to_csv('data.csv')

# Print the first few rows of the combined data
print(all_data.head())



insert_db('data_csv')

# Define a list of ticker symbols for the missing companies
missing_ticker_symbols = ['CAAMX.SA', 'CSMF.PA', 'KPMGY', 'UBP', 'IMPACT.CO']

# Define the start and end dates for the data
start_date = '2023-01-01'
end_date = dt.today().strftime('%Y-%m-%d')

# Initialize an empty DataFrame to store all data
all_data_missing = pd.DataFrame()

# Iterate through each missing ticker symbol
for symbol in missing_ticker_symbols:
    # Generate random closing prices for the given dates
    num_days = (dt.strptime(end_date, '%Y-%m-%d') - dt.strptime(start_date, '%Y-%m-%d')).days + 1
    closing_prices = np.random.uniform(190, 200, num_days)  # Random closing prices between 50 and 200
    
    # Create a DataFrame with the generated closing prices
    data = pd.DataFrame({
        'Date': pd.date_range(start=start_date, end=end_date),
        'Close': closing_prices,
        'Symbol': symbol,
        'Company Name': company_names[symbol]
    })
    
    # Append the data to the all_data_missing DataFrame
    all_data_missing = all_data_missing.append(data)

# Save the data to a CSV file
all_data_missing.to_csv('missing_data.csv', index=False)

# Print the first few rows of the combined data
print(all_data_missing.head())

insert_db('missing_data.csv')
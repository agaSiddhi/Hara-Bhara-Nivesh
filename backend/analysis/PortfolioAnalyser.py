from backend.database import return_price_and_date, return_score_and_date
import pandas as pd
import numpy as np


# def calculate_portfolio_balance(data):
#     # Initialize portfolio balance
#     priceDate= return_price_and_date()
#     df = pd.DataFrame(priceDate, columns=['tickers', 'price', 'dates'])
#     df['dates'] = pd.to_datetime(df['dates'])
#     df = df.pivot(index='dates', columns='tickers', values='price')
#     df = df.fillna(0)
    
#     portfolio_amount = []
#     portfolio_value = []
#     current_portfolio = 0
    
#     # dates = pd.date_range(start=min(data['Date']), end=max(data['Date']))
#     tickers = df.columns.to_numpy()
#     stocks = {ticker: 0 for ticker in tickers}
#     # prices = np.random.randint(100, 500, size=(len(dates), len(tickers)))  # Generating random prices -> this is something we ll get from the database

#     # Create the DataFrame
#     # df = pd.DataFrame(prices, index=dates, columns=tickers)

#     for index, row in data.iterrows():
#         current_value = 0
#         if row['Order Type'] == 'Buy':
#             current_portfolio += row['Amount'] * row['Price/Quote']
#             stocks[row['Ticker']]+=row['Amount']
#         elif row['Order Type'] == 'Sell':
#             current_portfolio -= row['Amount'] * row['Price/Quote']
#             stocks[row['Ticker']]-=row['Amount']
#         for ticker, value in stocks.items():
#             current_value += value * df.loc[row['Date']][ticker]
#         portfolio_amount.append(current_portfolio)
#         portfolio_value.append(current_value)

#     # Add 'Portfolio Amount' column to DataFrame
#     data['Invested Amount'] = portfolio_amount
#     data['Portfolio Value'] = portfolio_value 
#     return stocks,data

def calculate_portfolio_score(data):
    # Initialize portfolio score
    portfolio_score = []
    current_score = 0
    
    priceDate= return_score_and_date()
    df = pd.DataFrame(priceDate, columns=['tickers', 'score', 'dates'])
    df['dates'] = pd.to_datetime(df['dates'])
    df = df.pivot(index='dates', columns='tickers', values='score')
    df = df.fillna(0)
    
    for index, row in data.iterrows():
        current_value = 0
        if row['Order Type'] == 'Buy':
            current_score += row['Amount'] * df.loc[row['Date']][row['Ticker']]
        elif row['Order Type'] == 'Sell':
            current_score -= row['Amount'] * df.loc[row['Date']][row['Ticker']]
        portfolio_score.append(current_score)

    data['Score'] = portfolio_score
    return current_score, data 



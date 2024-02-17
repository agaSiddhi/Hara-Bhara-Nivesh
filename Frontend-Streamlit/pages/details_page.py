import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.database import return_companyID_from_company_name,return_company_details_from_companyID, return_industry_description_from_companyID,return_score_history_from_companyID,return_price_history_from_companyID
import datetime

if st.button("Back to Home"):
        st.switch_page("Landing.py")

company_name = st.session_state['company']
company_id = return_companyID_from_company_name(company_name)[0][0]
# print(company_id)
company_details = return_company_details_from_companyID(company_id)[0]
company_description = return_industry_description_from_companyID(company_id)[0][0]
score_history = return_score_history_from_companyID(company_id)
price_history = return_price_history_from_companyID(company_id)
# print("SH",score_history)
# print("PH",price_history)

st.markdown(f"# Details for {company_name}")

col1,col2 = st.columns(2)
with col1:
        st.write("**Last Updated At :**", company_details[3])
        st.write("**Total Assets :**", company_details[4])
        st.write("**Revenue :**", company_details[5])
        st.write("**Employees :**", company_details[6])
        st.write("**Website URL :**", company_details[9])
with col2:
        st.write("**Current Score :**", company_details[7])
        st.write("**Founded Year :**", company_details[2].date())
        st.write("**Company ID :**", company_details[0])
        st.write("**Description :**",company_description)
        st.write("**Rating :**")

# Extracting dates, scores, and prices from the history data
score_dates = [entry[1] for entry in score_history]
scores = [float(entry[0]) for entry in score_history]

price_dates = [entry[1] for entry in price_history]
prices = [float(entry[0]) for entry in price_history]

# Creating DataFrames
score_df = pd.DataFrame({'Date': score_dates, 'Score': scores})
price_df = pd.DataFrame({'Date': price_dates, 'Price': prices})

# Merging DataFrames on date
merged_df = pd.merge(score_df, price_df, on='Date', how='outer')

# Sorting merged DataFrame by date
merged_df.sort_values(by='Date', inplace=True)
# print(merged_df)
merged_df = merged_df.fillna(0)

print(merged_df.columns)

# Plotting
st.line_chart(merged_df, x="Date", y=["Price", "Score"], color=['#FF0000', '#0000FF'])

# Generating random dates
# start_date = datetime(2023, 1, 1)
# end_date = datetime(2023, 12, 31)
# random_dates = [start_date + timedelta(days=np.random.randint((end_date - start_date).days)) for _ in range(20)]
# dates = np.array(random_dates).reshape(-1, 1)

# # Generating random scores and prices
# scores = np.random.randn(20, 1)
# prices = np.random.randn(20, 1)

# # Concatenating arrays horizontally
# data = np.hstack((dates, scores, prices))

# chart_data = pd.DataFrame(data, columns=["Date", "Score", "Price"])
# st.line_chart(
#    chart_data, x="Date", y=["Score", "Price"], color=["#FF0000", "#0000FF"]  # Optional
# )

col1, col2 = st.columns(2)
with col1:
        st.link_button("Latest Articles", "https://streamlit.io/gallery")
with col2:
        if st.button("Go back"):
                st.switch_page("pages/1_Listings.py")


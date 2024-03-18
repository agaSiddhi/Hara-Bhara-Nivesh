import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# from backend.database import return_companyID_from_company_name,return_company_details_from_companyID, return_industry_description_from_companyID,return_score_history_from_companyID,return_price_history_from_companyID
from backend.configuration import initialize_system

def main():
        company_service = initialize_system()[0]
        details = company_service.return_company_name_and_description()

        company_name = st.session_state['company']
        company_id = company_service.return_companyID_from_company_name(company_name)[0][0]
        company_details = company_service.return_company_details_from_companyID(company_id)[0]
        company_description = company_service.return_industry_description_from_companyID(company_id)[0][0]
        score_history = company_service.return_score_history_from_companyID(company_id)
        price_history = company_service.return_price_history_from_companyID(company_id)


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


        col1, col2 = st.columns(2)
        with col1:
                st.link_button("Latest Articles", "https://streamlit.io/gallery")
                if st.button("Go back"):
                        st.switch_page("pages/1_Listings.py")

        with col2:
                if st.button("Buy"):
                        st.switch_page("pages/buy_stocks.py")


if __name__ == "__main__":
    main()


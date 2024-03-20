import streamlit as st
import pandas as pd
from backend.configuration import initialize_system
import plotly.graph_objects as go

def main():
        company_service = initialize_system()[0]

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

        # Extracting dates, scores, and prices from the history data
        score_dates = [entry[1] for entry in score_history]
        scores = [float(entry[0]) for entry in score_history]

        price_dates = [entry[1] for entry in price_history]
        prices = [float(entry[0]) for entry in price_history]
        
        # Creating DataFrames
        score_df = pd.DataFrame({'Date': score_dates, 'Score': scores})
        score_df = company_service.carry_over(score_df,'Score')
        price_df = pd.DataFrame({'Date': price_dates, 'Price': prices})
        price_df = company_service.carry_over(price_df,'Price')
        # Merging DataFrames on date
        merged_df = pd.merge(score_df, price_df, on='Date', how='outer')

        # Sorting merged DataFrame by date
        merged_df.sort_values(by='Date', inplace=True)

        merged_df = merged_df.fillna(0)
        
        # Create a Plotly figure
        fig = go.Figure()
        
        # Add traces for each set of data with different y-axes
        fig.add_trace(go.Scatter(x=merged_df['Date'], y=merged_df['Price'], name='Price', yaxis='y1'))
        fig.add_trace(go.Scatter(x=merged_df['Date'], y=merged_df['Score'], name='Score', yaxis='y2'))

        # Update layout to show two y-axes
        fig.update_layout(
            yaxis=dict(title='Price', side='left', showgrid=False),
            yaxis2=dict(title='Score', side='right', overlaying='y', showgrid=False)
        )
        
        # Apply custom CSS styling to change the color of y2 tick labels
        fig.update_layout(
            template='plotly',
            yaxis2_color='red'
        )
        
        # Plotting
        st.plotly_chart(fig)


        col1, col2 = st.columns(2)
        with col1:
                if st.button("Go back"):
                        st.switch_page("pages/1_Listings.py")

        with col2:
                if st.button("Buy"):
                        st.switch_page("pages/buy_stocks.py")


if __name__ == "__main__":
    
    main()


import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

if st.button("Back to Home"):
        st.switch_page("Landing.py")

company = st.session_state['company']

st.markdown(f"# Details for {company['Name']}")

col1,col2 = st.columns(2)
with col1:
        st.write("**Last Updated At :**", company["updatedAt"])
        st.write("**Total Assets :**", company["totalAssests"])
        st.write("**Revenue :**", company["revenue"])
        st.write("**Employees :**", company["employees"])
        st.write("**Website URL :**", company["websiteURL"])
with col2:
        st.write("**Current Score :**", company["currentScore"])
        st.write("**Founded Year :**", company["foundedYear"])
        st.write("**Company ID :**", company["companyID"])
        st.write("**Description :**", company["description"])
        st.write("**Rating :**", company["rating"])


# Generating random dates
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
random_dates = [start_date + timedelta(days=np.random.randint((end_date - start_date).days)) for _ in range(20)]
dates = np.array(random_dates).reshape(-1, 1)

# Generating random scores and prices
scores = np.random.randn(20, 1)
prices = np.random.randn(20, 1)

# Concatenating arrays horizontally
data = np.hstack((dates, scores, prices))

chart_data = pd.DataFrame(data, columns=["Date", "Score", "Price"])
st.line_chart(
   chart_data, x="Date", y=["Score", "Price"], color=["#FF0000", "#0000FF"]  # Optional
)

col1, col2 = st.columns(2)
with col1:
        st.link_button("Latest Articles", "https://streamlit.io/gallery")
with col2:
        if st.button("Go back"):
                st.switch_page("pages/1_Listings.py")


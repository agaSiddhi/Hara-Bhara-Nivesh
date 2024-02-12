import json
import streamlit as st
from backend.database import read_company_data
# Define a list of companies
companies = json.loads(read_company_data())


# Create a Streamlit app
def main():
    # Page title
    st.title("Top Sustainable Companies")

    # Search bar
    search_term = st.text_input("",placeholder= "Enter Company Name")
    search_button = st.button("Search")

    # Filter companies based on search term
    filtered_companies = [company for company in companies if search_term.lower() in company["Name"].lower()]

    # Display filtered companies
    for company in filtered_companies:
        st.subheader(f"{company['Rank']}. {company['Name']}")
        col1, col2 = st.columns([3,1])
        col1.write(company["Description"])
        col2.write(get_stars_html(company["Rating"]))

# Function to generate HTML code for star rating
def get_stars_html(rating):
    stars_html = ""
    for i in range(5):
        if i < rating:
            stars_html += ":star:"
    return stars_html

if __name__ == "__main__":
    main()

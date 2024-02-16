import json
import streamlit as st
from backend.database import read_company_data
# from pages.details_page import show_details_page

# Define a list of companies
companies = json.loads(read_company_data())

# Create a Streamlit app
def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    # Page title
    st.title("Top Sustainable Companies")

    # Search bar
    search_term = st.text_input("", placeholder="Enter Company Name")
    search_button = st.button("Search")

    # Filter companies based on search term
    filtered_companies = [company for company in companies if search_term.lower() in company["Name"].lower()]

    # Display filtered companies
    for company in filtered_companies:
        company_name = f"{company['companyID']}. {company['Name']}"
        st.subheader(company_name)
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(company["description"])
        col2.write(get_stars_html(company["rating"]))
        
        # Add detail button to view company details
        button_label = "Details"
        button_key = f"{button_label}_{company_name}"
        if col3.button(button_label, key=button_key):
            st.session_state['company'] = company
            st.switch_page("pages/details_page.py")
                # show_details_page(company)  # Pass the 'company' details as an argument

# Function to generate HTML code for star rating
def get_stars_html(rating):
    stars_html = ""
    for i in range(5):
        if i < rating:
            stars_html += ":star:"
    return stars_html

if __name__ == "__main__":
    main()

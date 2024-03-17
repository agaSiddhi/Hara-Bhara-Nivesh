import streamlit as st

# Define a list of companies
from backend.configuration import initialize_system
company_service = initialize_system()
details = company_service.return_company_name_and_description()

# Create a Streamlit app
def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")
    # Page title
        
    st.title("Top Sustainable Companies")

    # Search bar
    search_term = st.text_input("", placeholder="Enter Company Name")
    search_button = st.button("Search")

    filtered_companies = [company for company in details.keys() if search_term.lower() in company.lower()]

    # Filter companies based on search term
    for company in filtered_companies:
        company_detail = details[company]
        company_name = f"{company_detail[2]}. {company}"
        st.subheader(company_name)
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(company_detail[1])
        col2.write(company_detail[0])

        # Add detail button to view company details
        button_label = "Details"
        button_key = f"{button_label}_{company_name}"
        if col3.button(button_label, key=button_key):
            st.session_state['company'] = company
            st.switch_page("pages/details_page.py") 


if __name__ == "__main__":
    main()

# Define a list of companies
companies = [
    {"rank": 1, "name": "Company A", "description": "Company A is a leader in sustainable practices...","rating":4},
    {"rank": 2, "name": "Company B", "description": "Company B is committed to reducing its carbon footprint...","rating":3},
    {"rank": 3, "name": "Company C", "description": "Company B is committed to reducing its carbon footprint...","rating":2},
    {"rank": 4, "name": "Company D", "description": "Company B is committed to reducing its carbon footprint...","rating":1},
    {"rank": 5, "name": "Company E", "description": "Company B is committed to reducing its carbon footprint...","rating":1},
    # Add more companies as needed
]

# Create a Streamlit app
def main():
    # Page title
    st.title("Top Sustainable Companies")

    # Search bar
    search_term = st.text_input("",placeholder= "Enter Company Name")
    search_button = st.button("Search")

    # Filter companies based on search term
    filtered_companies = [company for company in companies if search_term.lower() in company["name"].lower()]

    # Display filtered companies
    for company in filtered_companies:
        st.subheader(f"{company['rank']}. {company['name']}")
        col1, col2 = st.columns([3,1])
        col1.write(company["description"])
        col2.write(get_stars_html(company["rating"]))

# Function to generate HTML code for star rating
def get_stars_html(rating):
    stars_html = ""
    for i in range(5):
        if i < rating:
            stars_html += ":star:"
    return stars_html

if __name__ == "__main__":
    main()

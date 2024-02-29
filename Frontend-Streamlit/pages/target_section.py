import streamlit as st
import random

# Generate a dictionary with keys A to Z and random scores between 100 and 200
scores_dict = {chr(65 + i): random.randint(100, 200) for i in range(26)}
# Create a dictionary with categories as keys and top industries as values
# Sample data for the DataFrame
data2 = {
    'Capital Goods': ['A','B'],
    'HealthCare':['D','E'],
    'Financial':['G','H'],
    'Services':['J','K'],
    'Other':['C','F'],
    'Consumer Staples': ['I','L']
}

# Create a dictionary with categories as keys and top industries as values
# Sample data for the DataFrame
data1 = {
    'Equity': ['A','B','C'],
    'Debt':['D','E','F'],
    'Hybrid':['G','H','I'],
    'Others':['J','K','L'],
}

def filter_companies(selected_categories, selected_sectors):
    filtered_companies = {}
    for category in selected_categories:
        if category in data1:
            for company in data1[category]:
                if company not in filtered_companies:
                    filtered_companies[company] = {'score': scores_dict[company], 'category': category, 'sector': None}
    
    for sector in selected_sectors:
        if sector in data2:
            for company in data2[sector]:
                if company not in filtered_companies:
                    # filtered_companies[company] = {'score': scores_dict[company], 'category': None, 'sector': sector}
                    continue
                else:
                    # If the company is already in the dictionary (from data1), update its sector
                    filtered_companies[company]['sector'] = sector

    
    filtered_companies = {company: details for company, details in filtered_companies.items() if details['sector'] is not None}
    # Sort the dictionary in descending order based on scores
    filtered_companies = dict(sorted(filtered_companies.items(), key=lambda x: x[1]['score'], reverse=True))
    return filtered_companies

# Function to get user input for fund categories
def get_fund_categories():
    st.write("Which category fund(s) would you like to invest in?")
    selected_categories = []
    categories = ['Equity', 'Debt', 'Hybrid', 'Others']
    for category in categories:
        if st.checkbox(category):
            selected_categories.append(category)
    return selected_categories

# Function to get user input for interested sectors
def get_interested_sectors():
    st.write("Which sector fund(s) would you like to invest in?")
    selected_sectors = []
    sectors = ['Capital Goods', 'HealthCare', 'Financial', 'Services', 'Consumer Staples', 'Other']
    for sector in sectors:
        if st.checkbox(sector):
            selected_sectors.append(sector)
    return selected_sectors

def main():
    if st.button("Back to Home"):
        st.switch_page("Landing.py")

    # Page title
    st.title('Set Your Target!')    
    current_stocks = st.session_state['stocks']
    current_score = st.session_state['current_score']
    # Main function for the target section
    target_score = st.number_input("Enter your score target:")
    if current_score < target_score:
        placeholder = st.empty()
        suggestions_button = None
        with placeholder.container():
            selected_categories = get_fund_categories()
            selected_sectors = get_interested_sectors()
            if selected_categories and selected_sectors:
                suggestions_button = st.button("Get Suggestions")
            st.write("---")

        if suggestions_button:
            placeholder.empty()
            filtered_companies = filter_companies(selected_categories,selected_sectors)
            for company, details in filtered_companies.items():
                col1,col2 = st.columns([3,1])
                col1.markdown(f"#### {company}")
                col1.write(f"{details['category']} ● {details['sector']}")
                col2.markdown(f"##### Average score: {details['score']}")
                st.write("---")

    else:
        st.write("Hurray!! You meet your sustainability Targets")
        st.write("---")
        
    
    if st.button("Go back"):
        st.switch_page("pages/2_PortfolioAnalyser.py")

if __name__ == "__main__":
    main()
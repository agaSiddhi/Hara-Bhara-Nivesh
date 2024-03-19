import streamlit as st
from backend.configuration import initialize_system
        

def main():
    company_service = initialize_system()[0]
    user_service= initialize_system()[1]
    company_id = company_service.return_companyID_from_company_name(company_name)[0][0]

    st.subheader(f"Buy: {company_name}")
    st.write(f"Price per stock: ${user_service.get_current_price_for_ticker(company_id)}")
    quantity = st.number_input("Enter quantity to buy:", min_value=10, max_value=1000, step=1)

    # Button to buy stocks
    if st.button("Buy"):
        user_service.buy_stock(username, quantity, company_id)

if __name__ == "__main__":
    col1,col2 = st.columns(2)
    if 'username' in st.session_state and st.session_state.username is not None:
        username = st.session_state.get('username')
        company_name = st.session_state.get('company')
        main()
        if col2.button("Go Back"):
            st.switch_page("pages/details_page.py")
    else:
        st.warning("Login to buy stocks")
        # back to home
    
    if col1.button("Back to Home"):
        st.switch_page("Landing.py")
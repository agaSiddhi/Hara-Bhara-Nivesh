import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space

page_title = "Hara Bhara Nivesh"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"


def main():

    st.set_page_config(initial_sidebar_state="collapsed",page_title=page_title, page_icon=page_icon, layout=layout)

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # Settings

    # --- NAVIGATION MENU ---
    selected = option_menu(
        menu_title=None,
        options=["Investor", "Company","Insights"],
        icons=["people-fill", "building-fill","bar-chart-fill"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )

    # Investor Tab
    if selected=="Investor":

        # Header Section
        st.markdown("<h1 style='text-align: center; color: #FF4B4B'>Welcome to Hara Bhara Nivesh</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Invest in a better future!</h3>", unsafe_allow_html=True)
        
        # Sample image URLs
        image_url = '/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/assets/landing.jpg'
        
        # Display image
        st.image(image_url, caption=None, use_column_width=True)

        st.markdown("---")


        col1, col2, col3, col4 = st.columns([1.8,2,1.2,0.8])  

        with col1:
            if st.button("Companies List"):
                st.switch_page("pages/1_Listings.py")

        with col2:
            if st.button("Portfolio Analyser"):
                st.switch_page("pages/2_PortfolioAnalyser.py")

        if 'username' in st.session_state and st.session_state.username is not None:
            username = st.session_state.get('username')
            authenticator = st.session_state.get('authenticator')
            with col3:
                if st.button("My Account"):
                    st.switch_page("pages/8_UserAccount.py")
            with col4:
                authenticator.logout('Logout', 'main', key='unique_key')     
        else:            
            with col3:
                if st.button("Login"):
                    st.switch_page("pages/5_Login.py")
            with col4:
                if st.button("Signup"):
                    st.switch_page("pages/6_Signup.py")

        
        add_vertical_space(2)
        # Introduction to Sustainable Investing
        st.header("What is Sustainable Investing?")
        st.write("""
        Sustainable investing, also known as socially responsible investing (SRI) 
        or ethical investing, aims to generate long-term positive impact alongside 
        financial returns. It considers environmental, social, and governance (ESG) 
        criteria to make investment decisions.
        """)
        st.markdown("---")

        add_vertical_space(2)
        # Featured Investments
        st.header("Featured Investments")
        st.write("Explore some of our top sustainable investment options:")
        # Add images of featured investments
        images = [
            '/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/assets/apple.jpeg',
            '/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/assets/tesla.jpeg',
            '/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/assets/gs.webp',
            '/Users/ojaswichopra/Downloads/DESIS/project/DesisSG-2/assets/nike.jpeg'
        ]
        col1, col2, col3, col4 = st.columns(4)
        col1.image(images[0],caption=None)
        col2.image(images[1],caption=None)
        col3.image(images[2],caption=None )
        col4.image(images[3],caption=None )
        st.markdown("---")

        add_vertical_space(2)
        # How It Works
        st.header("How It Works")
        st.write("""
        1. **Sign up for an account.**
        2. **Browse through our curated list of sustainable investment options.**
        3. **Choose investments that align with your values and financial goals.**
        4. **Invest responsibly and track your portfolio's performance.**
        """)
        st.markdown("---")

        add_vertical_space(2)
        # Testimonials
        st.header("Testimonials")
        # Add some testimonials from satisfied users or partners
        st.markdown("---")

        add_vertical_space(2)
        # Footer
        st.write("Contact us: contact@sustainableinvestments.com")

        # CSS styling
        st.markdown(
            """
            <style>
            body {
                background-color: #f5f5f5;
                color: #333333;
                font-family: Arial, sans-serif;
            }
            .stButton>button {
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border-radius: 8px;
                cursor: pointer;
                transition-duration: 0.4s;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        
    if selected == 'Company':
        if st.button("Carbon Credit Marketplace"):
            st.switch_page("pages/3_CarbonCredit.py")

        if st.button("Auction"):
            st.switch_page("pages/4_AuctionPage.py")

        

      

if __name__ == "__main__":
    main()


import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space

title = "Hara Bhara Nivesh"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

selection = None

landing_images = ['../assets/landing_investor.svg','../assets/landing_company.svg']

page_title=["What is Sustainable Investing?","Introduction to Carbon Credit Marketplace"]

st.session_state.role=None

# sidebar page links
def authenticated_menu_user():
    st.sidebar.empty()
    st.sidebar.page_link("pages/1_Listings.py", label="Companies List")
    st.sidebar.page_link("pages/2_PortfolioAnalyser.py", label="Portfolio Analyser")
    if 'username' in st.session_state and st.session_state.username is not None:
        authenticator = st.session_state.get('authenticator')
        st.sidebar.page_link("pages/8_UserAccount.py", label="My Account")
        st.sidebar.page_link("pages/12_SellStocks.py", label="Sell Shares")
        st.sidebar.page_link("pages/13_UploadPortfolio.py", label="Upload External Portfolio")
        st.sidebar.page_link("pages/14_TargetSection.py", label="Set Target")
        with st.sidebar:
            authenticator.logout('Logout', 'main', key='unique_key')     
    else:
        st.sidebar.page_link("pages/5_LoginUser.py", label="Login")
        st.sidebar.page_link("pages/6_SignupUser.py", label="Signup")        
        
# sidebar page links
def authenticated_menu_company():
    st.sidebar.empty()
    st.sidebar.page_link("pages/3_CarbonCredit.py", label="List your Credits")
    st.sidebar.page_link("pages/4_AuctionPage.py", label="Credits Auction")
    if 'username' in st.session_state and st.session_state.username is not None:
        authenticator = st.session_state.get('authenticator')
        st.sidebar.page_link("pages/11_CompanyAccount.py", label="My Account")
        with st.sidebar:
            authenticator.logout('Logout', 'main', key='unique_key')     
    else:
        st.sidebar.page_link("pages/9_LoginCompany.py", label="Login")
        st.sidebar.page_link("pages/10_SignupCompany.py", label="Signup")     


content = ["""
    Sustainable investing, also known as socially responsible investing (SRI) 
    or ethical investing, aims to generate long-term positive impact alongside 
    financial returns. It considers environmental, social, and governance (ESG) 
    criteria to make investment decisions.
    ""","""
        Welcome to the Carbon Credit Marketplace, where sustainability meets finance! 
        Our platform offers a convenient solution for buying and selling carbon credits, 
        enabling businesses to take tangible steps towards environmental responsibility. 
        Whether you're a company striving to reduce your carbon footprint or an investor 
        looking to support sustainability initiatives, our marketplace provides a 
        transparent and efficient platform for trading carbon credits.
        """]

process = ["""
        1. **Sign up for an account.**
        2. **Browse through our curated list of sustainable investment options.**
        3. **Choose investments that align with your values and financial goals.**
        4. **Invest responsibly and track your portfolio's performance.**
        ""","""
        1. **Sign up for an account:** Create your account on our platform to get started.
        2. **Browse carbon credit listings:** Explore our curated list of carbon credit listings.
        3. **Choose your carbon credits:** Select carbon credits that align with your sustainability goals.
        4. **Complete your transactions:** Buy or sell carbon credits seamlessly through our platform.
        """]

def main():

    st.set_page_config(page_title=title, page_icon=page_icon, layout=layout)

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
        styles={    
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#ffffff"},
        "nav-link-selected": {"background-color": "#2B8C0C"},
        }   
    )

    if selected=="Investor":
        authenticated_menu_user()
        selection=0
    
    if selected == 'Company':
        authenticated_menu_company()
        selection=1
        
    if selected == 'Insights':
        selection=2
        
    # Header Section
    st.markdown("<h1 style='text-align: center; color: #2B8C0C'>Welcome to Hara Bhara Nivesh</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Invest in a better future!</h3>", unsafe_allow_html=True)
    
    # Sample image URLs
    image_url = landing_images[selection]
    
    # Display image
    st.image(image_url, caption=None, use_column_width=True)

    st.markdown("---")
                         
    add_vertical_space(2)
        
    # Introduction 
    st.header(page_title[selection])
    st.write(content[selection])
    st.markdown("---")

    add_vertical_space(2)
    
    # Featured Investments
    st.header("Featured Investments")
    st.write("Explore some of our top sustainable investment options:")
    # Add images of featured investments
    images = [
        '../assets/apple.jpeg',
        '../assets/tesla.jpeg',
        '../assets/gs.webp',
        '../assets/nike.jpeg'
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
    st.write(process[selection])
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


if __name__ == "__main__":
    main()


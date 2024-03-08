import streamlit as st
page_title = "Hara Bhara Nivesh"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

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


st.title("Landing Page")
if st.button("Companies List"):
    st.switch_page("pages/1_Listings.py")

if st.button("Portfolio Analyser"):
    st.switch_page("pages/2_PortfolioAnalyser.py")

if st.button("Carbon Credit Marketplace"):
    st.switch_page("pages/3_CarbonCredit.py")

if st.button("Auction"):
    st.switch_page("pages/4_AuctionPage.py")

if st.button("Login"):
    st.switch_page("pages/5_Login.py")

if st.button("Signup"):
    st.switch_page("pages/6_Signup.py")
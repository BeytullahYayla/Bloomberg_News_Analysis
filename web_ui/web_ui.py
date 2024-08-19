import streamlit as st
from pages import *
import time

# Set up navigation
pg = st.navigation([
    st.Page(news_page, title="News", icon="🔥"),
    st.Page(analyzes_page, title="Visual Graphics", icon="📈"),
])

# Run the selected page
pg.run()

# Implement auto-refresh
# Refresh every 5 minutes
st.markdown("""
    <meta http-equiv="refresh" content="300">
    """, unsafe_allow_html=True)
import streamlit as st
from utils import *
from constants import *

def news_page():
    # Get data
    data = fetch_data(REQUEST_URL)
    st.markdown(
        "<h1 style='text-align:center;'>Bloomberg Economy News</h1>", 
        unsafe_allow_html=True)
    
    # Display total record count
    total_records = len(data)
    
    
    if data != []:
        # Prepare data for visualization purposes
        df = prepare_data(data)
        
        # Visualize table
        create_table(df)
        
        st.markdown(
        f"""
        <div style='text-align: center; 
                    background-color: #f0f2f6; 
                    padding: 10px; 
                    border-radius: 5px; 
                    border-left: 5px solid #2196f3;'>
            <strong>Total Records in Database: {total_records}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )
    else:
        st.warning("There is no data in database!")

        
    
def analyzes_page():
    st.markdown(
        "<h1 style='text-align: center;'>Sentiment Distribution of News</h1>",
        unsafe_allow_html=True)
    data = fetch_data(REQUEST_URL)
    if data!=[]:
        
        st.markdown(
        "<h2 style='text-align: center'>Pie Chart</h2>",
        unsafe_allow_html=True)
        create_pie_chart(data)
        st.markdown(
        "<h2 style='text-align: center'>Bar Plot</h2>",
        unsafe_allow_html=True
    
)
        create_bar_plot(data)
        
    else:
        st.warning("There is no data in database!")

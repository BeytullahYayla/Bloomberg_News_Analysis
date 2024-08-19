import streamlit as st
from utils import *
from constants import *

def news_page():
    """
    Displays the Bloomberg Economy News page in the Streamlit app.

    This function retrieves news data from the specified API endpoint and displays it
    in a table format. It also shows the total number of records fetched from the
    database. If no data is available, a warning message is displayed.

    The page includes the following features:
    - A centered title at the top of the page.
    - Visualization of the fetched news data in a table.
    - A centered information box showing the total number of records in the database.
    - A warning message if no data is available.

    Note:
        The function relies on external utility functions such as `fetch_data`,
        `prepare_data`, and `create_table`, which are assumed to be defined elsewhere
        in the codebase.

    Args:
        None

    Returns:
        None
    """
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
    """
    Displays the Sentiment Distribution Analysis page in the Streamlit app.

    This function retrieves news data from the specified API endpoint and performs sentiment
    analysis on the gathered news. It visualizes the sentiment distribution through pie and
    bar charts. If no data is available, a warning message is displayed.

    The page includes the following features:
    - A centered title at the top of the page.
    - An introductory explanation of the benefits of sentiment analysis on news.
    - Visualization of sentiment distribution using a pie chart.
    - Visualization of sentiment distribution using a bar plot.
    - A warning message if no data is available.

    Note:
        The function relies on external utility functions such as `fetch_data`,
        `create_pie_chart`, and `create_bar_plot`, which are assumed to be defined
        elsewhere in the codebase.

    Args:
        None

    Returns:
        None
    """
    st.markdown(
        "<h1 style='text-align: center;'>Sentiment Distribution of News</h1>",
        unsafe_allow_html=True)
    st.write("We can do sentiment analysis to gathered news. Doing sentiment analysis on news may provide some insights for us. Classifying news as negative, positive, or neutral can be very useful for understanding general trends, public sentiment, and market conditions.")
    
    data = fetch_data(REQUEST_URL)
    if data != []:
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
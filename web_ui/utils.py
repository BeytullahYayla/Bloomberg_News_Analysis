import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px

def fetch_data(url: str):
    """
    Fetches data from the specified API endpoint.

    This function sends a GET request to the given URL and returns the JSON response
    as a Python dictionary.

    Args:
        url (str): The URL of the API endpoint from which to fetch data.

    Returns:
        dict: The JSON response from the API, converted to a Python dictionary.
    """
    response = requests.get(url)
    response_json = response.json()
    return response_json


def create_table(df: pd.DataFrame):
    """
    Displays a paginated table in Streamlit.

    This function takes a DataFrame and displays it in a paginated table format
    within the Streamlit app. Users can navigate through the table pages using
    a number input widget.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be displayed.

    Returns:
        None
    """
    # Pagination settings
    items_per_page = 5
    total_items = len(df)
    total_pages = total_items // items_per_page + (total_items % items_per_page > 0)

    # Page number input
    page_number = st.number_input('Page number', min_value=1, max_value=total_pages, step=1)

    # Calculate indices for the DataFrame
    start_idx = (page_number - 1) * items_per_page
    end_idx = start_idx + items_per_page

    if total_items != 0:
        # Show only sliced data
        st.table(df.iloc[start_idx:end_idx])
    else:
        st.write("There is no data in database!")
def prepare_data(data):
    """
    Prepares the data for visualization by converting it into a DataFrame and
    formatting it.

    This function converts the input data into a pandas DataFrame, selects specific
    columns, renames them, and returns the processed DataFrame.

    Args:
        data (list): A list of dictionaries containing the raw data to be prepared.

    Returns:
        pd.DataFrame: The processed DataFrame with selected and renamed columns.
    """
    # Convert data into DataFrame
    df = pd.DataFrame(data)
    
    # Drop "id" column and select necessary columns
    columns = ["title", "sentiment", "publish_date", "description"]
    df = df[columns]
    
    # Change column names
    df.columns = ["Title", "Sentiment", "Date", "Description"]
    return df


def create_pie_chart(data):
    """
    Creates and displays a pie chart of sentiment distribution in Streamlit.

    This function extracts sentiment data from the input, counts the occurrences
    of each sentiment, and displays a pie chart representing the distribution
    of sentiments (Positive, Negative, Neutral) in the dataset.

    Args:
        data (list): A list of dictionaries containing news data with sentiments.

    Returns:
        None
    """
    # Write an explanation
    st.write("The pie chart represents the distribution of sentiments across a set of news articles. The sentiments are categorized into three groups: Neutral, Negative, and Positive. The chart provides a visual breakdown of the proportion of each sentiment within the dataset.")
    
    # Extract sentiments
    sentiments = [item['sentiment'] for item in data]

    # Count occurrences of each sentiment
    sentiment_counts = Counter(sentiments)

    # Prepare data for the pie chart
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())

    # Create pie chart using Plotly
    fig = px.pie(values=values, names=labels)

    # Display the pie chart in Streamlit
    st.plotly_chart(fig)

def create_bar_plot(data):
    """
    Creates and displays a bar plot of sentiment distribution in Streamlit.

    This function extracts sentiment data from the input, counts the occurrences
    of each sentiment, and displays a bar plot representing the count of news
    articles classified by sentiment (Positive, Negative, Neutral).

    Args:
        data (list): A list of dictionaries containing news data with sentiments.

    Returns:
        None
    """
    # Write an explanation
    st.write("The bar plot represents the count of news articles classified by sentiment: Positive, Negative, and Neutral. This visualization provides a clear comparison of the number of articles corresponding to each sentiment category.")
    
    # Extract sentiments
    sentiments = [item['sentiment'] for item in data]
    
    # Count occurrences of each sentiment
    sentiment_counts = Counter(sentiments)
    
    # Prepare data for the bar chart
    labels = list(sentiment_counts.keys())
    values = list(sentiment_counts.values())
    
    # Create a bar plot
    fig, ax = plt.subplots()
    ax.bar(labels, values, color='skyblue')
    
    # Set titles and labels
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Count')
    
    # Display the plot in Streamlit
    st.pyplot(fig)

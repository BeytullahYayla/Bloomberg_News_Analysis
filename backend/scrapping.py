import requests
from bs4 import BeautifulSoup
import time
from constants import *
from bloomberg_database import BloombergNewDatabase
from gpt_sentiment_classifier import GptSentimentClassifier


class NewsScraper:
    """
    A class to scrape news data from BloombergHT and store it in a database
    with sentiment analysis using GPT.

    Attributes:
    -----------
    url : str
        The URL of the news page to scrape.
    database : BloombergNewDatabase
        An instance of the BloombergNewDatabase to store scraped news.
    classifier : GptSentimentClassifier
        An instance of GptSentimentClassifier to classify the sentiment of the news.
    """

    def __init__(self, url: str, database: BloombergNewDatabase, gpt_sentiment_classifier: GptSentimentClassifier):
        """
        Initializes the NewsScraper with a URL, database instance, and sentiment classifier.

        Parameters:
        -----------
        url : str
            The URL of the news page to scrape.
        database : BloombergNewDatabase
            An instance of the BloombergNewDatabase to store scraped news.
        gpt_sentiment_classifier : GptSentimentClassifier
            An instance of GptSentimentClassifier to classify the sentiment of the news.
        """
        self.url = url
        self.database = database
        self.classifier = gpt_sentiment_classifier
        
    def __fetch_page(self, url: str):
        """
        Fetches the HTML content of the given URL.

        Parameters:
        -----------
        url : str
            The URL of the page to fetch.

        Returns:
        --------
        soup : BeautifulSoup object or None
            The BeautifulSoup object if the page is successfully fetched; otherwise, None.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None
        
    def __get_news_from_page(self, soup: BeautifulSoup):
        """
        Extracts news articles from the page and stores them in the database with sentiment analysis.

        Parameters:
        -----------
        soup : BeautifulSoup
            The BeautifulSoup object containing the HTML content of the page.

        Returns:
        --------
        None
        """
        news_div = soup.find("div", class_="widget-news-list type1")

        if news_div:
            news_list = news_div.find("ul")
            if news_list:
                for item in news_list.find_all("li"):
                    title = item.find("span", class_="title").text.strip()
                    link = item.find("a")["href"]
                    description = item.find("span", class_="description").text.strip()
                    date = item.find("span", class_="date").text.strip()
                    full_link = f"https://www.bloomberght.com{link}"
                    
                    if self.database.get_new_by_title(title) == []:  # Control if data is already existing in database
                        sentiment = str(self.classifier.classify_sentence(description))
                        self.database.add_new(title, description, sentiment, date)
                        print(f"Title: {title}\nDescription: {description}\nSentiment: {sentiment}\nDate: {date}")
                    else:
                        print("Data is already existing in the database")
                    
                    print()
                    time.sleep(5)
            else:
                print("No 'ul' found within the specified div.")
        else:
            print("No div with the specified class found.")
        
    def __get_next_page_url(self, soup: BeautifulSoup):
        """
        Extracts the URL of the next page from the current page's pagination section.

        Parameters:
        -----------
        soup : BeautifulSoup
            The BeautifulSoup object containing the HTML content of the page.

        Returns:
        --------
        full_next_page_url : str or None
            The full URL of the next page if available; otherwise, None.
        """
        page_div = soup.find("div", class_="widget-pager type1")

        if page_div:
            next_page = page_div.find("a", title="Sonraki")
            if next_page:
                next_page_url = next_page["href"]
                full_next_page_url = f"https://www.bloomberght.com{next_page_url}"
                print(f"Next Page URL: {full_next_page_url}")
                return full_next_page_url
            else:
                print("No more pages to fetch.")
                return None
        else:
            print("No pagination div found.")
            return None
        
    def run(self):
        """
        Starts the news scraping process. It fetches pages iteratively, extracts news articles,
        performs sentiment analysis, and stores the results in the database.

        Returns:
        --------
        None
        """
        current_url = self.url
        while current_url:
            print(f"Fetching data from {current_url}...")
            soup = self.__fetch_page(current_url)
            if soup:
                self.__get_news_from_page(soup)
                current_url = self.__get_next_page_url(soup)
                if current_url:
                    print("Moving to the next page...")
                    time.sleep(5)  # Adding a delay before moving to the next page
                else:
                    print("No more pages found. Stopping.")
                    break
            else:
                print("Failed to fetch the page. Stopping.")
                break

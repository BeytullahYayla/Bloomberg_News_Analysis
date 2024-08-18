import requests
from bs4 import BeautifulSoup
import time
from constants import *
from bloomberg_database import BloombergNewDatabase
from gpt_sentiment_classifier import GptSentimentClassifier


class NewsScraper:
    """
    A class used to scrape news articles from a given URL.

    Attributes:
    -----------
    url : str
        The URL to start scraping from.
    database : BloombergNewDatabase
        An instance of the BloombergNewDatabase class to store the scraped news data.
    """

    def __init__(self, url: str, database: BloombergNewDatabase,gpt_sentiment_classifier:GptSentimentClassifier):
        """
        Initializes the NewsScraper with the provided URL and database.

        Parameters:
        -----------
        url : str
            The URL from which to start scraping.
        database : BloombergNewDatabase
            An instance of the BloombergNewDatabase class where the news data will be stored.
        """
        self.url = url
        self.database = database
        self.classifier=gpt_sentiment_classifier
        
    def __fetch_page(self, url):
        """
        Fetches the HTML content of the provided URL.

        Parameters:
        -----------
        url : str
            The URL to fetch the HTML content from.

        Returns:
        --------
        soup : BeautifulSoup object or None
            The parsed HTML content as a BeautifulSoup object. Returns None if the request fails.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None
        
    def __get_news_from_page(self, soup):
        """
        Extracts news data from the HTML content and stores it in the database.

        Parameters:
        -----------
        soup : BeautifulSoup object
            The parsed HTML content from which to extract news data.

        Returns:
        --------
        news_list_data : list
            A list of dictionaries, each containing the title, link, description, and date of a news article.
        """
        news_list_data = []
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
                    sentiment=str(self.classifier.classify_sentence(description))
                    news_list_data.append({
                        "title": title,
                        "link": full_link,
                        "description": description,
                        "sentiment_analysis":sentiment,
                        "date": date
                    })
                    
                    self.database.add_new(title, description, sentiment, date)
                    
                    print(f"Title: {title}\nDescription: {description}\nSentiment:{sentiment}\nDate:{date}")
                    print()
                    time.sleep(5)
            else:
                print("No 'ul' found within the specified div.")
        else:
            print("No div with the specified class found.")
        
        return news_list_data
            
    def __get_next_page_url(self, soup):
        """
        Extracts the URL of the next page from the HTML content.

        Parameters:
        -----------
        soup : BeautifulSoup object
            The parsed HTML content from which to extract the next page URL.

        Returns:
        --------
        full_next_page_url : str or None
            The full URL of the next page. Returns None if no next page is found.
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
        Starts the news scraping process, iterating through pages until no more pages are found.

        The function continuously fetches, processes, and stores news data from the current URL
        and then moves to the next page if available.

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

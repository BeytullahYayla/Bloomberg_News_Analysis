from bloomberg_database import BloombergNewDatabase
from constants import *
from scrapping import NewsScraper


if __name__=='__main__':
    
    bloomberg_db=BloombergNewDatabase(USER,PASSWORD,HOST,DB_NAME,PORT)
    scrapper=NewsScraper(SOURCE_URL,bloomberg_db)
    scrapper.run()
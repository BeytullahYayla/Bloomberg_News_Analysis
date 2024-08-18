from bloomberg_database import BloombergNewDatabase
from constants import *
from scrapping import NewsScraper
from gpt_sentiment_classifier import GptSentimentClassifier
import ast 

if __name__=='__main__':
    
    bloomberg_db=BloombergNewDatabase(USER,PASSWORD,HOST,DB_NAME,PORT)
    
    message_history=open('message_history.txt',"r",encoding="utf-8").read()
    message_history=ast.literal_eval(message_history)
    
    gpt_sentiment_classifier=GptSentimentClassifier(message_history)
    
    #dependency injection
    scrapper=NewsScraper(SOURCE_URL,bloomberg_db,gpt_sentiment_classifier)
    scrapper.run()
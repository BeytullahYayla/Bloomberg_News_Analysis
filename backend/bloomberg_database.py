import mysql.connector
from datetime import datetime


class BloombergNewDatabase():
    def __init__(self,user,password,host,db_name,port) -> None:
        try:
            self.conn = mysql.connector.connect(#start database connectionm- with the provided informations
                user=user,
                password=password,
                host=host,
                database=db_name,
                port=port
            )
            self.cursor=self.conn.cursor()
            print("Connected to database successfully")
        except :
            print("Occured an error while connecting database")
            
            
    def __list_all_news(self):
        query="SELECT * FROM NEWS"
        try:
            
            self.cursor.execute(query)
            record=self.cursor.fetchall()
            return record 
        except:
            print("An error occurred while listing data")
    def get_new_by_title(self,title:str):
        query="SELECT * FROM NEWS WHERE id = (SELECT id from NEWS WHERE title = %s)"
        try:
            
            self.cursor.execute(query,(title,))
            record=self.cursor.fetchall()
            return record
        
        except:
            print("An error occured while getting data by title")
            
         
    def add_new(self,title:str,description:str,sentiment_analysis:str,publish_date:str):
        query = "INSERT INTO NEWS (title,description,sentiment,publish_date) VALUES (%s,%s, %s, %s)"
        try:
            self.cursor.execute(query,(title,description,sentiment_analysis,publish_date))
            self.conn.commit()
            print("Data Added Successfully")   
                     
        except:
            print("An error occured while adding data to database")
        
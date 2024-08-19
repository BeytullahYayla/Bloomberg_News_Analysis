import mysql.connector
from mysql.connector import Error
from datetime import datetime

class BloombergNewDatabase:
    """
    A class to interact with the Bloomberg news database.

    Attributes:
    -----------
    conn : mysql.connector.connection_cext.CMySQLConnection
        The connection object to interact with the MySQL database.
    cursor : mysql.connector.cursor_cext.CMySQLCursor
        The cursor object to execute SQL queries.
    """

    def __init__(self, user: str, password: str, host: str, db_name: str, port: int) -> None:
        """
        Initializes the database connection using the provided credentials.

        Parameters:
        -----------
        user : str
            The username to connect to the database.
        password : str
            The password to connect to the database.
        host : str
            The hostname of the database server.
        db_name : str
            The name of the database to connect to.
        port : int
            The port number of the database server.
        """
        try:
            self.conn = mysql.connector.connect(
                user=user,
                password=password,
                host=host,
                database=db_name,
                port=port
            )
            self.cursor = self.conn.cursor()
            print("Connected to the database successfully")
        except Error as e:
            print(f"An error occurred while connecting to the database: {e}")
    
    def list_all_news(self):
        """
        Retrieves all news records from the NEWS table.

        Returns:
        --------
        list of tuple
            A list of tuples where each tuple represents a record in the NEWS table.
        """
        query = "SELECT * FROM NEWS"
        try:
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records
        except Error as e:
            print(f"An error occurred while listing data: {e}")
    
    def get_new_by_title(self, title: str):
        """
        Retrieves a news record by its title.

        Parameters:
        -----------
        title : str
            The title of the news article to search for.

        Returns:
        --------
        list of tuple
            A list of tuples where each tuple represents a record in the NEWS table matching the title.
        """
        query = "SELECT * FROM NEWS WHERE id = (SELECT id FROM NEWS WHERE title = %s)"
        try:
            self.cursor.execute(query, (title,))
            records = self.cursor.fetchall()
            return records
        except Error as e:
            print(f"An error occurred while getting data by title: {e}")
    
    def add_new(self, title: str, description: str, sentiment_analysis: str, publish_date: str):
        """
        Adds a new record to the NEWS table.

        Parameters:
        -----------
        title : str
            The title of the news article.
        description : str
            A brief description of the news article.
        sentiment_analysis : str
            The sentiment analysis result of the news article.
        publish_date : str
            The publication date of the news article.
        """
        query = "INSERT INTO NEWS (title, description, sentiment, publish_date) VALUES (%s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (title, description, sentiment_analysis, publish_date))
            self.conn.commit()
            print("Data added successfully")
        except Error as e:
            print(f"An error occurred while adding data to the database: {e}")

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
            print("Database connection closed")

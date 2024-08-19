# Bloomberg Economy News Analysis


https://github.com/user-attachments/assets/d3ae4e29-d0b9-419c-aca2-827df7958bd5


## 🚩 Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Features](#features)
  * [Web Scrapping](#web-scrapping)
  * [Sentiment Analysis Using Chatgpt Api](#sentiment-analysis-using-chatgpt-api)
  * [Database Operations](#database-operations)
  * [Backend Server](#backend-server)
  * [Web User Interface](#web-user-interface)
- [How To Run on My Local Computer](#how-to-run-on-my-local-computer)
- [Contact Information](#contact-information)

## Project Overview
The project aims to create a system to scrape news articles from a specific website, store them in an SQL database, and ensure that duplicate articles are not stored. Additionally, a simple user interface (UI) should display the collected news, and there's an extra challenge to analyze the news using GPT API. 

## Technologies Used

- **Programming Languages**: Python
- **Frameworks**: FastAPI, Streamlit
- **Database**: MySQL
- **LLM Library**: OpenAI Chatgpt Api

## Features
### Web Scrapping
- In this section i have used beautifulsoup library to gather data from specific url.
- Created a class named <b> NewsScrapper </b> including methods to fetch data, add database gathered data if it's not already existing in database, and do sentiment analysis using chatgpt api.
- This class must get database and gpt_classifier objects when create an instance from it.
- With the run() function we can start and continue the process automatically.
- We control whether is data already added database before or not using get_new_by_title() method coming from database object.
  ![image](https://github.com/user-attachments/assets/25b25cd6-8f0a-4bfa-bdcd-27cbf46f2a2a)
- Example output of a running scrapping process
  ![Screenshot_1](https://github.com/user-attachments/assets/ad1ff2d5-eb65-4dfa-9bc2-094f57f36f9e)
### Sentiment Analysis Using Chatgpt Api
- In this section, the OpenAI API is utilized to classify the sentiment of sentences using the GPT model.
- Created a class named GptSentimentClassifier which includes methods to interact with the GPT model, manage message history, and classify sentiment.
- This class requires an initial message_history list when an instance is created, which represents the conversation history.
- The chat() function starts an interactive session where user input is processed by the GPT model, and the conversation is stored in the message_history.
- The classify_sentence() method is designed to classify the sentiment of a specific sentence using GPT-4. It adds the sentence to the message history, sends it to the model, and returns the sentiment result.
- The OpenAI API key is securely read from a file named key.txt within the class initializer, ensuring proper API access.

### Database Operations
- In this section, a connection to a MySQL database is established and managed to interact with Bloomberg news data.
- Created a class named BloombergNewDatabase which includes methods to connect to the database, retrieve news data, add new records, and close the database connection.
- This class requires the user, password, host, db_name, and port parameters to initialize a connection to the MySQL database.
- The list_all_news() method retrieves all records from the NEWS table, returning them as a list of tuples.
- The get_new_by_title() method searches for a specific news article by its title and returns the matching record(s) from the NEWS table.
- The add_new() method inserts a new news article record into the NEWS table, including the title, description, sentiment analysis, and publication date.
- The close_connection() method ensures the database connection is properly closed after operations are complete.

### Backend Server
- In this section, a RESTful API is built using FastAPI to interact with the web-scraped news data stored in a database.
- Created an API application titled Hagia Web Scraping which handles news data retrieval and supports Cross-Origin Resource Sharing (CORS) for specific origins.
- The get_database_connection() function is a dependency that provides a database session, ensuring it is properly closed after use.
- CORS middleware is added to the application to allow requests from specified origins such as localhost:4200, localhost:8000, and localhost:8080.
- The /news/ endpoint retrieves all news records from the database, returning them as a list of tables.New objects.
- The /news_paginated/ endpoint retrieves a paginated list of news records, with optional query parameters limit and offset to control the number of records returned and where to start retrieving records.
- SQLAlchemy is used to query the database, and HTTPException is raised to handle errors gracefully, providing appropriate HTTP status codes and error details.
![image](https://github.com/user-attachments/assets/ee3c7cd5-6008-47b4-ae65-55613732c8fe)

### Web User Interface
- In this section, two pages are created for a Streamlit web application: Bloomberg Economy News and Sentiment Distribution Analysis. Each page offers specific functionalities to display and analyze news data fetched from an API.
### <i>Bloomberg Economy News Page</i>
- <b>Title and Layout:</b> The page begins with a centered title, Bloomberg Economy News, displayed at the top.
- <b>Data Retrieval and Display:</b> The news data is fetched using the fetch_data function, and if data is available, it is prepared using the prepare_data function and displayed in a table using the create_table function.
- <b>Record Count:</b> A centered information box shows the total number of records fetched from the database. This is displayed using a styled st.markdown element.
- <b>Error Handling:</b> If no data is available, a warning message is shown using st.warning.

<p align="center">
  <img src="https://github.com/user-attachments/assets/a5aa722f-52d0-48a0-abdc-88d4236a7f01" width="45%" />
  <img src="https://github.com/user-attachments/assets/be2b0ad4-4d14-4ec9-b15d-4ae99b2a99b8" width="45%" />
</p>

### <i>Sentiment Distribution Analysis Page</i>

- <b>Title and Layout:</b> The page opens with a centered title, Sentiment Distribution of News, followed by an introductory explanation of the benefits of sentiment analysis on news data.
- <b>Data Retrieval and Visualization:</b> After fetching data, the sentiment distribution is visualized through a pie chart and a bar plot using the create_pie_chart and create_bar_plot functions, respectively.
- <b>Error Handling:</b> Similar to the news page, if no data is found, a warning message is shown using st.warning.
- Both pages rely on external utility functions like fetch_data, prepare_data, create_table, create_pie_chart, and create_bar_plot for data processing and visualization, which are assumed to be defined elsewhere in the codebase.

<p align="center">
  <img src="https://github.com/user-attachments/assets/af4d8f1f-cbb6-4f5f-80e0-42aa5326c99d" width="45%" />
  <img src="https://github.com/user-attachments/assets/6ec4b6f6-91c9-4f61-8819-32aa7ecabe8d" width="45%" />
</p>

## How To Run on My Local Computer

First of all, we are going to create an Anaconda virtual environment in order to manage dependencies effectively.

1. **Install Anaconda**: If you haven't already installed Anaconda, download and install it from [here](https://www.anaconda.com/products/distribution).

2. **Create a Virtual Environment**:
   - Open the Anaconda Prompt.
   - Create a new virtual environment using the following command:
     ```bash
     conda create -n myenv python=3.10
     ```
   - Replace `myenv` with your desired environment name.
   - Activate the virtual environment:
     ```bash
     conda activate myenv
     ```

3. **Install Dependencies**:
   - Navigate to the project directory:
     ```bash
     cd path_to_your_project_directory
     ```
   - Install the required Python packages using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Scripts**:

   - **Run the Web Scraping Script**:
     - This script enables the scraping process in ./backend path:
       ```bash
       python main.py
       ```

   - **Run the Uvicorn App**:
     - Start the Uvicorn application in ./backend path:
       ```bash
       uvicorn app:app --reload
       ```

   - **Run the Streamlit UI**:
     - Finally, launch the Streamlit UI in ./web_ui path:
       ```bash
       streamlit run main.py
       ```

5. **Access the Applications**:
   - Open your web browser:
     - For the Uvicorn app, go to `http://localhost:8000`.
     - For the Streamlit UI, go to `http://localhost:8501`.

This setup allows you to manage and run all three scripts effectively on your local machine.

## Contact Information


**Contributors:**
- Beytullah Yayla  
  Email: beytullahyayla1@gmail.com

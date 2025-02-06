# Mini-Project-1
Game Analytics: Unlocking Tennis Data with SportRadar API

# Tennis Data Web Application

This project involves fetching tennis data from external APIs, processing the data, and displaying it using a web application built with Streamlit. The data is stored and managed using PostgreSQL, and users can interact with the data through a user-friendly interface. The application includes features such as a dashboard, competitor search and filter, competitor details viewer, country-wise analysis, and leaderboards.

## Technologies Used

- **pandas**: Used for data manipulation and conversion into DataFrames.
- **requests**: Used to fetch data from external APIs.
- **psycopg2**: Used to connect to PostgreSQL and perform database operations.
- **SQLAlchemy**: Used to manage connections to PostgreSQL and interact with the database.
- **Streamlit**: Used to build the web application for displaying the dashboard and allowing user interactions.

## Steps Involved

### 1. Data Fetching

The data for competitors, rankings, and related information is fetched from the tennis API using the `requests` library. The API endpoints provide details such as competitor rankings, match data, venues, and more.

### 2. Data Transformation

The raw data from the API is converted into a structured format using the `pandas` library. Each dataset is converted into a DataFrame for further processing and manipulation. 

### 3. PostgreSQL Integration

The processed data is then inserted into a **PostgreSQL database**. The following steps are performed:
- Connected to the local PostgreSQL database using **psycopg2** and **SQLAlchemy**.
- Created tables for storing the data (e.g., `competitors`, `competitor_rankings`, `venues`, etc.).
- Used `pandas` to insert data into these tables.

### 4. Streamlit Web Application

The data is displayed through a web interface using **Streamlit**. The following features are available in the application:
- **Homepage**: Displays the dashboard with key statistics (e.g., total number of competitors, highest points, etc.).
- **Search and Filter**: Allows users to search for competitors by name, filter by rank range, country, or points.
- **Competitor Details**: Displays detailed information about a selected competitor (e.g., rank, country, points).
- **Country-Wise Analysis**: Lists countries with the total number of competitors and their average points.
- **Leaderboards**: Shows the top-ranked competitors and competitors with the highest points.

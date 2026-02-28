This project builds a Sports Analytics platform using real-time NCAA Football (NCAAFB) data.

It collects data from the Sportradar NCAAF API including teams, players, rankings, schedules, and seasons.

The project follows a structured ETL pipeline to extract, transform, and load data.

Raw API data is cleaned and standardized using Python data processing techniques.

The processed data is stored in a PostgreSQL relational database for efficient querying.

SQL queries are used to analyze team performance, ranking trends, and season statistics.

The system generates insights like top-ranked teams across seasons and average ranking points.

A Streamlit dashboard is built to visualize analytics in an interactive and user-friendly way.

The project demonstrates real-world data engineering concepts like API integration, database design, and modular architecture.

Overall, it provides a scalable platform for exploring and analyzing college football performance data.




Sportradar API (JSON)
        ↓
Data Extraction (Python)
        ↓
Data Transformation (Flatten + Clean)
        ↓
PostgreSQL Database
        ↓
SQL Analysis / Analytics

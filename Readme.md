![Jordan_picture](images/Jordan.jpeg)

# NBA Stats Scraper and Database Loader

## 📌 Project Overview

This project scrapes NBA player statistics from the official NBA website, cleans and processes the data, then stores it in both a PostgreSQL database and CSV files for analysis. The system handles special characters (like Nikola Jokić) through UTF-8 encoding and provides data backup capabilities.

## 🏗️ Project Structure
![nba](images/NBA.png

## 🛠️ Key Features

1. **Web Scraping**
   - Uses Selenium to scrape player stats from NBA.com
   - Handles pagination to collect complete datasets
   - Robust error handling for web elements

2. **Data Processing**
   - Cleans and standardizes column names
   - Converts numeric values to proper data types
   - Adds metadata (timestamp, season info)

3. **Database Integration**
   - PostgreSQL storage with UTF-8 encoding
   - Environment variable configuration for security
   - SQLAlchemy for ORM functionality

4. **Backup System**
   - Automatic CSV exports with timestamped filenames
   - Special character reporting

## ⚙️ Installation

1. Clone the repository
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   
3.Install dependencies:
```
pip install -r requirements.txt
```
4.Set up PostgreSQL and create a .env file with your database credentials:
```
DB_HOST=your_host
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT=5432
```

## 🚀 Usage
Run the main script:
```
python main_file.py
```

- The script will:

- Scrape data from NBA.com

- Clean and process the statistics

- Save to PostgreSQL

- Create a CSV backup

- Generate a character issues report

## Database Schema
- The player_stats table includes:

- Player information (name, team, position)

- Statistical data (points, rebounds, assists, etc.)

- Metadata (season, last update timestamp)

Initialize the database with:

```
psql -U your_user -d your_db -f init.db.sql
```

📄 File Descriptions
- main_file.py: Main script with all functionality

- init.db.sql: Database initialization script

- requirements.txt: Python dependencies

- TEST.sql: Example queries for testing

- nba_stats_YYYYMMDD.csv: Generated data backups

- character_issues_report.csv: Players with special characters






























   

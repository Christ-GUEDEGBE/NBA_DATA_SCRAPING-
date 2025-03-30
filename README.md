# � NBA Stats Scraper with PostgreSQL

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-336791)
![Docker](https://img.shields.io/badge/Docker-20.10%2B-2496ED)
![Data Analysis](https://img.shields.io/badge/Potential_Use_Cases-Data_Analysis%7CML%7CVisualization-FFA500)

This project provides an automated pipeline to collect, store, and analyze NBA player statistics, designed for easy extension to data analysis and machine learning projects. Here's exactly how it works:

1. **The Scraper (`scripts/nba_scraper.py`)**:
   - Uses Selenium to extract player data from [NBA.com/stats](https://www.nba.com/stats)
   - Handles pagination to collect complete datasets
   - Cleans and prepares the data (handling special characters like ć, é, etc.)
   - Saves results to both PostgreSQL and CSV

2. **The Database Setup**:
   - PostgreSQL runs in a Docker container for easy setup
   - Automatic table creation with proper data types
   - Special configuration for UTF-8 character support

3. **The Environment**:
   - Virtual environment (`.venv` folder) isolates dependencies
   - `requirements.txt` lists all required Python packages
   - `.env` file stores sensitive configuration separately


## 🏗️ Project Structure

NBA_SCRAPER/
├── docker/
│ └── postgres/ # PostgreSQL configuration
│ ├── init.sql # Database initialization
│ └── pgdata/ # Persistent volume
├── scripts/
│ └── nba_scraper.py # Main scraping script
├── data/ # Auto-generated CSV exports
├── .env # Environment variables
├── docker-compose.yml # Docker orchestration
├── requirements.txt # Python dependencies
└── README.md # This file


## 🚀 Getting Started

### Prerequisites
- Docker Desktop ([download](https://www.docker.com/products/docker-desktop))
- Python 3.9+

### Installation
```bash
git clone https://github.com/your-username/nba-scraper.git
cd nba-scraper

# Set up environment
cp .env.example .env
nano .env  # Edit with your credentials

# Launch services
docker-compose up -d
pip install -r requirements.txt
python scripts/nba_scraper.py
```












# NBA STATS SCRAPER AND DATABASE LOADER
# -------------------------------------
# This script:
# 1. Scrapes NBA player statistics from the official NBA website
# 2. Cleans and processes the data
# 3. Saves to PostgreSQL database
# 4. Exports to CSV as backup

# Import required libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration - using environment variables for security
DB_CONFIG = {
    "host": os.getenv('DB_HOST', 'localhost'),  # Default to localhost if not set
    "database": os.getenv('DB_NAME', ''),
    "user": os.getenv('DB_USER', ''),
    "password": os.getenv('DB_PASSWORD', ''),
    "port": os.getenv('DB_PORT', '')
}

# ==============================================
# DATABASE CONNECTION FUNCTIONS
# ==============================================

def init_db_connection():
    """
    Initialize and return a PostgreSQL database connection using SQLAlchemy
    Returns:
        engine: SQLAlchemy engine object or None if connection fails
    """
    try:
        connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)
        print("✅ Successfully connected to PostgreSQL database")
        return engine
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def save_to_postgres(df, table_name="player_stats", engine=None):
    """
    Save cleaned NBA stats data to PostgreSQL database
    Args:
        df: Pandas DataFrame containing cleaned data
        table_name: Name of the target table (default: 'player_stats')
        engine: SQLAlchemy engine (if None, will initialize new connection)
    """
    if engine is None:
        engine = init_db_connection()
    
    if engine is None:
        print("❌ Cannot save data - no database connection")
        return

    try:
        with engine.connect() as conn:
            # Set client encoding to UTF-8
            conn.execute(text("SET client_encoding TO 'UTF8';"))
            
            # Save DataFrame to PostgreSQL
            df.to_sql(
                table_name,
                engine,
                if_exists='replace',
                index=False,
                method='multi'
            )
        print("✅ Data successfully saved to PostgreSQL")
    except Exception as e:
        print(f"❌ Error saving to database: {str(e)}")

# ==============================================
# WEB SCRAPING FUNCTIONS
# ==============================================

def configure_browser():
    """
    Configure Chrome browser options for headless scraping
    Returns:
        Options: Configured Chrome options object
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return chrome_options

def scrape_nba_stats_with_selenium():
    """
    Scrape NBA player statistics from the official NBA stats website
    Returns:
        tuple: (headers, rows, dataframe) containing the scraped data
    """
    print("Starting NBA stats scraping with Selenium...")

    try:
        # Initialize browser with configured options
        chrome_options = configure_browser()
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Target URL for scraping
        url = 'https://www.nba.com/stats/players/traditional?PerMode=Totals&dir=A&sort=TD3&Season=2024-25'
        print(f"Navigating to: {url}")
        driver.get(url)

        # Wait for main data table to load
        print("⏳ Waiting for data table to load...")
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Crom_table__p1iZz')))

        # Attempt to close any popups
        try:
            popup = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close"]')
            popup.click()
            print("✅ Closed popup dialog")
            time.sleep(1)
        except Exception:
            print("ℹ️ No popup found or could not close it")

        # Extract table headers
        headers = []
        header_elements = driver.find_elements(By.CSS_SELECTOR, '.Crom_headers__mzI_m th')
        for header in header_elements:
            if header.get_attribute('field'):
                headers.append(header.get_attribute('field'))
            elif header.get_attribute('title'):
                headers.append(header.get_attribute('title'))
            else:
                headers.append(header.text.strip())

        # Clean headers and add row number column
        headers = [h for h in headers if h]
        headers.insert(0, 'row_number')

        # Pagination and data collection
        all_rows = []
        max_pages = 12
        current_page = 1

        while current_page <= max_pages:
            time.sleep(2)  # Respectful delay

            # Extract current page rows
            row_elements = driver.find_elements(By.CSS_SELECTOR, '.Crom_body__UYOcU tr')
            for row_element in row_elements:
                row_data = [cell.text.strip() for cell in row_element.find_elements(By.TAG_NAME, 'td')]
                if row_data:
                    all_rows.append(row_data)

            print(f"Processed page {current_page} - Total rows: {len(all_rows)}")

            # Navigate to next page
            try:
                next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-pos="next"]')))
                
                if 'disabled' in next_button.get_attribute('class'):
                    print("ℹ️ Reached the last page of data")
                    break

                driver.execute_script("arguments[0].scrollIntoView();", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                print("➡️ Navigating to next page...")
                current_page += 1
                time.sleep(2)
                wait.until(EC.staleness_of(row_elements[0]))

            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                print(f"⚠️ Pagination error: {str(e)}")
                break

        # Create DataFrame
        df = pd.DataFrame(all_rows, columns=headers[:30]) if all_rows else pd.DataFrame()
        driver.quit()

        return headers, all_rows, df

    except Exception as e:
        print(f"❌ Scraping failed with error: {e}")
        try:
            driver.quit()
        except:
            pass
        return [], [], pd.DataFrame()

# ==============================================
# DATA CLEANING FUNCTIONS
# ==============================================

def clean_nba_data(df):
    """
    Clean and preprocess the scraped NBA data
    Args:
        df: Raw DataFrame from scraping
    Returns:
        df: Cleaned DataFrame
    """
    if df.empty:
        return df

    # Convert numeric columns
    numeric_cols = ['PTS', 'AST', 'TRB', 'FG%', '3P%', 'FT%', 'AGE']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Standardize column names
    df.columns = [col.lower().replace('%', '_pct') for col in df.columns]

    # Add metadata
    df['last_update'] = pd.Timestamp.now()
    df['season'] = '2024-25'

    return df

# ==============================================
# MAIN EXECUTION
# ==============================================

def main():
    """
    Main execution workflow:
    1. Scrape data from NBA website
    2. Clean and process the data
    3. Save to PostgreSQL database
    4. Export to CSV as backup
    """
    # Step 1: Scrape the data
    print("\n=== SCRAPING PHASE ===")
    headers, rows, raw_df = scrape_nba_stats_with_selenium()

    if raw_df.empty:
        print("❌ No data was scraped - exiting")
        return

    # Step 2: Clean the data
    print("\n=== DATA CLEANING PHASE ===")
    cleaned_df = clean_nba_data(raw_df)
    print("\nSample of cleaned data:")
    print(cleaned_df.head())

    # Step 3: Save to PostgreSQL
    print("\n=== DATABASE SAVE PHASE ===")
    db_engine = init_db_connection()
    save_to_postgres(cleaned_df, engine=db_engine)

    # Step 4: Save to CSV as backup
    print("\n=== BACKUP PHASE ===")
    csv_filename = f"nba_stats_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
    cleaned_df.to_csv(csv_filename, index=False)
    print(f"✅ Data backup saved to {csv_filename}")

    # Create character issues report
    problem_report = cleaned_df[cleaned_df.apply(lambda x: x.str.contains(r'[^\x00-\x7F]').any(), axis=1)]
    problem_report.to_csv("character_issues_report.csv", 
                      columns=['player_name'],
                      index=False)
    print("ℹCharacter issues report generated")
    # Save csv as a backup

if __name__ == "__main__":
    main()
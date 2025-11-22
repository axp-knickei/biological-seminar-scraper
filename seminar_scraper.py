# seminar_scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import re
from urllib.parse import urljoin, urlparse
import logging
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

logger = logging.getLogger(__name__)

class SeminarScraper:
    def __init__(self):
        self.driver = self._init_driver()
        self.output_dir = config.OUTPUT_DIR
        self.columns = config.COLUMNS

    def _init_driver(self):
        """
        Initializes a headless Chrome webdriver with anti-detection measures.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # The following options are added to make the Selenium-controlled browser
        # appear more like a normal browser and avoid bot detection.
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def fetch_page(self, url):
        """Fetches a web page using Selenium to handle dynamic content."""
        try:
            self.driver.get(url)
            # Use an explicit wait to allow time for dynamic content to load.
            # This waits up to 10 seconds for an element with the class 'front-item-box'
            # to appear on the page.
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "front-item-box"))
            )
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Error fetching {url} with Selenium: {e}")
            # If an error occurs (e.g., a timeout), save the page source for debugging.
            with open("page_source_on_error.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            return None

    def parse_date_improved(self, date_str):
        """Enhanced date parsing with better 2025-2026 filtering."""
        if not date_str or 'Not known' in str(date_str) or not isinstance(date_str, str):
            return 'Not known'
        
        date_str = re.sub(r'[^\w\s\-\/.]', '', date_str).strip()
        
        current_year = datetime.now().year
        target_years = config.TARGET_YEARS
    
        try:
            year = None
            for y in target_years:
                if str(y) in date_str:
                    year = y
                    break
            
            if year is None:
                return 'Not known'
        
            parsed_date = None
            date_formats = [
                "%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y",
                "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d",
                "%d %b", "%b %d", "%d.%m.", "%d.%m.%Y"
            ]
        
            date_str_for_parsing = date_str
            if not any(str(y) in date_str for y in range(current_year - 5, current_year + 5)) and year:
                date_str_for_parsing = f"{date_str} {year}"
        
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str_for_parsing, fmt)
                    if parsed_date.year in target_years:
                        break
                    else:
                        parsed_date = None
                except ValueError:
                    try:
                        temp_date = datetime.strptime(date_str, fmt)
                        if temp_date.year == 1900:
                            temp_date = temp_date.replace(year=year)
                        if temp_date.year in target_years:
                            parsed_date = temp_date
                            break
                    except ValueError:
                        continue
            if parsed_date:
                if parsed_date.year in target_years:
                    return parsed_date.strftime('%Y-%m-%d')
                else:
                    return 'Not known'
            else:
                return 'Not known'

        except Exception as e:
            logger.debug(f"Could not parse date '{date_str}': {e}")
            return 'Not known'

    def parse_seminar_data(self, html_content, base_url):
        """
        Parses the HTML content to extract seminar data.
        
        NOTE: This method is highly dependent on the HTML structure of the target
        website. The current implementation is tailored for allconferencealert.net.
        If you are scraping a different website, you will need to inspect its
        HTML and modify the selectors accordingly.
        
        CURRENT CHALLENGE: As of the last test, allconferencealert.net is
        successfully detecting and blocking our scraper, even with Selenium and
        anti-detection measures. This results in the 'front-item-box' elements
        not being loaded. More advanced techniques are likely needed to bypass
        this. See the "Current Challenges" section in README.md for more details.
        """
        soup = BeautifulSoup(html_content, 'lxml')
        seminars = []

        listings = soup.find_all('div', class_='front-item-box')
        logger.info(f"Found {len(listings)} conference listings.")

        for item in listings:
            try:
                name_element = item.find('h2')
                name = name_element.text.strip() if name_element else 'Not found'
                
                link_element = name_element.find('a') if name_element else None
                link = urljoin(base_url, link_element['href']) if link_element else 'Not found'

                details = item.find_all('span')
                
                conference_dates_str = 'Not known'
                city_country = 'Not found'
                organizer = 'Not found'
                key_topic_description = 'Not found'
                
                for detail in details:
                    text = detail.text.strip()
                    if "Conference Date" in text:
                        conference_dates_str = text.replace('Conference Date', '').strip()
                    elif "Venue" in text:
                        city_country = text.replace('Venue', '').strip()
                    elif "Organizer" in text:
                        organizer = text.replace('Organizer', '').strip()
                    elif "Event Type" in text:
                        key_topic_description = text.replace('Event Type', '').strip()

                conference_dates = self.parse_date_improved(conference_dates_str)
                
                abstract_deadline = 'Not known'

                seminars.append({
                    'Name': name,
                    'City_Country': city_country,
                    'Conference_Dates': conference_dates,
                    'Abstract_Submission_Deadline': abstract_deadline,
                    'Key_Topic_Description': key_topic_description,
                    'Organizer': organizer,
                    'Link': link
                })
            except Exception as e:
                logger.error(f"Error parsing a seminar item: {e}")
                continue

        return seminars

    def save_data(self, data, filename="biological_seminars.csv"):
        if not data:
            logger.info("No data to save.")
            return

        df = pd.DataFrame(data, columns=self.columns)
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, filename)
        df.to_csv(output_file, index=False)
        logger.info(f"Data saved to {output_file}")

    def run(self, base_urls, filename="biological_seminars.csv"):
        all_seminars = []
        if not base_urls:
            logger.warning("No URLs provided to scrape.")
            return

        for base_url in base_urls:
            logger.info(f"Scraping {base_url}...")
            html_content = self.fetch_page(base_url)
            if html_content:
                seminars_on_page = self.parse_seminar_data(html_content, base_url)
                all_seminars.extend(seminars_on_page)
            else:
                logger.error(f"Could not fetch or parse {base_url}")
        
        self.save_data(all_seminars, filename)
        logger.info("Scraping process finished.")
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

import config

logger = logging.getLogger(__name__)

class SeminarScraper:
    def __init__(self):
        self.session = self._create_session_with_retries()
        self.output_dir = config.OUTPUT_DIR
        self.columns = config.COLUMNS # Assuming COLUMNS will be moved to config

    def _create_session_with_retries(self):
        """Create a request session with automatic retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=config.RETRY_TOTAL,
            backoff_factor=config.RETRY_BACKOFF_FACTOR,
            status_forcelist=config.RETRY_STATUS_FORCELIST,
            allowed_methods=config.RETRY_ALLOWED_METHODS
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _get_headers(self):
        """Return randomized headers to avoid bot detection."""
        return {
            'User-Agent': random.choice(config.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }

    def fetch_page(self, url):
        """Fetches a web page with randomized headers and retry mechanism."""
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=10)
            response.raise_for_status()
            time.sleep(random.uniform(1, 3)) # Introduce a random delay
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def parse_date_improved(self, date_str):
        """Enhanced date parsing with better 2025-2026 filtering."""
        if not date_str or 'Not known' in str(date_str) or not isinstance(date_str, str):
            return 'Not known'
        
        # Clean the date string - remove extra characters including commas
        date_str = re.sub(r'[^\w\s\-\/.]', '', date_str).strip()
        
        # Current year for context
        current_year = datetime.now().year
        target_years = config.TARGET_YEARS
    
        try:
            # Look for explicit years first with a more flexible approach
            year = None
            for y in target_years:
                if str(y) in date_str:
                    year = y
                    break
            
            if year is None:
                return 'Not known'
        
            # Attempt to parse date with various formats
            parsed_date = None
            date_formats = [
                "%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y", # No commas in formats
                "%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d",
                "%d %b", "%b %d", "%d.%m.", "%d.%m.%Y"
            ]
        
            # Add year to string if not explicitly present for formats that need it
            date_str_for_parsing = date_str
            # If the date_str doesn't contain a full year, but we've identified one, append it
            if not any(str(y) in date_str for y in range(current_year - 5, current_year + 5)) and year: # crude check if year is missing
                date_str_for_parsing = f"{date_str} {year}"
        
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str_for_parsing, fmt)
                    # Check if the parsed year matches the identified year or is within target years
                    if parsed_date.year == year or parsed_date.year in target_years:
                        break
                    else: # If parsed year doesn't match, it might be a different year, so continue
                        parsed_date = None
                except ValueError:
                    # If format with year failed, try formats without explicit year (e.g., "Oct 15")
                    try:
                        temp_date = datetime.strptime(date_str, fmt)
                        if temp_date.year == 1900: # Default year for strptime if not specified
                            temp_date = temp_date.replace(year=year) # Use the identified year
                        if temp_date.year == year or temp_date.year in target_years:
                            parsed_date = temp_date
                            break
                    except ValueError:
                        continue
            if parsed_date:
                # Final check if the parsed date is within the target years
                if parsed_date.year in target_years:
                    return parsed_date.strftime('%Y-%m-%d')
                else:
                    return 'Not known' # Date is not in target years
            else:
                # If still not parsed, a final attempt with year inference for month/day only strings
                for fmt in date_formats:
                    try:
                        temp_date = datetime.strptime(date_str, fmt)
                        if temp_date.year == 1900:
                            temp_date = temp_date.replace(year=year)
                        if temp_date.year in target_years:
                            return temp_date.strftime('%Y-%m-%d')
                    except ValueError:
                        continue
                return 'Not known'

        except Exception as e:
            logger.debug(f"Could not parse date '{date_str}': {e}")
            return 'Not known'

    def parse_seminar_data(self, html_content, base_url):
        """Parses the HTML content to extract seminar data."""
        soup = BeautifulSoup(html_content, 'lxml')
        seminars = []
        
        # Find the main container for seminar listings
        seminar_list_container = soup.find('div', id='seminar-list')
        if not seminar_list_container:
            logger.warning("Could not find the seminar list container on the page.")
            return seminars

        # Iterate through each seminar item
        for item in seminar_list_container.find_all('div', class_='seminar-item'):
            try:
                # Extracting seminar name and link
                name_element = item.find('h2', class_='seminar-title')
                name = name_element.text.strip() if name_element else 'Not found'
                
                link_element = name_element.find('a') if name_element else None
                link = urljoin(base_url, link_element['href']) if link_element else 'Not found'

                # Extracting city and country
                location_element = item.find('span', class_='seminar-location')
                city_country = location_element.text.strip() if location_element else 'Not found'

                # Extracting conference dates
                date_element = item.find('span', class_='seminar-date')
                conference_dates = self.parse_date_improved(date_element.text.strip()) if date_element else 'Not known'
                
                # Extracting abstract submission deadline
                details_container = item.find('div', class_='seminar-details')
                abstract_deadline_text = 'Not known'
                if details_container:
                    # Find span containing "Abstract Deadline"
                    for span in details_container.find_all('span'):
                        if 'Abstract Deadline' in span.text:
                            abstract_deadline_text = span.text.replace('Abstract Deadline:', '').strip()
                            break
                abstract_deadline = self.parse_date_improved(abstract_deadline_text)

                # Extracting key topic description
                description_element = item.find('p', class_='seminar-description')
                key_topic_description = description_element.text.strip() if description_element else 'Not found'

                # Extracting organizer
                organizer_text = 'Not found'
                if details_container:
                     for span in details_container.find_all('span'):
                        if 'Organizer' in span.text:
                            organizer_text = span.text.replace('Organizer:', '').strip()
                            break
                organizer = organizer_text

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
        """Saves the scraped data to a CSV file."""
        if not data:
            logger.info("No data to save.")
            return

        df = pd.DataFrame(data, columns=self.columns)
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, filename)
        df.to_csv(output_file, index=False)
        logger.info(f"Data saved to {output_file}")

    def run(self, base_urls, filename="biological_seminars.csv"):
        """Orchestrates the scraping process."""
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
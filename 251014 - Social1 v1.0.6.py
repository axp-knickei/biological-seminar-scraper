# Version 1.0.6

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

## Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

COLUMNS = ['Name', 'City_Country', 'Conference_Dates', 'Abstract_Submission_Deadline', 'Key_Topic_Description', 'Organizer', 'Link']

def create_session_with_retries():
    """Create a request session with automatic retry strategy."""
    session = request.Session()

    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

def get_headers():
    """Return randomized headers to avoid bot detection."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ,
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ,
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
    ]

    return {
        'User-Agent': random.choice(user_agents),
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

def parse_date_improved(date_str):
    """Enhanced date parsing with better 2025-2026 filtering."""
    if not date_str or 'Not known' in str(date_str) or not isinstance(date_str, str):
        return 'Not known'
    
    # Clean the date string
    date_str = re.sub(r'[^\w\s\-\/,.]', '', date_str).strip()
    
    # Current year for context
    current_year = datetime.now().year
    target_years = [2025, 2026]

    try:
        # Look for explicit years first
        year_match = re.search(r'202[5-6]', date_str)
        if year_match:
            year = int(year_match.group())
        else:
            # If no year found, skip this retry
            return 'Not known'
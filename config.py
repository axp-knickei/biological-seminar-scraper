# config.py

# User-Agent strings for the scraper
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36'
]

# Retry strategy for requests
RETRY_TOTAL = 3
RETRY_BACKOFF_FACTOR = 1
RETRY_STATUS_FORCELIST = [429, 500, 502, 503, 504]
RETRY_ALLOWED_METHODS = ["HEAD", "GET", "OPTIONS"]

# Target years for date parsing and filtering
TARGET_YEARS = [2025, 2026]

# Output directory for CSV files
OUTPUT_DIR = "output"

# Columns for the output CSV file
COLUMNS = ['Name', 'City_Country', 'Conference_Dates', 'Abstract_Submission_Deadline', 'Key_Topic_Description', 'Organizer', 'Link']

# Base URLs to scrape (example - you'll need to add your actual target URLs here)
# Example:
# BASE_URLS = [
#     "https://example.com/conferences",
#     "https://anothersite.org/seminars"
# ]
BASE_URLS = [] # Placeholder, to be filled with actual URLs.

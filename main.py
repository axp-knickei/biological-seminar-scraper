import logging
import argparse
from seminar_scraper import SeminarScraper
import os

## Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to run the seminar scraper."""
    parser = argparse.ArgumentParser(description="Scrape biological seminars from web pages.")
    parser.add_argument(
        '--urls', 
        nargs='+', 
        required=True, 
        help="One or more URLs to scrape."
    )
    parser.add_argument(
        '--output', 
        default="biological_seminars.csv", 
        help="Output CSV file name. (default: biological_seminars.csv)"
    )
    args = parser.parse_args()

    logger.info(f"Starting seminar scraper for URLs: {args.urls}")
    with SeminarScraper() as scraper:
        scraper.run(base_urls=args.urls, filename=args.output)
    logger.info("Scraping process completed.")

if __name__ == "__main__":
    main()
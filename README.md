# Biological Seminar Web Scraper

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

A Python web scraper designed to collect information about biological seminars and conferences. This tool automatically extracts conference details including names, locations, dates, abstract submission deadlines, topics, organizers, and links.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Output](#output)
- [Configuration](#configuration)
- [Testing](#testing)
- [Current Challenges](#current-challenges)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## ✨ Features

- **Automated Data Collection**: Scrapes conference and seminar information from biological science websites
- **Robust Error Handling**: Implements retry strategies and logging for reliable data collection
- **Dynamic Content Handling**: Uses Selenium to render JavaScript-heavy websites.
- **Smart Date Parsing**: Enhanced date parsing with filtering for 2025-2026 events
- **Anti-Bot Detection**: Randomized headers and delays to avoid being blocked
- **Structured Output**: Exports data to CSV format with organized columns
- **Command-Line Interface**: Flexible CLI for specifying URLs and output files.
- **Test Suite**: Includes unit and integration tests to ensure reliability.

## 🔧 Prerequisites

Before running this scraper, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Google Chrome (or another browser compatible with Selenium)
- The necessary system dependencies for your webdriver (see "Current Challenges" for details).

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/biological-seminar-scraper.git
cd biological-seminar-scraper
```

2. **Create a virtual environment** (recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install required dependencies**

```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the scraper using the `main.py` script with the following command-line arguments:

```bash
python3 main.py --urls <URL1> <URL2> ... --output <FILENAME>.csv
```

- `--urls`: (Required) One or more URLs to scrape.
- `--output`: (Optional) The name of the output CSV file. Defaults to `biological_seminars.csv`.

### Example

```bash
python3 main.py --urls https://example.com/seminars http://anothersite.org/events --output my_seminars.csv
```

The scraper will:
1. Connect to the target websites.
2. Extract seminar and conference information.
3. Parse dates and filter for events in the configured years.
4. Export the results to the specified CSV file.

## 📁 Project Structure

```
biological-seminar-scraper/
├── main.py                     # Main entry point for the scraper
├── seminar_scraper.py          # Contains the SeminarScraper class and core logic
├── config.py                   # Configuration file for settings
├── requirements.txt            # Python dependencies
├── tests/                      # Test suite for the scraper
│   ├── test_date_parsing.py    # Unit tests for date parsing
│   └── test_scraper.py         # Integration tests for the scraper
├── test_data/                  # Dummy data for testing
│   └── dummy_seminars.html     # Sample HTML file for testing
├── output/                     # Directory for output files (created automatically)
├── venv/                       # Python virtual environment (if created)
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore file
```

## 📊 Output

The scraper generates a CSV file with the following columns:

| Column                       | Description                                 |
| ---------------------------- | ------------------------------------------- |
| Name                         | Conference/seminar name                     |
| City_Country                 | Location (city and country)                 |
| Conference_Dates             | Event dates (YYYY-MM-DD)                    |
| Abstract_Submission_Deadline | Deadline for submissions (YYYY-MM-DD)       |
| Key_Topic_Description        | Main topics covered                         |
| Organizer                    | Hosting organization                        |
| Link                         | Event website URL                           |

## ⚙️ Configuration

The scraper's behavior can be configured by editing the `config.py` file:

- **`USER_AGENTS`**: A list of User-Agent strings to rotate through for requests.
- **`RETRY_TOTAL`**, **`RETRY_BACKOFF_FACTOR`**, etc.: Parameters for the request retry strategy.
- **`TARGET_YEARS`**: A list of years to filter for when parsing dates (e.g., `[2025, 2026]`).
- **`OUTPUT_DIR`**: The directory where output CSV files will be saved.
- **`COLUMNS`**: The list of column names for the output CSV.
- **`BASE_URLS`**: (Legacy) A placeholder for base URLs. It is recommended to use the `--urls` command-line argument instead.

## 🧪 Testing

The project includes a test suite to ensure reliability. To run the tests, execute the following command from the project root directory:

```bash
python3 -m unittest discover tests
```

## 🚨 Current Challenges

### Advanced Bot Detection on `allconferencealert.net`

We are currently facing challenges scraping `https://allconferencealert.net/`. The website appears to use advanced bot detection mechanisms that are preventing our `selenium`-based scraper from accessing the conference data.

**What we've tried:**

- Using `selenium` with a headless Chrome browser to render dynamic JavaScript content.
- Implementing explicit waits to ensure the page has time to load.
- Disabling the `navigator.webdriver` flag and other common `selenium` automation flags to appear more like a normal browser.

Despite these efforts, the scraper is still being blocked, and the conference listings are not being loaded.

**How you can help:**

We are looking for contributors to help us bypass this bot detection. Some potential avenues to explore include:

- **More advanced anti-detection libraries:** Investigating libraries like `undetected-chromedriver` which are specifically designed to be more stealthy.
- **Proxy services:** Using a rotating proxy service to avoid IP-based blocking.
- **Network analysis:** Manually inspecting the website's network traffic in a real browser's developer tools to see if there's a direct API call we can use to fetch the data, which would be more reliable than scraping the HTML.
- **Alternative scraping libraries:** Exploring other scraping libraries or frameworks that might be better suited for this kind of challenge.

If you have experience with advanced web scraping and bot detection, we would greatly appreciate your contributions!

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines for Python code.
- Add docstrings to all functions and classes.
- Update tests if you add new functionality.
- Update the README.md if you change functionality.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

**Alex Prima**
- GitHub: [@axp-knickei](https://github.com/axp-knickei)
- Email: alexprima@gmail.com

## 🙏 Acknowledgments

- Thanks to the Beautiful Soup and Selenium communities for their excellent libraries.
- Inspired by the need for automated conference tracking in biological sciences.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always:
- Check the website's `robots.txt` before scraping.
- Respect the website's terms of service.
- Implement appropriate delays between requests.
- Consider using official APIs when available.

## 📝 Changelog

### Version 1.2.0 (Selenium Integration and Debugging)
- **Added Selenium**: Integrated `selenium` to handle dynamically loaded content.
- **Bot Detection Attempts**: Added measures to prevent `selenium` detection.
- **Documented Challenges**: Added a "Current Challenges" section to the README to document issues with scraping `allconferencealert.net`.

### Version 1.1.0 (Refactor and Test)
- **Refactored to Object-Oriented Structure**: Moved core logic into a `SeminarScraper` class in `seminar_scraper.py`.
- **Added Configuration File**: Centralized settings into `config.py`.
- **Implemented Command-Line Interface**: Added `argparse` in `main.py` to accept URLs and an output file.
- **Added Test Suite**: Created unit and integration tests using `unittest` to ensure scraper reliability.
- **Bug Fixes**: Corrected date parsing logic and various other bugs.

### Version 1.0.6
- Enhanced date parsing with 2025-2026 filtering
- Improved retry mechanism
- Added randomized headers for better bot detection avoidance
- Implemented comprehensive logging

---

**Note**: This scraper is designed for academic and research purposes. Please use responsibly and in accordance with website terms of service.
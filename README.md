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
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## ✨ Features

- **Automated Data Collection**: Scrapes conference and seminar information from biological science websites
- **Robust Error Handling**: Implements retry strategies and logging for reliable data collection
- **Smart Date Parsing**: Enhanced date parsing with filtering for 2025-2026 events
- **Anti-Bot Detection**: Randomized headers and delays to avoid being blocked
- **Structured Output**: Exports data to CSV format with organized columns
- **Session Management**: Built-in retry mechanism for handling failed requests

## 🔧 Prerequisites

Before running this scraper, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)

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

Run the scraper using the following command:

```bash
python 251014-Social1-v1.0.6.py
```

The scraper will:
1. Connect to target websites
2. Extract seminar and conference information
3. Parse dates and filter for 2025-2026 events
4. Export results to a CSV file

### Example Output

The scraper collects the following information:
- **Name**: Conference/seminar title
- **City_Country**: Location of the event
- **Conference_Dates**: Event dates
- **Abstract_Submission_Deadline**: Deadline for abstract submissions
- **Key_Topic_Description**: Main topics and themes
- **Organizer**: Organization or institution hosting the event
- **Link**: URL to the event page

## 📁 Project Structure

```
biological-seminar-scraper/
├── 251014-Social1-v1.0.6.py    # Main scraper script
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── .gitignore                    # Git ignore file
└── output/                       # Directory for output files (created automatically)
```

## 📊 Output

The scraper generates a CSV file with the following columns:

| Column | Description |
|--------|-------------|
| Name | Conference/seminar name |
| City_Country | Location (city and country) |
| Conference_Dates | Event dates |
| Abstract_Submission_Deadline | Deadline for submissions |
| Key_Topic_Description | Main topics covered |
| Organizer | Hosting organization |
| Link | Event website URL |

## ⚙️ Configuration

### Customizing Headers

The scraper uses randomized User-Agent strings to avoid detection. You can add more user agents in the `get_headers()` function:

```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    # Add your custom user agents here
]
```

### Adjusting Retry Strategy

Modify the retry parameters in `create_session_with_retries()`:

```python
retry_strategy = Retry(
    total=3,                    # Number of retries
    backoff_factor=1,           # Delay between retries
    status_forcelist=[429, 500, 502, 503, 504]  # HTTP status codes to retry
)
```

### Date Range Filtering

The scraper currently filters for 2025-2026 events. To change this, modify the `target_years` list in `parse_date_improved()`:

```python
target_years = [2025, 2026]  # Add or remove years as needed
```

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

- Follow PEP 8 style guidelines for Python code
- Add docstrings to all functions
- Update tests if you add new functionality
- Update the README.md if you change functionality

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Contact

**Alex Prima**
- GitHub: [@axp-knickei](https://github.com/axp-knickei)
- Email: alexprima@gmail.com

## 🙏 Acknowledgments

- Thanks to the Beautiful Soup community for the excellent HTML parsing library
- Inspired by the need for automated conference tracking in biological sciences

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Always:
- Check the website's `robots.txt` before scraping
- Respect the website's terms of service
- Implement appropriate delays between requests
- Consider using official APIs when available

## 📝 Changelog

### Version 1.0.6
- Enhanced date parsing with 2025-2026 filtering
- Improved retry mechanism
- Added randomized headers for better bot detection avoidance
- Implemented comprehensive logging

---

**Note**: This scraper is designed for academic and research purposes. Please use responsibly and in accordance with website terms of service.

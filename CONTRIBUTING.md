# Contributing to Biological Seminar Web Scraper

First off, thank you for considering contributing to this project! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to alexprima@gmail.com.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if relevant**
- **Mention your Python version and operating system**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed enhancement**
- **Explain why this enhancement would be useful**
- **List any similar features in other projects**

### Pull Requests

1. Fork the repository and create your branch from `main`
2. If you've added code, add tests
3. Ensure your code follows PEP 8 style guidelines
4. Update the README.md with details of changes if needed
5. Issue the pull request!

## Development Setup

1. Fork and clone the repository
```bash
git clone https://github.com/yourusername/biological-seminar-scraper.git
cd biological-seminar-scraper
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create a new branch
```bash
git checkout -b feature/your-feature-name
```

## Style Guidelines

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Use type hints where appropriate

Example:
```python
def parse_conference_date(date_str: str) -> str:
    """
    Parse conference date string and return formatted date.

    Args:
        date_str: Raw date string from website

    Returns:
        Formatted date string or 'Not known' if parsing fails
    """
    # Implementation here
    pass
```

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests after the first line

Example:
```
Add date range filtering for conferences

- Implemented filter for 2025-2026 events
- Added configuration option for custom date ranges
- Fixes #123
```

## Testing

Before submitting a pull request:

1. Test your changes manually
2. Ensure no existing functionality is broken
3. Add new tests for new features
4. Run the scraper with different configurations

## Project Structure

```
biological-seminar-scraper/
├── 251014-Social1-v1.0.6.py    # Main scraper
├── requirements.txt              # Dependencies
├── README.md                     # Documentation
├── CONTRIBUTING.md               # This file
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore rules
```

## Questions?

Feel free to open an issue with the tag "question" or contact the maintainer directly at alexprima@gmail.com.

## Recognition

Contributors will be recognized in the project README. Thank you for your contributions!

import unittest
from seminar_scraper import SeminarScraper
import config

class TestDateParsing(unittest.TestCase):
    def setUp(self):
        self.scraper = SeminarScraper()
        # Ensure target years include 2025 and 2026 for testing
        config.TARGET_YEARS = [2025, 2026]

    def test_valid_date_formats(self):
        self.assertEqual(self.scraper.parse_date_improved("15 Oct 2025"), "2025-10-15")
        self.assertEqual(self.scraper.parse_date_improved("October 15, 2025"), "2025-10-15")
        self.assertEqual(self.scraper.parse_date_improved("2025-10-15"), "2025-10-15")
        self.assertEqual(self.scraper.parse_date_improved("15/10/2025"), "2025-10-15")
        self.assertEqual(self.scraper.parse_date_improved("10/15/2025"), "2025-10-15")

    def test_year_inference(self):
        self.assertEqual(self.scraper.parse_date_improved("Oct 15, 2025"), "2025-10-15")
        self.assertEqual(self.scraper.parse_date_improved("15 Oct, 2025"), "2025-10-15")

    def test_invalid_and_edge_cases(self):
        self.assertEqual(self.scraper.parse_date_improved("Not known"), "Not known")
        self.assertEqual(self.scraper.parse_date_improved(None), "Not known")
        self.assertEqual(self.scraper.parse_date_improved(""), "Not known")
        self.assertEqual(self.scraper.parse_date_improved("Invalid Date"), "Not known")
        self.assertEqual(self.scraper.parse_date_improved("32 Oct 2025"), "Not known")

    def test_year_filtering(self):
        self.assertEqual(self.scraper.parse_date_improved("15 Oct 2024"), "Not known")
        self.assertEqual(self.scraper.parse_date_improved("15 Oct 2027"), "Not known")
        self.assertEqual(self.scraper.parse_date_improved("15 Oct 2026"), "2026-10-15")

if __name__ == '__main__':
    unittest.main()

import unittest
import os
from seminar_scraper import SeminarScraper
from urllib.parse import urljoin

class TestSeminarScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = SeminarScraper()
        self.test_html_path = os.path.join('test_data', 'dummy_seminars.html')
        with open(self.test_html_path, 'r') as f:
            self.html_content = f.read()
        self.base_url = "http://example.com"

    def test_parse_seminar_data(self):
        seminars = self.scraper.parse_seminar_data(self.html_content, self.base_url)
        self.assertEqual(len(seminars), 3)

        # Test first seminar
        self.assertEqual(seminars[0]['Name'], 'Advanced Neuroscience Conference')
        self.assertEqual(seminars[0]['City_Country'], 'Berlin, Germany')
        self.assertEqual(seminars[0]['Conference_Dates'], 'Not known') # The date format is not in the list of valid formats
        self.assertEqual(seminars[0]['Abstract_Submission_Deadline'], '2025-08-15')
        self.assertEqual(seminars[0]['Key_Topic_Description'], 'A conference on the latest in neural engineering.')
        self.assertEqual(seminars[0]['Organizer'], 'Future Science Institute')
        self.assertEqual(seminars[0]['Link'], 'http://example.com/events/neuro-2025')

        # Test second seminar
        self.assertEqual(seminars[1]['Name'], 'Genomics & Bioinformatics Symposium')
        self.assertEqual(seminars[1]['City_Country'], 'San Francisco, USA')
        self.assertEqual(seminars[1]['Conference_Dates'], 'Not known') # The date format is not in the list of valid formats
        self.assertEqual(seminars[1]['Abstract_Submission_Deadline'], 'Not known')
        self.assertEqual(seminars[1]['Organizer'], 'Genome Research Foundation')
        self.assertEqual(seminars[1]['Link'], 'http://example.com/events/genomics-symposium-2026')

        # Test third seminar (with missing data)
        self.assertEqual(seminars[2]['Name'], 'Invalid Entry - Missing Link')
        self.assertEqual(seminars[2]['Link'], 'Not found')
        self.assertEqual(seminars[2]['Organizer'], 'Not found')


if __name__ == '__main__':
    unittest.main()

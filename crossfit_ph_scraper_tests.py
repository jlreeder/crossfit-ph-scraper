import unittest
from crossfit_ph_scraper import *

class Test(unittest.TestCase):

    def test_get_content_for_date(self):
        self.assertTrue(get_content("2016/09/06/wod-wednesday-sept-7/"))

    def test_format_content(self):
        page = get_content("2016/09/06/wod-wednesday-sept-7/")
        self.assertTrue(format_content(page))

    def test_date_functioning(self):
        date_delay = 0
        self.assertTrue(format_date(date_delay))

    def test_date_correct(self):
        date_delay = 0
        self.assertEqual(format_date(date_delay),
                          "2016/09/07/wod-thursday-sept-8/")

if __name__ == "__main__":
    unittest.main()

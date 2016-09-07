import unittest
from crossfit_ph_scraper import *

class Test(unittest.TestCase):

    def test_get_content_for_date(self):
        self.assertTrue(get_content("2016/09/06/wod-wednesday-sept-7/"))

    def test_format_content(self):
        page = get_content("2016/09/06/wod-wednesday-sept-7/")
        self.assertTrue(format_content(page))

if __name__ == "__main__":
    unittest.main()

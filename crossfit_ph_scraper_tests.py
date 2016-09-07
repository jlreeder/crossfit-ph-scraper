import unittest
from crossfit_ph_scraper import *

class Test(unittest.TestCase):

    def test_retrieve_blog(self):
        self.assertTrue(get_content())

if __name__ == '__main__':
    unittest.main()

import urllib.request
from bs4 import BeautifulSoup

def format_date():
    """
    TODO: Format date for wod blog
    """
    pass

def get_content(date):
    """
    Get the content of the WOD blog for a given date
    """

    base_url = "http://crossfitph.com/"
    crossfit_ph_url = base_url + date

    req = urllib.request.Request(crossfit_ph_url,
                                 headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    page = response.read()
    soup = BeautifulSoup(page, "html.parser")

    return soup

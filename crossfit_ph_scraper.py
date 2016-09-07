import urllib.request
from bs4 import BeautifulSoup

def get_content():
    """
    Get the content of the WOD blog
    """

    crossfit_ph_url = "http://crossfitph.com/wod-blog/"
    req = urllib.request.Request(crossfit_ph_url,
                                 headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    page = response.read()
    soup = BeautifulSoup(page, "html.parser")

    return soup

# get_content(crossfit_ph_url)

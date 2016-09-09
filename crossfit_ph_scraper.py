import urllib.request
from datetime import date, timedelta
from bs4 import BeautifulSoup

def format_date(delay=0):
    """
    Format date for wod blog

    Delay is how many days ago, default 0 (today)
    """

    day = date.today() - timedelta(delay)
    weekday = day.strftime("%A").lower()
    month = day.strftime("%B")[:4].lower()

    # NOTE: Post date is usually one before WOD date
    post_day = day - timedelta(1)
    post_date = post_day.strftime("%Y/%m/%d")

    post_title = "/wod-%s-%s-%s/" % (weekday, month, day.day)

    return post_date + post_title

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

    return page

def format_content(page):
    """
    Parse and format the content of the html page
    """

    # Isolate WOD Text
    soup = BeautifulSoup(page, "html.parser")
    text = soup.get_text()

    pre, relevant = text.split("FAQ")
    relevant, post = relevant.split("WOD LOGGING")

    # Clean up
    lines = relevant.splitlines()
    lines = [line for line in lines if line]
    lines = lines[4:]

    # Format
    HEADERS = ["Strength A:", "Strength B:", "Strength:", "WOD:"]
    wod_text = ""
    for line in lines:
        prefix = "  - "
        if line in HEADERS:
            prefix = "- "
        line = prefix + line
        wod_text += line + "\n"

    return wod_text

if __name__ == "__main__":
    date = format_date()
    content = get_content(date)
    text = format_content(content)
    print(text)

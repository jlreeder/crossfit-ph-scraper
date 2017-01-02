#!/usr/bin/env python
"""
Crossfit Potrero Hill Scraper

Find the latest workout at Crossfit Potrero Hill
"""

import urllib.request
import argparse
import os
from datetime import date, timedelta
from bs4 import BeautifulSoup


def parse_date(delay=0):
    """
    Parse the input given, return the date requested.

    Delay is how many days ago, default 0 (today)
    """

    return date.today() - timedelta(delay)


def format_date(day):
    """
    Format date for wod blog url
    """

    weekday = day.strftime("%A").lower()

    # NOTE: Month abbreviations are inconsistent. October and November are 3
    # chars (oct, nov) while September is 4 chars (sept). Unsure of others but
    # will default to 3 chars
    abbreviation_len = 3
    if day.month == 9:
        abbreviation_len = 4
    month = day.strftime("%B")[:abbreviation_len].lower()

    # NOTE: Post date is usually one before WOD date
    post_day = day - timedelta(1)
    post_date = post_day.strftime("%Y/%m/%d")

    post_title = "/wod-%s-%s-%s/" % (weekday, month, day.day)

    return post_date + post_title


def format_url(raw_date):
    """
    From a raw date, return the URL used by the PH Crosfit website.
    """

    base_url = "http://crossfitph.com/"

    return base_url + raw_date


def get_content(url):
    """
    Get the content of the WOD blog for a given url
    """

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    page = response.read()

    return page


def format_title(date, width=10):
    """
    Prepare the title text for output using date and terminal width
    """

    heading = "POTRERO HILL CROSSFIT".center(width, " ")
    subheading = "WOD: {}".format(str(date)).center(width, " ")

    return "\n{}\n{}".format(heading, subheading)


def format_content(page):
    """
    Parse and format the content of the html page
    """

    # Isolate WOD Text
    soup = BeautifulSoup(page, "html.parser")
    text = soup.get_text()

    beginning_split = text.split("FAQ")
    relevant = beginning_split[1]
    if "Athlete of the" in relevant:
        middle_split = relevant.split("Athlete of the")
    else:
        middle_split = relevant.split("WOD LOGGING")
    relevant = middle_split[0]

    # Clean up
    lines = relevant.splitlines()
    lines = [line.strip() for line in lines if line]
    lines = lines[4:-1]

    # Add contents as bullets
    wod_text = ""
    for line in lines:
        prefix = "  - "
        # Do not add indent for headers
        if line.endswith(":") and not line.startswith("Lv"):
            prefix = "- "
        line = prefix + line
        wod_text += line + "\n"

    return wod_text


def main():
    """
    Implement helper functions
    """

    # Configure arguments
    parser = argparse.ArgumentParser(description="Get Workout at Crossfit-PH")
    parser.add_argument(
        "delay",
        metavar="D",
        type=int,
        nargs="?",
        default="0",
        help="How many days ago was the workout (today would be 0)")
    parser.add_argument(
        '--url',
        action="store",
        dest="custom_url",
        help="Custom url (if default was unsuccessful)")
    args = parser.parse_args()
    delay = args.delay
    custom_url = args.custom_url

    # Get terminal width
    width = int(os.popen('stty size', 'r').read().split()[1])
    divider = "~" * width

    # Run helper functions with configured args
    date_requested = parse_date(delay)
    formatted_date = format_date(date_requested)
    title = format_title(date_requested, width)
    url_to_query = format_url(formatted_date)
    if custom_url:
        url_to_query = custom_url
    print("{}{}\nURL: {}\n".format(divider, title, url_to_query))
    try:
        content = get_content(url_to_query)
        text = format_content(content)
        print(text)
        # Copy only the wod text to clipboard
        os.system("echo '%s' | pbcopy" % text)
    except urllib.error.HTTPError:
        print("Sorry, couldn't find any data at this url.")
    except urllib.error.URLError:
        print("ERROR: No internet connection")


if __name__ == "__main__":
    main()

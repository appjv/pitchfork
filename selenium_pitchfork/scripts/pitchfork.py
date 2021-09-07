import time
import sys
import datetime as dt
import pandas as pd
import logging
import os
import errno
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from config import from_config
from datetime import datetime

wait = 3
urls = [i for i in range(1, 100)]
target_urls = [f'https://pitchfork.com/reviews/albums/?page={url}' for url in urls]
with open("/Users/japp/PycharmProjects/dev/pitchfork/selenium_pitchfork/pitchfork/pitchfork_urls.txt", 'w') as f:
    for line in target_urls:
        f.write(line + '\n')

def mkdir_p(path):
    # https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def initiate_browser(wait, url):
    # Set options for our browser, in this case run a headless browser
    opts = Options()
    # opts.add_argument('-headless')
    # assert opts.headless  # Operating in headless mode
    driver = Firefox(options=opts)
    driver.implicitly_wait(wait)
    driver.get(url)
    return driver


driver = initiate_browser(wait, target_url)

SCROLL_PAUSE_TIME = 20

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

hrefs = driver.find_elements_by_xpath("//div[@class='review']/a[@href]")

# hrefs = []
# artists = []
# albums = []
#
#
# def parse():
#     for artist, album, href in map(zip(artists, albums, hrefs)):
#         yield {
#             'artist': artist,
#             'href': href,
#             'album': album
#     }

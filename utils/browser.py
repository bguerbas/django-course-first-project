import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def make_chrome_browser(*options):
    chrome_options = Options()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if int(os.environ.get('SELENIUM_HEADLESS')) == 1:
        chrome_options.add_argument('--headless')

    chrome_service = ChromeService(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

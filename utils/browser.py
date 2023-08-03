from dataclasses import dataclass
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


@dataclass()
class Driver:
    time: int = 5
    options = Options()
    if os.environ.get('SELENIUM_HEADLESS') == 1:
        options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
        )
    wait = WebDriverWait(browser, time)

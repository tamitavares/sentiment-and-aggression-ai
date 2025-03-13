from imports import *
from config import *

driver = webdriver.Firefox()

def open_page(link):
    driver.get(link)
    time.sleep(10)
from bs4 import BeautifulSoup as bs
import requests
import pprint
import re
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import math
import csv


url = 'http://proxy.library.georgetown.edu/login?url=https://search.proquest.com/search/1396058?accountid=11091'

driver = webdriver.Chrome()
driver.get(url)

driver.find_element_by_id('mainContentRight').click()
#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Opti

binary = r'/usr/lib/Google_Chrome.app/Contents/MacOS/Google_Chrome'
options = Options()
options.set_headless(headless=True)
options.binary = binary
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
driver.get("http://www.imdb.com/title/tt3783958/")
elem = driver.find_element_by_css_selector('strong span')
print("Rating: {}".format(elem.text))
elem = driver.find_elements_by_css_selector('.subtext .itemprop')
for e in elem:
  print("- {}".format(e.text))
driver.quit()
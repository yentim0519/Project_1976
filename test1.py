#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

binary = r'/usr/lib/Google_Chrome.app/Contents/MacOS/Google_Chrome'
options = Options()
options.set_headless(headless=True)
options.binary = binary
driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
print ("Headless Chrome Initialized")
# driver.get("http://www.imdb.com/title/tt3783958/")
# elem = driver.find_element_by_css_selector('strong span')
# print("Rating: {}".format(elem.text))
# elem = driver.find_elements_by_css_selector('.subtext .itemprop')
# for e in elem:
#   print("- {}".format(e.text))
driver.quit()
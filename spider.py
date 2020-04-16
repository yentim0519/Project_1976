# -*- coding: UTF-8 -*-

# 匯入libraries
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pymysql
import time
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import importlib
from selenium.common.exceptions import WebDriverException

#設定編碼
# importlib.reload(sys)
# #獲得系統編碼格式
# type = sys.getfilesystemencoding()
# print(type)


def connectChrome():
    binary = r'/usr/lib/Google_Chrome.app/Contents/MacOS/Google_Chrome'
    options =  Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('window-size=1920x3000') # 指定浏览器分辨率
    options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
    # options.add_argument("--remote-debugging-port=9222")
    # options.add_argument('--ignore-certificate-errors')
    options.add_argument('blink-settings=imagesEnabled=false')# 不加载图片, 提升速度
    options.add_argument('--disable-gpu')
    options.binary = binary
    driver = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
    return driver
print(1)
# 連接資料庫
conn = pymysql.connect(host = 'sogoyen.crc98fdcbodi.us-east-2.rds.amazonaws.com', port = 3306, user = 'admin',
                       passwd = 'helloyen', db =  'mydb')

cursor = conn.cursor()

# create table
# cursor.execute("CREATE TABLE perfume_data(id INT NOT NULL AUTO_INCREMENT,product_brand VARCHAR(100),product_name VARCHAR(100),fragrance_notes VARCHAR(50),top_notes VARCHAR(50),middle_notes VARCHAR(50),base_notes VARCHAR(50),product_url VARCHAR(100),PRIMARY KEY(ID))")
# conn.commit()


# 將brand names存成list
resp = requests.get('https://www.1976.com.tw/brand')
soup = BeautifulSoup(resp.text, 'html.parser')
brand_names = soup.find("div", {"class": "brandall"}).find_all('a')
brand_names_list = []
print(6)

for brand_name in brand_names:      # 要用for迴圈才能將resultset object的資料取出
    brand_name = brand_name.string.strip() # 將string的空格和'\n'拿掉
    print(brand_name)
    brand_names_list.append(brand_name)

# 利用迴圈將5筆品牌A開頭的資料抓下來
target_url = 'https://www.1976.com.tw/brand'



try:
    driver = connectChrome()
except WebDriverException:
    driver.quit()

driver.get(target_url)
print(7)

# 進入特定品牌
for i in range(len(brand_names_list)):
    # print('i = '+ str(i))

    element0 = driver.find_element_by_link_text(brand_names_list[i]) # 上面的目錄擋住了click的地方，用ENTER即可解決
    driver.execute_script("arguments[0].click();", element0)

    # 將此brand的product_name存入list
    resp1 = requests.get(driver.current_url)
    print(resp1.encoding)
    soup1 = BeautifulSoup(resp1.text, 'html.parser')
    print(soup1.original_encoding)
    
    #soup1.encoding = 'utf-8'
    product_names = soup1.find_all("div", {"class": "item-name"})
    # product_names = str(product_names,'utf-8')
    # print(product_names)
    product_names_list = []

    # for sql
    product_brand = brand_names_list[i]
    print(8)
    for product_name in product_names:      # 要用for迴圈才能將resultset object的資料取出   
        a = product_name.find('a').string.strip()
        # print(a)
        product_names_list.append(a)

    print(2)
    # 進入特定商品
    for j in range(len(product_names_list)): 

        product_name = product_names_list[j]

        driver.implicitly_wait(10)
        element = driver.find_element_by_link_text(product_names_list[j])
        driver.execute_script("arguments[0].click();", element) # 用這個作法即可解決偶爾有element not interactable的問題
#         print(product_names_list[j])

        print(3)
        # 將前中後香的資訊拿出來
        product_url = driver.current_url
        resp2 = requests.get(product_url)
        resp2.encoding = 'utf-8'
        soup2 = BeautifulSoup(resp2.text, 'html.parser')
        perfume_notes = soup2.find("div", {"class": "product-perfume"})
#         print(perfume_notes)

        fragrance_notes = perfume_notes.contents[0].strip().strip('香 調： ')
        top_notes = perfume_notes.contents[2].strip().strip('前 味： ')
        middle_notes = perfume_notes.contents[4].strip().strip('中 味： ')
        base_notes = perfume_notes.contents[6].strip().strip('後 味： ')
        print(fragrance_notes)

        # 將中文編碼，否則進到db會是亂碼
        # product_name
        # fragrance_notes
        # top_notes
        # middle_notes
        # base_notes

        # 將爬下的資料輸入datbase
        cursor.execute("INSERT INTO perfume_data1(product_brand, product_name, fragrance_notes, top_notes, middle_notes, base_notes, product_url)VALUES(%s, %s, %s, %s, %s, %s, %s);", 
                          (product_brand, product_name, fragrance_notes, top_notes, middle_notes, base_notes, product_url))
        print(1)
        conn.commit()
        driver.back()
    
    driver.back()
    del resp1, soup1, product_names, product_names_list # 將前一個brand的資料都清除


driver.quit()
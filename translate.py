import os.path
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
from time import sleep
import pickle
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


if __name__ == '__main__':
    filename='journal-list.txt'
    filename='keywords-list.txt'
    
    with open(filename, 'r') as file:
        top_journals = file.readlines()

    chrome_driver_path = 'chromedriver.exe'

    # Configure proxy settings. If you need...
    proxy_address = 'socks5://127.0.0.1:1080'
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": proxy_address,
        "ftpProxy": proxy_address,
        "sslProxy": proxy_address,
        "proxyType": "MANUAL",
    }

    chrome_options = Options()
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    # chrome_options.add_argument('--headless')  # Run Chrome in headless mode

    # Launch WebDriver with proxy settings
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
    actions = ActionChains(driver)


    output='hine-en'
    if not os.path.exists(output):
        os.mkdir(output)
    # 获取已下载文献数量
    t = os.listdir(output)
    if os.path.exists(output+"/fail2translate.txt"):
        t.remove("fail2translate.txt")
    thesis_seq = len(t) + 1
        
        

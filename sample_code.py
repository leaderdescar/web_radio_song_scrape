from selenium import webdriver
import os
os.environ["LANG"] = "en_US.UTF-8"




options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
browser = webdriver.Chrome(chrome_options=options) 
browser.get('https://en.wikipedia.org/wiki/Web_navigation')
browser.implicitly_wait(100)
assert 'Web' in browser.title


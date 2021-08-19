import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



#open browser
driver = webdriver.Opera()
#open website with infinity scroll
driver.get('Enter web Address')
# how many time yuo want to scroll down. writer range_value
for _ in range(11):
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(3)
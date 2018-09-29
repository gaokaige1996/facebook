
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import re
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from time import sleep

fileid = '102621172007'
postid = '10154874257057008'

chrome_options = webdriver.ChromeOptions()


prefs = {"profile.managed_default_content_settings.images": 2 ,"permissions.default.stylesheet" :2
         ,"javascript.enabled" :False ,"profile.default_content_setting_values.notifications" :1}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
# driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=chrome_options)
driver.maximize_window()
driver.get('https://www.facebook.com/' + fileid + '/posts/' + postid)

# driver.get('https://www.facebook.com')
# if has other windows

driver.find_element_by_xpath("//*[@id='expanding_cta_close_button']").click()
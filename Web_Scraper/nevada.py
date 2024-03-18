# IMPORT NECESSARY LIBRARIES
import time
import pyautogui
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from datetime import datetime, date, timedelta
import config

# SETUP (access website, filter for information)
path = "C:\Downloads\chromedriver.exe"
browser = webdriver.Chrome(path)

# access public notice website
browser.get('https://www.nevadapublicnotice.com/')
browser.implicitly_wait(100)
browser.maximize_window()
   
time.sleep(3)

# access date range drop down menu
WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_divDateRange"))).click()

# access custom date range
WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_rbRange"))).click()

# set start date 
WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_txtDateFrom"))).click()
pyautogui.keyDown("ctrl") 
pyautogui.press("a")
pyautogui.press("ctrl")
pyautogui.press("backspace")
pyautogui.write("1/01/2023") # define current date later

# set end date 
WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_txtDateTo"))).click()
pyautogui.keyDown("ctrl") 
pyautogui.press("a")
pyautogui.press("ctrl")
pyautogui.write("3/23/2023")


# quick search for foreclosures --> triggers search
WebDriverWait(browser, 50).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_ddlPopularSearches"))).click()
pyautogui.write("FORECLOSURES")
pyautogui.press("enter")

# filters max number of results per page
WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_ddlPerPage"))).click()
browser.implicitly_wait(50)
pyautogui.write("50")
browser.implicitly_wait(50)
pyautogui.press("enter")

# allow results to load
time.sleep(3)

# To Complete User Captcha then allow for automation 

# access record
WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl03_btnView2"))).click()
# wait until user has completed CAPTCHA and agreed to notice
WebDriverWait(browser, 100).until(EC.url_changes)
# test to grab back button
backBtn = browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBody")
browser.implicitly_wait(50)
backBtn.click()

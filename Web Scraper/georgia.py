# IMPORT NECESSARY LIBRARIES
import time
import pyautogui
import pandas as pd
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
# path = "C:\Downloads\chromedriver.exe"
# browser = webdriver.Chrome(path)

# access public notice website
# browser.get('https://www.georgiapublicnotice.com/')
# browser.implicitly_wait(100)
# browser.maximize_window()

# initialSetupParameters scrapes either COUNTY or PUBLICATION
def setSearch(browser):

    # quick search for foreclosures --> triggers search
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_pnlQuickSearch"))).click()
    pyautogui.write("FORECLOSURES")


# setupParameter sets start/end dates + filters quick search to foreclosures
def setDate(browser, currentDate): 
    
    # print("in setup "+currentDate.strftime("%m/%d/%Y"))
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
    pyautogui.write(currentDate) # define current date later

    # set end date 
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_txtDateTo"))).click()
    pyautogui.keyDown("ctrl") 
    pyautogui.press("a")
    pyautogui.press("ctrl")
    pyautogui.write(currentDate)

    
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.NAME,"ctl00$ContentPlaceHolder1$as1$btnGo"))).click()
    WebDriverWait(browser, 100).until(EC.url_changes)
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_divDateRange"))).click()

# scrape facilitates all web scraping actions
def scrape(browser, current_date):

    # create initial df to hold information
    dfall = pd.DataFrame(columns = ["noticeDate","webURL","pubName","location","Content","Hash"])

    # increase results per page to 50
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl01_ddlPerPage"))).click()
    pyautogui.write("50")
    pyautogui.press("enter")

    time.sleep(3)

    # view one record 
    buttons = browser.find_element(By.ID,"ctl00_ContentPlaceHolder1_WSExtendedGridNP1_GridView1_ctl03_btnView2")
    buttons.click()

    WebDriverWait(browser, 100).until(EC.url_changes)



    # TEST: grab notice content
    backBtn = browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBody")
    backBtn.click()

def ga_publicnotice(siteurl, start_date, end_date):
    
    # access chrome driver
    browser = webdriver.Chrome(config.keys['driver-path'])
    
    # opening the web to scrape
    browser.get(siteurl)
    browser.maximize_window

    # set up dataframe
    # Date:Publication date, Source:Publication Website, Label:?, 
    dfall = pd.DataFrame(columns = ["Date","Source","Label","Area","Content","Hash"])

    
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    current_date = end_date 
    setSearch(browser)

    flag=0
    while True: #iterating the through the date
        current_date_str = str(current_date.strftime('%m/%d/%Y'))
        if current_date_str == start_date:
            break
        current_date = current_date - timedelta(days = 1)
        print(current_date_str)
        print ("current_date {}".format(current_date))
        current_date_str = str(current_date.strftime('%m/%d/%Y'))
        setDate(browser,current_date_str) 
        time.sleep(5)
        # initialSetupParameters(browser)


    browser.quit()
    print(dfall)

    return dfall



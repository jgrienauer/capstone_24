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
from selenium.webdriver.support.ui import Select
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

    # First, click the dropdown toggle to ensure the dropdown is visible
    dropdown_toggle = WebDriverWait(browser, 100).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_pnlQuickSearch")))
    dropdown_toggle.click()

    # Now that the dropdown is open, select the "FORECLOSURES" option from the <select> element
    select_element = WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_as1_ddlPopularSearches")))
    dropdown = Select(select_element)

    # Select the option by its visible text or value. Here we're selecting by visible text
    try:
        # Try to select "Foreclosures" first
        dropdown.select_by_visible_text("Foreclosures")
    except NoSuchElementException:
        try:
            # If "Foreclosures" is not found, try "Foreclosure"
            dropdown.select_by_visible_text("Foreclosure")
        except NoSuchElementException:
            # Handle the case where neither option is found
            print("Neither 'Foreclosures' nor 'Foreclosure' options were found.")
            # Consider adding more error handling here, e.g., logging or raising an error
    
    
    # quick search for foreclosures --> triggers search
 


# setupParameter sets start/end dates + filters quick search to foreclosures
def setDate(browser, currentDate): 
    
    # print("in setup "+currentDate.strftime("%m/%d/%Y"))
    # access date range drop down menu 
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_divDateRange"))).click()

    # access custom date range
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_rbRange"))).click()

    # set start date 
    ctrl_Character = config.keys['control_key']
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_txtDateFrom"))).click()
    pyautogui.keyDown(ctrl_Character)
    pyautogui.press("a")
    pyautogui.keyUp(ctrl_Character)
    pyautogui.press("backspace")
    pyautogui.write(currentDate) # define current date later

    # set end date 
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_txtDateTo"))).click()
    pyautogui.keyDown(ctrl_Character)
    pyautogui.press("a")
    pyautogui.keyUp(ctrl_Character)
    pyautogui.press("backspace")
    pyautogui.write(currentDate)

    # Finally, click the search button to apply the filter
    search_button = WebDriverWait(browser, 100).until(
        EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_as1_btnGo")))
    search_button.click()
    
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

    time.sleep(15)

    # TEST: grab notice content
    backBtn = browser.find_element(By.ID, "ctl00_ContentPlaceHolder1_PublicNoticeDetailsBody1_hlBackFromBody")
    backBtn.click()

def ga_publicnotice(siteurl, start_date, end_date):
    
    # access chrome driver
    browser = webdriver.Chrome()
    
    # opening the web to scrape
    browser.get(siteurl)
    browser.maximize_window

    # set up dataframe
    # Date:Publication date, Source:Publication Website, Label:?, 
    dfall = pd.DataFrame(columns = ["Date","Source","Label","Area","Content","Hash"])

    # Convert string dates to datetime objects
    start_dt = datetime.strptime(start_date, '%m/%d/%Y')
    end_dt = datetime.strptime(end_date, '%m/%d/%Y')

    # Iterate over each day in the date range
    current_date = start_dt
    while current_date <= end_dt:
        current_date_str = current_date.strftime('%m/%d/%Y')
        
        # Set the search parameters for the current date
        setSearch(browser)  # This sets the category; ensure it clicks the search button if needed
        setDate(browser, current_date_str)  # This sets the date and should trigger the search

        # Scrape the data for the current date
        daily_notices = scrape(browser, current_date_str)

        # Append the daily notices to the collective DataFrame
        dfall = pd.concat([dfall, daily_notices], ignore_index=True)

        # Move to the next day
        current_date += timedelta(days=1)
    #end_date = datetime.strptime(end_date, '%m/%d/%Y')
    #current_date = end_date 
    #setSearch(browser)

    #flag=0
    #while True: #iterating the through the date
        #current_date_str = str(current_date.strftime('%m/%d/%Y'))
        #if current_date_str == start_date:
            #break
        #current_date = current_date - timedelta(days = 1)
        #print(current_date_str)
        #print ("current_date {}".format(current_date))
        #current_date_str = str(current_date.strftime('%m/%d/%Y'))
        #setDate(browser,current_date_str) 
        #time.sleep(5)
        # initialSetupParameters(browser)


    browser.quit()
    print(dfall)

    return dfall



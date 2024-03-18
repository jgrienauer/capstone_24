from ssl import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import re
import pandas as pd
# import pyap - needed for address validation
from datetime import datetime, date, timedelta
import os
import hashlib
import config

# function "setSearch" filters NOTICE TYPE to FORECLOSURE SALE
def setSearch(browser):

    WebDriverWait(browser, timeout=100).until(EC.visibility_of_element_located((By.ID,"noticetype"))).click()
    pyautogui.write("Foreclosure Sale")
    pyautogui.press("enter")   

# function "setDate" sets start & end dates using CURRENT_DATE, which is defined in function "id_publicnotice"
def setDate(browser, current_date_str):

    #setting the starting date
    ctrl_Character = config.keys['control_key']
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"dateStart"))).click()
    pyautogui.keyDown(ctrl_Character)
    pyautogui.press("a")
    pyautogui.keyUp(ctrl_Character)
    pyautogui.press("backspace")
    pyautogui.write(current_date_str)

    #setting the end date
    WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.ID,"dateEnd"))).click()
    pyautogui.keyDown(ctrl_Character)
    pyautogui.press("a")
    pyautogui.keyUp(ctrl_Character)
    pyautogui.press("backspace")
    pyautogui.write(current_date_str)

    #search the files by the filter
    WebDriverWait(browser, 200)
    WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div/div[1]/div[1]/div/div[7]/span[3]/button"))).click()

    
    #waiting for them to load
    time.sleep(5)

def scrape(browser,current_date_str):
    try:
        # count total results for each search
        result_count_str = browser.find_element(By.ID,"result-count").get_attribute('textContent')
        result_count = int(re.sub("[^0-9]", "", result_count_str))
        print(result_count)
    except:
        df = pd.DataFrame(columns = ["Date","Publication","Location","Content","Hash"])
        data = {}
        data["Date"] = current_date_str
        data["Publication"] = "NaN"
        data["Location"] = "NaN"
        data["Content"] = "NaN"
        data["Hash"] = "NaN"
        df.loc[0] = data
        return df 
            

    # create dataframe
    df = pd.DataFrame(columns = ["Date","Publication","Location","Content","Hash"])

    for ix in range(1, result_count+1):
        try:
            date = current_date_str
            publication = browser.find_element(By.XPATH,f'/html/body/div/div[2]/div/div[2]/div[4]/div[2]/div[{ix}]/div/div[1]/div/div[1]/div/h3').get_attribute('textContent')
            location = browser.find_element(By.XPATH,f'/html/body/div/div[2]/div/div[2]/div[4]/div[2]/div[{ix}]/div/div[2]/div').get_attribute('textContent')
            content = browser.find_element(By.XPATH,f'/html/body/div/div[2]/div/div[2]/div[4]/div[2]/div[{ix}]/div/div[1]/div/div[3]').get_attribute('textContent')
            hash = hashlib.md5(content.encode("utf-8")).hexdigest()

            print("Record: "+date,publication, location, content)

            data = {}
            data["Date"] = current_date_str
            data["Publication"] = publication
            data["Location"] = location
            data["Content"] = content
            data["Hash"] = hash 
            df.loc[ix] = data
            df.append(data, ignore_index=True)
        except:
            print(ix)
            continue
    return df

# 
def idPublicNotice(siteurl, startDate, endDate):

    # browser = webdriver.Chrome("/Users/wesleysebastian/Downloads/chromedriver")
    browser = webdriver.Chrome()
    #opt=webdriver.ChromeOptions()
    #opt.add_argument("--start-maximized")
    browser.set_window_size(1920,1080)
    #opening the web to scrape
    browser.get(siteurl) 

    dfall = pd.DataFrame(columns = ["Date","Publication","Location","Content","Hash"])

    end_date = datetime.strptime(endDate, '%m/%d/%Y')
    current_date = end_date - timedelta(days=1)
    setSearch(browser)

    while True: #iterating the through the date
        current_date_str = str(current_date.strftime('%m/%d/%Y'))
        if current_date_str == startDate:
            break
        current_date = current_date - timedelta(days = 1)
        print(current_date_str)


        setDate(browser,current_date_str)
        df = scrape(browser,current_date_str)
        if df.iloc[0]["Content"]!="NaN":
          dfall = pd.concat([dfall,df],ignore_index=True)
       
        print ("current_date {}".format(current_date))

    browser.quit()
    print(dfall)

    return dfall
       


     
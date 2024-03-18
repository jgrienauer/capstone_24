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
import urllib.parse
from bs4 import BeautifulSoup



# path = "C:\Downloads\chromedriver.exe"
# driver = webdriver.Chrome(path)
 
def tnPublicNotice(siteurl):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(siteurl)
    browser.implicitly_wait(100)


    # search = driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_as1_txtSearch")
    # WebDriverWait(driver, timeout=100).until(EC.visibility_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_as1_txtSearch")))

    search = WebDriverWait(browser, timeout=15000).until(EC.visibility_of_element_located((By.ID,"ContentPane_ForeclosureGridView")))

    innerHTML = search.get_attribute("innerHTML")
    # print(innerHTML)

    soup = BeautifulSoup(innerHTML, 'html.parser')
    links = soup.find_all('a')
    # print(links)

    df = pd.DataFrame(columns = ["Date","Publication","Location","Content","Hash"])
    ix = 0

    for link in links:

        pos1 = str(link).find('(')    
        pos2 = str(link).find(')')
        txt = str(link)[pos1+1:pos2]
        txt = txt.replace("'","")
        
        args = txt.split(",")

        # print(link,pos1,pos2,type(link),txt,end="\n")
        # print(txt,end="\n")
        # print(txt,args[0],args[1])

        # https://tnledger.com/Search/Details/ViewNotice.aspx?id=Fsl56393&date=2/24/2023

        listingURL = "https://tnledger.com/Search/Details/ViewNotice.aspx?id=" + args[0] + "&date=" + args[1]
        # print(listingURL, end="\n")

        browser.execute_script("window.open('"+listingURL+"');")
        browser.implicitly_wait(500)
        browser.switch_to.window(browser.window_handles[1])

        search2 = WebDriverWait(browser, timeout=500).until(EC.visibility_of_element_located((By.ID,"record-details")))

        innerHTML2 = search2.get_attribute("innerHTML")
        soup2 = BeautifulSoup(innerHTML2,"html.parser")

        panelSummary = soup2.find('div',{'id':'pnlSummary'})
        child_soup = panelSummary.find_all("td")
        str_values = ''
        
        address = ""

        for element in child_soup:
            # print("element text "+ element.text)
            if "Borrower:" in element.text:
                next_td = element.find_next_sibling()
                print(next_td)
                value = next_td.text.replace("\n","")
                str_values += "| Borrower: " + value
                print("Borrower "+ value)

            elif "Attorney:" in element.text:
                next_td = element.find_next_sibling()
                print(next_td)
                value = next_td.text.replace("\n","")
                str_values += "| Attorney: " + value
                print("Attorney "+ value)
            
            elif "Address:" in element.text:
                next_td = element.find_next_sibling()
                print(next_td)
                value = next_td.text.replace("\n","")
                str_values += "| Address: " + value
                print("Address "+ value)

                # find parent of this td, then next sibling
                this_parent = element.find_parent()
                next_parent = this_parent.find_next_sibling()
                next_element = next_parent.findChildren("span")
                str_values += " " + next_element[0].text
                print("Listing: " + str_values)
            
            elif "Advertised Auction Date:" in element.text:
                next_td = element.find_next_sibling()
                print(next_td)
                value = next_td.text.replace("\n","")
                str_values += "| Auction Date: " + value
                print("Auction Date "+ value)
            
            elif "Substitute Trustee:" in element.text:
                next_td = element.find_next_sibling()
                print(next_td)
                value = next_td.text.replace("\n","")
                str_values += "| Substitute Trustee: " + value
                print("Substitute Trustee "+ value)

                

                # next_td = next_td.find_next_sibling()
                # print("Next line first td "+ next_td.text)

                # if next_td.text == "":
                #     next_td = next_td.find_next_sibling()
                #     value = next_td.text.replace("\n","")
                #     
                #     print("Address "+ value)

            
        
        elements = soup2.find_all("div")
        
        for elem in elements: 
            elem.decompose()
        
        listingContent = str_values + "|" + soup2.get_text().replace("\n","").replace("\t","")
        print(listingContent)
        
        # countyvalues = re.search("in\s([A-Za-z\s]+)\sCounty", listingContent)
        # print(type(countyvalues))
        
        # print(child_soup)
        # print(innerHTML2,end="\n")

        ix = ix+1
        data = {}
        # print(urllib.parse.unquote(args[1]))
        datetime_obj = datetime.strptime(urllib.parse.unquote(args[1]), "%m/%d/%Y")
        # print("DATETIME " + datetime_obj.strftime("%Y-%m-%d"))
        data["Date"] = datetime_obj.strftime("%Y-%m-%d")
        data["Publication"] = "TN Ledger"
        data["Location"] = "" #countyvalues[0]
        data["Content"] = listingContent
        data["Hash"] = hashlib.md5(innerHTML2.encode("utf-8")).hexdigest()
        df.loc[ix] = data
        df._append(data, ignore_index=True)
        
        browser.close()
        time.sleep(5)
        browser.switch_to.window(browser.window_handles[0])
        if ix > 4:
            break

    browser.quit()
    return df

# siteurl = "https://tnledger.com/Notices.aspx?noticesDate=02/24/2023"
# tnPublicNotice(siteurl)

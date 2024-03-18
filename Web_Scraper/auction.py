import pandas as pd
import pyap
from datetime import datetime, date, timedelta
import os
import pymssql
import config
import sys
#import california
import idaho2023
import georgia
import tnledger
#import nevada



#Function giving the user the choice of which state the want to go to
def user_select_state():
    print("Select a state to scrape:")
    print("1: Idaho")
    print("2: Georgia")
    print("3: Tennessee")
    print("4: Nevada")
    print("5: California")
    choice = input("Enter the number of your choice: ")
    return choice



# Main program that invokes individual sites and saves data to DB
def main():
    choice = user_select_state()

    dt_today = date.today()
    end_date = date.strftime(dt_today, "%m/%d/%Y")
    start_date = date.strftime(dt_today - timedelta(7), "%m/%d/%Y")

    if choice == '1':
        # Idaho scraping
        siteurl = "https://www.idahopublicnotices.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '2':
        # Georgia scraping
        siteurl = "https://www.georgiapublicnotice.com/"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '3':
        # For Tennessee, implement logic to find the appropriate Friday
        friday_date = "your_logic_to_find_friday"  # Placeholder for actual logic
        siteurl = f"https://tnledger.com/Notices.aspx?noticesDate={friday_date}"
        dfall = tnledger.tnPublicNotice(siteurl)
    elif choice == '4':
        # Nevada scraping, assuming you want to use version2 for Nevada as well
        siteurl = "https://www.nevadapublicnotice.com/"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '5':
        # California scraping
        siteurl = "https://www.capublicnotice.com/"  # Ensure this is the correct URL for California
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    else:
        print("Invalid choice. Please run the script again and select a valid option.")
        return

    # Assuming write_content_to_sql works with all states equally
    #write_content_to_sql(dfall, siteurl)

if __name__ == "__main__":
    main()



# Write site content to DB
def write_content_to_sql(dfall, siteurl):
  conn = pymssql.connect(server=config.keys['server'], user=config.keys['username'], password=config.keys['password'], database=config.keys['database']) 

   
  dfall = dfall.reset_index()
  print("dfall below")
  print(dfall)
  cur = conn.cursor()  
  for index,row in dfall.iterrows(): 
      sql= "select * from Listing where County='{}' and Hash_key='{}'".format(row['Location'], row['Hash'])
      cur.execute(sql)
      records =  cur.fetchall()
      if cur.rowcount==0:     
           content=row['Content'].replace("'","''")
           content=content.replace('\n',' ')
           sql= "INSERT INTO Listing (County, ListingDate, Content, Analyzed, Hash_key, SiteURL, RetrievalDate) VALUES ('{}', '{}', '{}', 0, '{}','{}', getdate())".format(row['Location'], row['Date'], content, row['Hash'],siteurl)
           print(sql) 
           cur.execute(sql) 
      
  conn.commit()
  cur.close() 
      
  conn.close()

# First eset up date range to scrape
# default is today back to 3 days.
# command line "auction n1" starts from today and goes back top n1 days
# command line "auction n1 n2" starts from today and goes back top n2 days

args = sys.argv
# default date range
end_day_delta = 0     # compared to today
start_day_delta = 7   # compared to today
# if len(args) > 2:
#     if args[2].isdigit():
#         end_day_delta = int(args[2])
# if len(args) > 1:
#     if args[1].isdigit():
#         start_day_delta = int(args[1])
    
# get the start and end dates to pass to functions
dt_today =  date.today()
if (end_day_delta >0):
    end_date = date.strftime(dt_today - timedelta(end_day_delta),"%m/%d/%Y")
else:
    end_date = date.strftime(dt_today,"%m/%d/%Y")

start_date = date.strftime(dt_today - timedelta(start_day_delta),"%m/%d/%Y")

# print ("start date {} End date {}".format(start_date, end_date))

# CA Public Notice 
# siteurl = "https://www.capublicnotice.com/"
# dfall= california.ca_publicnotice(siteurl,start_date,end_date ) 
# write_content_to_sql(dfall, siteurl)

# # ID Public Notice
#siteurl = "https://www.idahopublicnotices.com/"
#dfall= idaho2023.idPublicNotice(siteurl,start_date,end_date) 
#write_content_to_sql(dfall, siteurl)

# GA Public Notice
#siteurl = "https://www.georgiapublicnotice.com/"
#dfall= georgia.ga_publicnotice(siteurl,start_date,end_date ) 
# write_content_to_sql(dfall, siteurl)

#print ("url {}".format(siteurl))
#fntocall = "tnledger.tnPublicNotice('{}')".format(siteurl)
#print("fntocall ",fntocall)
#dfall = eval(fntocall)
#dfall= tnledger.tnPublicNotice(siteurl) 
# write_content_to_sql(dfall, siteurl)


# def parse():
#     conn1 = pymssql.connect(server=config.keys['server'], user=config.keys['username'], password=config.keys['password'], database=config.keys['database'])
#     curs = conn1.cursor()
#     sql = "SELECT AttrID, AttrName, AttrType, AttrLength FROM Attributes"
#     curs.execute(sql)
#     attr = curs.fetchone()

#     for attributes in attr:
#         print(attributes.loc[0])


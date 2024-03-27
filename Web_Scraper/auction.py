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
    print("1: Alabama")
    print("2: Arizona")
    print("3: Arkansas")
    print("4: California")
    print("5: Colorado")
    print("6: Georgia")
    print("7: Idaho")
    print("8: Illinois")
    print("9: Indiana")
    print("10: Kansas")
    print("11: Maine")
    print("12: Massachusetts")
    print("13: Minnesota")
    print("14: Mississippi")
    print("15: Missouri")
    print("16: Nebraska")
    print("17: Nevada")
    print("18: New Jersey")
    print("19: New Mexico")
    print("10: North Carolina")
    print("21: Ohio")
    print("22: Oregon")
    print("23: Pennsylvania")
    print("24: South Carolina")
    print("25: South Dakota")
    print("26: Tennessee")
    print("27: Tennessee Ledger")
    print("28: Texas")
    print("29: Utah")
    print("30: Virginia")
    print("31: Washington")
    print("32: Wyoming")
    choice = input("Enter the number of your choice: ")
    return choice



# Main program that invokes individual sites and saves data to DB
def main():
    choice = user_select_state()

    dt_today = date.today()
    end_date = date.strftime(dt_today, "%m/%d/%Y")
    start_date = date.strftime(dt_today - timedelta(7), "%m/%d/%Y")

    if choice == '1':
        siteurl = "https://www.alabamapublicnotices.com/(S(nowvxlolxhrtwtcyhgyzexk4))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '2':
        siteurl = "https://www.arizonapublicnotices.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '3':
        siteurl = "https://www.arkansaspublicnotices.com/(S(iwv5ywh1d4pwglzi3tgp1pqd))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '4':
        # California scraping
        siteurl = "https://www.capublicnotice.com/"  # Ensure this is the correct URL for California
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '5':
        siteurl = "https://www.publicnoticecolorado.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '6':
        siteurl = "https://www.georgiapublicnotice.com/"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '7':
        # Idaho scraping
        siteurl = "https://www.idahopublicnotices.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '8':
        siteurl = "https://www.publicnoticeillinois.com/(S(acg0brnnirfdehovjyj20ig4))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '9':
        siteurl = "https://www.publicnoticeindiana.com/(S(0flhp1nk4qvrrzyqemgomgu3))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '10':
        siteurl = "https://www.kansaspublicnotices.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '11':
        siteurl = "https://mainenotices.com/(S(2dgdqe0pz4guvnhoycxjue5z))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '12':
        siteurl = "https://www.masspublicnotices.org/(S(s43e0tkcc2aq0gdqjybak0dg))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '13':
        siteurl = "https://www.mnpublicnotice.com/(S(o4rwbjgyn5rcujmjrkfenwem))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '14':
        siteurl = "https://www.mspublicnotices.org/(S(yta5ummmhaeoa0oiyrf4abzf))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '15':
        siteurl = "https://www.mopublicnotices.com/(S(skzjxohmoq31x4t4ph0eyxbe))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '16':
        siteurl = "https://www.nepublicnotices.com/(S(n3vqaf3qvny5yn2tgas5puzz))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '17':
        siteurl = "https://www.nevadapublicnotice.com/"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '18':
        siteurl = "https://www.njpublicnotices.com/(S(sj4lgax2dyi22mp2wr00sc5k))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '19':
        siteurl = "https://www.newmexicopublicnotices.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '20':
        siteurl = "https://www.ncnotices.com/(S(30tkdtpubdykkyopexzalu42))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '21':
        siteurl = "https://www.publicnoticesohio.com/"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '22':
        siteurl = "https://www.publicnoticeoregon.com/(S(udtynok3jnxr5v1jhkkzidly))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '23':
        siteurl = "https://www.publicnoticepa.com/"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '24':
        siteurl = "https://www.scpublicnotices.com/(S(zr3qozc5sxwqhfmbajyvcomk))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '25':
        siteurl = "https://www.sdpublicnotices.com/"
        dfall = idaho2023.idPublicNotice(siteurl, start_date, end_date)
    elif choice == '26':
        siteurl = "https://www.tnpublicnotice.com/(S(efycd0n34a1pcelrrxmq0mu4))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '27':
        # For Tennessee, implement logic to find the appropriate Friday
        today = date.today()
        day_of_week = today.isoweekday()
        
        if day_of_week != 5:
            if day_of_week < 5:
                day_of_week += 7
            day_to_subtract = day_of_week - 5
            date_to_search = today - timedelta(days=day_to_subtract)
        else:
            date_to_search = today
        
        friday_date = date.strftime(date_to_search, "%m/%d/%Y")
        
        siteurl = f"https://tnledger.com/Notices.aspx?noticesDate={friday_date}"
        dfall = tnledger.tnPublicNotice(siteurl)
    elif choice == '28':
        siteurl = "https://www.texaspublicnotices.com/(S(kzeegwavdu3mlnumbjexd3t2))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '29':
        siteurl = "https://www.utahlegals.com/(S(f2w4igb1u1hct4jzwd5c3ms2))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '30':
        siteurl = "https://www.publicnoticevirginia.com/(S(fzf3pmn4rtene0kkb2fz110e))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '31':
        siteurl = "https://www.wapublicnotices.com/(S(4bhn45cvryy0ehlmhmu4wsbu))/default.aspx"
        dfall = georgia.ga_publicnotice(siteurl, start_date, end_date)
    elif choice == '32':
        siteurl = "https://www.wyopublicnotices.com/"
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


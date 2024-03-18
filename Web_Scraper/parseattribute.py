from attr import attributes
from sympy import content
import config
import pymssql
import pandas as pd
import re
import pyap

conn1 = pymssql.connect(server=config.keys['server'], user=config.keys['username'], password=config.keys['password'], database=config.keys['database'])
curs = conn1.cursor()

def parsevalueforregex(listingseqnum, attrid, attrlength, content):

    sql1 = "SELECT distinct a.AttrID, a.Regex FROM Attribute_Regex a WHERE a.AttrID = {}".format(attrid)
    curs.execute(sql1)
    regex_rows= curs.fetchall()

    
    sql1 = "SELECT distinct a.AttrID, a.TextBefore FROM Attribute_Text a WHERE a.AttrID = {}".format(attrid)
    curs.execute(sql1)
    text_rows= curs.fetchall()

    for regex_row in regex_rows:
        for text_row in text_rows:
            textbefore = text_row[1]
            regex = "({})".format(regex_row[1])
            texttoparse = content
            if len(textbefore) > 0:
                pos = texttoparse.find(textbefore)
                if pos < 0:
                    continue
                pos += len(textbefore)
                texttoparse = texttoparse[pos+1:pos+attrlength]
                texttoparse = " " + texttoparse + " "
            print(texttoparse)
            values = re.findall(regex,texttoparse)
            print(values)
            # val = re.findall("(\w{1,4}-?\w{1,4}-?\w{1,4}-?\w{1,4}-?\w{1,4})",texttoparse)
            # print
            for val in values:
                sql3 = "if not exists (select top 1 AttrValue from ListingAttributeValuesTemp where ListingSeqNum={} and AttrID={} \
                        and AttrValue = '{}') \
                        INSERT INTO ListingAttributeValuesTemp (ListingSeqNum, AttrID, AttrValue) values ({},{},'{}')".format(listingseqnum, row[0],val.strip(),listingseqnum, row[0],val.strip())
                print(sql3)
                curs.execute(sql3)
                conn1.commit()
                #write to table listing attributes values temp
                #seq num = seqnum
                #attrid = attributes[0]
                #attrvalue = val
                print

def parsevalueforaddress(listingseqnum, attrid, attrlength, content):

    sql1 = "SELECT a.AttrID, a.TextBefore, a.Regex FROM Attribute_Regex a WHERE a.AttrID = {}".format(attrid)
    curs.execute(sql1)
    regex_rows= curs.fetchall()

    for row in regex_rows:
        textbefore = row[1]
        regex = "({})".format(row[2])
        texttoparse = content
        if len(textbefore) > 0:
            pos = texttoparse.find(textbefore)
            if pos < 0:
                continue
            pos += len(textbefore)
            texttoparse = texttoparse[pos+1:pos+attrlength]
        print(texttoparse)
        values = pyap.parse(texttoparse,country="US")
        print(values)
        # val = re.findall("(\w{1,4}-?\w{1,4}-?\w{1,4}-?\w{1,4}-?\w{1,4})",texttoparse)
        # print
        for val in values:
            if (val.find("'")) >= 0:
                val = val.replace("'","''")

            sql3 = "INSERT INTO ListingAttributeValuesTemp (ListingSeqNum, AttrID, AttrValue) values ({},{},'{}')".format(listingseqnum, row[0],val)
            print(sql3)
            curs.execute(sql3)
            conn1.commit()
            #write to table listing attributes values temp
            #seq num = seqnum
            #attrid = attributes[0]
            #attrvalue = val
            print


def parse_regex(seqnum,content):


    sql = "SELECT AttrID, AttrName, AttrType, AttrLength FROM Attributes"
    curs.execute(sql)
    attr = curs.fetchall()

    for attributes in attr:
        attrlength = attributes[3]
        attrname = attributes[1]
        attrtype = attributes[2]
    
        print(attributes)
        if attrtype == "RegEx":
            parsevalueforregex(seqnum, attributes[0], attrlength, content)
        # elif attrtype == "Address":
        #     parsevalueforaddress(seqnum, attributes[0], attrlength, content)

def parse_tn(seqnum, listing):

    pipeList = listing.split('|')

    for attr in pipeList:
        sql3 = ""

        if attr.find("Borrower:") >= 0:
            attrID = 12
            parts = attr.split(":")
            sql3 = "if not exists (select top 1 AttrValue from ListingAttributeValuesTemp where ListingSeqNum={} and AttrID={} \
                    and AttrValue = '{}') \
                    INSERT INTO ListingAttributeValuesTemp (ListingSeqNum, AttrID, AttrValue) values ({},{},'{}')".format(seqnum, attrID,parts[1].strip(),seqnum, attrID,parts[1].strip())
        
        elif attr.find("Address:") >= 0:
            attrID = 3
            parts = attr.split(":")
            sql3 = "if not exists (select top 1 AttrValue from ListingAttributeValuesTemp where ListingSeqNum={} and AttrID={} \
                    and AttrValue = '{}') \
                    INSERT INTO ListingAttributeValuesTemp (ListingSeqNum, AttrID, AttrValue) values ({},{},'{}')".format(seqnum, attrID,parts[1].strip(),seqnum, attrID,parts[1].strip())
        
        elif attr.find("Substitute Trustee:") >= 0:
            attrID = 9
            parts = attr.split(":")
            sql3 = "if not exists (select top 1 AttrValue from ListingAttributeValuesTemp where ListingSeqNum={} and AttrID={} \
                    and AttrValue = '{}') \
                    INSERT INTO ListingAttributeValuesTemp (ListingSeqNum, AttrID, AttrValue) values ({},{},'{}')".format(seqnum, attrID,parts[1].strip(),seqnum, attrID,parts[1].strip())
        
        elif attr.find("Auction Date:") >= 0:
            attrID = 4
            parts = attr.split(":")
            sql3 = "if not exists (select top 1 AttrValue from ListingAttributeValuesTemp where ListingSeqNum={} and AttrID={} \
                    and AttrValue = '{}') \
                    INSERT INTO ListingAttributeValuesTemp (ListingSeqNum, AttrID, AttrValue) values ({},{},'{}')".format(seqnum, attrID,parts[1].strip(),seqnum, attrID,parts[1].strip())
        



        print(sql3)
        curs.execute(sql3)
        conn1.commit()

            
        print(attr)


    



    

# parse tn ledger
# (1) split content with pipes
# (2) take each element and match to items in attribute title
# (3) 

sql2 = "SELECT seqnum,Content FROM Listing WHERE seqnum => 62"
curs.execute(sql2)
propertylist = curs.fetchall()
for fields in propertylist:
   # print(fields[1])
    val = fields[1].replace("</br>", " ")
   # print (val)
   # parse_regex(fields[0],val[1])
    parse_tn(fields[0],val)
    








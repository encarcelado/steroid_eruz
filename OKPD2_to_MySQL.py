#скрипт забирает все данные ЕРУЗ и закидывает их в MySQL

import bs4 as bs
import urllib.request
#import os
import mysql.connector
import re
import time
from colorama import Fore, Back, Style
from datetime import date
import csv
import codecs
import sys

today = date.today()
d1 = today.strftime("%d.%m.%Y")
print("Сегодня:", d1)
d1 = str(d1)


mydb = mysql.connector.connect(host="v0434826.beget.tech", user="v0434826_eruz", passwd="1560ford", database = "v0434826_eruz")
mydb.autocommit = True

print(mydb)

if(mydb):
    print(Fore.BLUE + "Connection is successful")
    print(Style.RESET_ALL)
else:
    print("Connection is unsuccessful")

my_cursor = mydb.cursor()

# my_cursor.execute("SHOW TABLES")
# for table in my_cursor:
#     print(table[0])

#my_cursor.execute("SELECT * FROM nalog_codes WHERE region_code = 02")

#for table in my_cursor:
#    print(table)

#my_cursor.execute("SELECT * FROM okved_codes WHERE SubKod1 = 1")

#for table in my_cursor:
#    print(table)

# my_cursor.execute("SELECT nalog_city FROM nalog_codes WHERE nalog_region LIKE '%Башкортостан%'")
#
# for table in my_cursor:
#     print(table[0])

with codecs.open('okpd2.csv', "rb", encoding='utf8') as okpd2file:
    #text = okpd2file.read()
    #print(text)
    okpd2fullList = okpd2file.readlines()
    lineNum = 1
    
    for okpd2line in okpd2fullList:
        okpd2line = okpd2line.strip()
        #print(okpd2line)
        okpd2lineSplit = okpd2line.split(";")
        okpd2_code = okpd2lineSplit[0]
        okpd2_desc = okpd2lineSplit[1]
        print(lineNum, " ", okpd2_code, " ", okpd2_desc)
        lineNum = lineNum + 1
        sql3 = "INSERT INTO okpd2_2020(okpd2_code, okpd2_desc) values(%s, %s)"
        my_cursor.execute(sql3, (okpd2_code, okpd2_desc))








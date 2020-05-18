#!/usr/bin/python

# News Headlines for Raspberry Pi w/Adafruit Mini Thermal Printer.
# 
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
# 
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import urllib, time, json, math
from Adafruit_Thermal import *
import unicodedata


# APIKEY can be obtained by registering for a developer's trial account
# at https://newsapi.org

APIKEY = '224cd1b6b5824016804d037808e84a45'

#SOURCES for news headlines
SOURCES = 'associated-press' 


def cleanText(text):
    # Fix unicode apostrophes
    fix_quotes = text.replace(u'\u2018', '\'').replace(u'\u2019', '\'')
    # Fix unicode dashes
    fix_dashes = fix_quotes.replace(u'\u2013', '-').replace(u'\u2014', '-')

    # Replace accented characters
    fixed = unicodedata.normalize('NFD', fix_dashes)

    # Printer only supports ASCII 
    # return fixed.encode('ascii','ignore')

    # for now, show unicode escape sequence to id characters
    return fixed.encode('ascii','backslashreplace')


# Write a headline to the printer
def headline(idx):
    printer.println()
    title = data['articles'][idx]['title']
    lede = cleanText(title)
    printer.print(lede)
    printer.println()
    return

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# grw - Dec 1, 2019
# NewsApi.org 

try:
    query_url = 'http://newsapi.org/v2/top-headlines?' + 'sources=' + SOURCES + '&apiKey=' + APIKEY

    response = ( urllib.urlopen(query_url).read())

    data = json.loads(response)

    count = int(data['totalResults'])

    # Don't do more than 11 stories
    # Main lede is often 'Ten Things to Know' followed by 10 stories
    if count > 11:
	count = 11		

    #Print heading
    today = time.strftime("%A, %B %d, %Y")

    printer.boldOn()
    printer.println('{:^32}'.format("AP Top Stories"))
    printer.println('{:^32}'.format(today))
    printer.boldOff()
    # Required NewsAPI.org attribution
    printer.println('{:^32}'.format("powered by NewsAPI.org"))
    printer.println()

    for i in range(0, count):
    	headline(i)

    printer.feed(3)

except Exception as e:
    printer.println('--Error--')  # debugging 
    printer.println(e)  # debugging 
    # print('--Error--')  
    # print(e)
    print (1) # send true value back to main
    exit(0)

print (0) # send false  value back to main


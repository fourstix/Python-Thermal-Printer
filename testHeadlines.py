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


# APIKEY can be obtained by registering for a developer's trial account
# at https://newsapi.org

APIKEY = 'YOUR_API_KEY'

#SOURCES for news headlines
SOURCES = 'associated-press' 

def cleanText(text):
    # Fix unicode apostrophes
    fixed = text.replace(u'\u2018', '\'').replace(u'\u2019', '\'')

    # Printer only supports ASCII 
    # return fixed.encode('ascii','ignore')

    # for now, show unicode escape sequence to id characters
    return fixed.encode('ascii','backslashreplace')


# Write one headline to the printer
def headline(idx):
    # print('Inside headline')
    # print('Index')
    print(idx)
    printer.println()
    # print('Getting title')
    title = data['articles'][idx]['title']
    print(title)
    lede = cleanText(title)
    # print(lede)
    printer.print(lede)
    printer.println()
    return

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# grw - Dec 1, 2019
# NewsApi.org 

try:
    query_url = 'http://newsapi.org/v2/top-headlines?' + 'sources=' + SOURCES + '&apiKey=' + APIKEY

    # print(query_url)
    response = ( urllib.urlopen(query_url).read())
    # print('Got response')

# Fake response to avoid using up our daily trial API limit
#  response = '''
#  {
#  ...
#  }
#  '''

    # print('Loading json data from response string')
    data = json.loads(response)
    # print('Printing Type')
    # print(type(data))
    # print('Printing status')
    # print(data['status'])

    # print('Printing result count')
    count = int(data['totalResults'])
    print(count)

    # Don't do more than 11 stories
    # Main lede is often 'Ten Things to Know' followed by 10 stories
    if count > 11:
	count = 11		

    #Print heading
    today = time.strftime("%A, %B %d, %Y")
    # print(today)
    printer.boldOn()
    printer.println('{:^32}'.format("AP Top Stories"))
    printer.println('{:^32}'.format(today))
    printer.boldOff()
    # Required NewsAPI.org attribution
    printer.println('{:^32}'.format("powered by NewsAPI.org"))
    printer.println()

    for i in range(0, count):
	# print('Calling headline ' + str(i))
    	headline(i)

    printer.feed(3)

except Exception as e:
    printer.println('--Error--')  # debugging 
    printer.println(e)  # debugging 
    print('--Error--')  
    print(e)
    print (1) # send true value back to main
    exit(0)

print (0) # send false  value back to main


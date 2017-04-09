# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 22:00:15 2017

@author: Kush Shukla
"""

MONEY_CONTROL_TERMINAL = "http://www.moneycontrol.com/terminal/index_v1.php?index=9"

def getSiteSource(site_name):
    '''
    Returns the source file for the html page
    '''
    import urllib.request
    try:
        response = urllib.request.urlopen(site_name)
    except ValueError:
        print("Check the url again!")
    except Exception:
        print("Something is Fishy!")
            
    return response.read()

def printRequiredStockPrice():
    terminal_source = getSiteSource(MONEY_CONTROL_TERMINAL)
    from bs4 import BeautifulSoup as bs
    soup = bs(terminal_source, 'html.parser')
    print("NIFTY 50: " + soup.find(id="Ter_indic").contents[0])
    print("ACC Ltd : " + soup.find(id="ACC_ltp").contents[0])
    print("\n")

#
#import time
#while(True):
#    try:
#        printRequiredStockPrice()
#        time.sleep(5)
#        
#    except KeyboardInterrupt:
#        break
#    
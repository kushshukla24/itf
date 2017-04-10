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

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')
fig = plt.figure()
axl = fig.add_subplot(1,1,1)

def animate(i):
    graph_data = open('example.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line)<1:
            continue
        x, y = line. split(',')
        xs.append(x)
        ys.append(y)
    
    axl.clear()
    axl.plot(xs,ys)

ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.show()

#import time
#while(True):
#    try:
#        printRequiredStockPrice()
#        time.sleep(5)
#        
#    except KeyboardInterrupt:
#        break
#    
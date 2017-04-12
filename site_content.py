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

from bs4 import BeautifulSoup as bs
def getStockPrice():
    terminal_source = getSiteSource(MONEY_CONTROL_TERMINAL)
    soup = bs(terminal_source, 'html.parser')
    price = float(soup.find(id="Ter_indic").contents[0])
    return price

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')
fig = plt.figure()
axl = fig.add_subplot(1,1,1)

xs = []
ys = []
def animate(i):
    stock_price = getStockPrice()
    xs.append(i)
    ys.append(stock_price)
    axl.clear()
    axl.plot(xs,ys)

ani = animation.FuncAnimation(fig, animate, interval = 10000)
plt.show()



   
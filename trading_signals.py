# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:55:19 2017

@author: kush

PS: Only Python 2.x is supported
"""

import urllib2
import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as BS
import talib as ta
from pandas.io.data import DataReader as dr

MONEY_CONTROL_TERMINAL = "http://www.moneycontrol.com/terminal/index_v1.php?index=11"
from_mail = "yenwatcher@gmail.com"
to_mail = "kushukla@ymail.com"

def send_mail(yen_inr_val):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    
    msg = MIMEMultipart()
    msg['From'] = from_mail 
    msg['To'] = to_mail
    msg['Subject'] = "YEN to INR Conversion Rate reached your expectation!"
    body = "Current Conversion Rate is:" + yen_inr_val + "\n\nRegards,\nConversion Team, Japan\n "
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("yenwatcher@gmail.com", "yenwatcher18")
    
    server.sendmail(from_mail, to_mail, msg.as_string())
    
def getSiteSource(site_name):
    '''
    Returns the source file for the html page
    '''
    import urllib2
    try:
        response = urllib2.urlopen(site_name)
    except ValueError:
        print("Check the url again!")
    except Exception:
        print("Something is Fishy!")
            
    return response.read()


global last_best_value
last_best_value = 0
def get_share_price(stock_id):
    source = getSiteSource(MONEY_CONTROL_TERMINAL)
    soup = BS(source, 'html.parser')
    found_stock_id = soup.find(id=stock_id)
    if found_stock_id is None:
        print stock_id + "is incorrect or not found!"
        return
    content = found_stock_id.contents
    if content is not None and len(content)>0:
        last_best_value = content[0]
        
    return last_best_value

def get_last_trading_day_quotes(symbol):
    today = datetime.today()
    i = 1
    yesterday = today - timedelta(i)

    df = dr(symbol, 'yahoo', yesterday, today)
    while df.empty:
        i = i+1
        yesterday = today - timedelta(i)
        df = dr(symbol, 'yahoo', yesterday, today)

    return df

def get_pivot_points_for_today(symbol):
    df = get_last_trading_day_quotes(symbol)
    high = df['High'][0]
    low = df['Low'][0]
    close = df['Close'][0]

    pivot = (high + low + close)/3
    s1 = (pivot * 2) - high
    s2 = pivot - (high - low)
    r1 = (pivot*2) - low
    r2 = pivot + (high-low)

    return (pivot, s1, r1, s2, r2)



print get_pivot_points_for_today('BHEL.NS')
df = get_last_trading_day_quotes('BHEL.NS')

df['Volume'] = df['Volume'].apply(lambda x: x/1.)
print df
print ta.MFI(df['High'], df['Low'], df['Close'], df['Volume'])
##
##while True:
##    try:
##        rate_string = get_share_price("BHE_ltp")
##
##        if rate_string is None:
##            break
##
##        price = float(rate_string)
##        print price
##        #trigger 1
##        if price-pivot < 0.1 and price-pivot > 0:
##            print "Bullish trend"
##        elif pivot-price < 0.1 and pivot-price > 0:
##            print "Bearish trend"
##        
##        time.sleep(10)
##    except KeyboardInterrupt:
##        break
##    
##    

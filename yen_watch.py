# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 12:55:19 2017

@author: love
"""
import requests
from bs4 import BeautifulSoup

YEN_TO_RUPEE = "https://www.yen2rupees.com"
MONEY_CONTROL_TERMINAL = "http://www.moneycontrol.com/terminal/index_v1.php?index=11"
from_mail = "yenwatcher@gmail.com"
to_mail = "kushukla@ymail.com"

class sms:
    def __init__(self,username,password):
        '''
        Takes username and password as parameters for constructors
        and try to log in
        '''
        self.url='http://site24.way2sms.com/Login1.action?'
        self.cred={'username': username, 'password': password}
        self.s=requests.Session()
        '''
        changing s.headers['User-Agent'] to spoof that python is requesting
        '''
        self.s.headers['User-Agent']="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"
        self.q=self.s.post(self.url,data=self.cred)
        self.loggedIn=False
        if self.q.status_code!=200:
            self.loggedIn=False
        else:
            self.loggedIn=True
        self.jsid=self.s.cookies.get_dict()['JSESSIONID'][4:]    
        
    def msgSentToday(self):
        '''
        Returns number of SMS sent today as there is a limit of 100 messages everyday..!
        '''

        self.msg_left_url='http://site24.way2sms.com/sentSMS?Token='+self.jsid
        self.q=self.s.get(self.msg_left_url)
        self.soup=BeautifulSoup(self.q.text,'html.parser')    
        self.t=self.soup.find("div",{"class":"hed"}).h2.text
        self.sent=0
        for self.i in self.t:
            if self.i.isdecimal():
                self.sent=10*self.sent+int(self.i)
        return self.sent

    def send(self,mobile_no,msg):
        '''
        Sends the message to the given mobile number
        '''

        if len(msg)>139 or len(mobile_no)!=10 :
            return False                            
        self.payload={'ssaction':'ss',
                'Token':self.jsid,                
                    'mobile':mobile_no,                
                        'message':msg,                
                    'msgLen':'129'
                        }
        self.msg_url='http://site24.way2sms.com/smstoss.action'
        self.q=self.s.post(self.msg_url,data=self.payload)

        if self.q.status_code==200:
            return True
        return False
    
    def logout(self):
        self.s.get('http://site24.way2sms.com/entry?ec=0080&id=dwks')
        self.s.close()
        self.loggedIn=False
        
def send_sms(msg):
    q=sms("9765983653","realmadrid")
    q.send("9765983653",msg)
    q.msgSentToday()
    q.logout()


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

def mrpl_price():
    source = getSiteSource(MONEY_CONTROL_TERMINAL)
    soup = BeautifulSoup(source, 'html.parser')
    content = soup.find(id="MRP_ltp").contents
    if len(content)>0:
        last_best_value = content[0]
        
    return last_best_value


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
    
while True:
    try:
        rate = float(mrpl_price())
        print(rate)
        if rate-MRPL_SUPPORT <= 0.00001:
            send_sms(str(rate))
            send_mail(str(rate))
        
        import time
        time.sleep(100)
    except KeyboardInterrupt:
        break
    
    

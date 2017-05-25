# -*- coding: utf-8 -*-
"""
Created on Thu May 25 22:43:44 2017

@author: Kush Shukla
"""


import csv
import time
import requests
from bs4 import BeautifulSoup
from pattern.en import ngrams

Base_url = "http://www.moneycontrol.com"

# Build a dictionary of companies and their abbreviated names 
companies = {'cadilahealthcare':'CHC','piramalenterprises':'PH05',
             'glenmarkpharma':'GP08','glaxosmithklinepharmaceuticals':'GSK',
             'sunpharmaceuticalindustries':'SPI','lupinlaboratories':'LL',
             'cipla':'C','aurobindopharma':'AP',
             'drreddyslaboratories':'DRL','divislaboratories':'DL03'}
             
# Create a list of the news section urls of the respective companies 
url_list = ['http://www.moneycontrol.com/company-article/{}/news/{}#{}'.format(k,v,v) for k,v in companies.iteritems()]
print url_list

# Create an empty list which will contain the selected news articles 
List_of_links = []   

reccomendation_words = ['buy', 'sell', 'hold', 'resistance', 'bullish', 'bull'
                        , 'bearish', 'bear', 'support', 'resistance', 'prakash gaba'
                        , 'icici securities', 'kr choksey', 'expert', 'gaurang shah', 
                        'stop loss', 'gautam trivedi']
reccomendation_news = []
informational_news = []
# Extract the relevant news articles weblinks from the news section of selected companies
for urls in url_list:
   html = requests.get(urls)
   soup = BeautifulSoup(html.text,'html.parser') # Create a BeautifulSoup object 

   # Retrieve a list of all the links and the titles for the respective links
   #word1,word2,word3 = "US","USA","USFDA"
   
   sub_links = soup.find_all('a', class_='arial11_summ')
   for links in sub_links:
      sp = BeautifulSoup(str(links),'html.parser')  # first convert into a string
      tag = sp.a
      info = tag['title'].lower()
      if not any(word in info for word in reccomendation_words):
          informational_news.append(tag['title'])


# Create a dictionary of positive/negative words related to the Pharma Sector
reader = csv.reader(open('dict.csv', 'r'))
pharma_dict = dict((rows[0],rows[1]) for rows in reader)
#
## Remove the duplicate news articles based on News Title
unique_news = list(set(informational_news))
df = []
for news in unique_news:
    final_text = ngrams(news, n=1, punctuation=".,;:!?()[]{}`''\"@#$^&*+-|=~_", continuous=False)
    
    #Checking if any of the words in the news article text matches with the words in the Pharma dictionary(pos/neg)
    new_dict = {}
    positive_score,negative_score = 0,0
   
    for x in final_text:
        if pharma_dict.has_key(x[0]):
            new_dict[x[0]] = pharma_dict[x[0]] 
                  
    positive_list = [] ; negative_list = [];
    for key, value in new_dict.items():
        if value == 'positive': positive_list.append(key)
        if value == 'negative': negative_list.append(key)
                           
   # Compute the positive score, the negative score for each news articles
    positive_score = len(positive_list) ; negative_score = len(negative_list);
   #print positive_list ; print negative_list ;
   #print positive_score ; print negative_score;
   
   # Appending the empty list to create the final Sentiment analysis output
    var_nos = [news, positive_score, negative_score]
    print var_nos
    print "\n\n"
    df.append(var_nos)

#for item in df:
#    print(item)

#
## Creating an empty list which will be filled later with news article links, and Polarity values (pos/neg)

#
## Open the choosen news articles and extract the main text  
#for selected_links in unique_links:
#   results_url = selected_links 
#   #print results_url
#   
#   results = requests.get(results_url)
#   results_text = BeautifulSoup(results.text)
#   extract_text = results_text.find(class_='arti_cont')
#   final_text = extract_text.get_text()
#   
#   # Pre-processing the extracted text using ngrams function from the pattern package   
#   
   

   
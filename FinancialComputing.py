# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 20:16:16 2017

@author: Kush Shukla
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import bs4 as bs
import pickle
import requests
import os
import numpy as np
from collections import Counter
from sklearn import svm, cross_validation, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier

MONEY_CONTROL_TERMINAL = "http://www.moneycontrol.com/terminal/index_v1.php?index=9"
WIKIPEIA_NIFTY_50 = "https://en.wikipedia.org/wiki/NIFTY_50"

style.use('ggplot')

def get_equity_price_dataFrame(symbol, start, end):
    '''
    Returns the data frame consisting of
    Open, Low, High, Close, Adjusted Close, Volume
    for the symbol from Yahoo Finance!
    '''
    return web.DataReader('BHEL.NS', 'yahoo', start, end)

def store_data_to_csv(df, symbol):
    '''
    Store the stock price data in a csv file
    where the name of the csv is the ticker symbol
    of the stock
    Returns the name of the csv file
    '''
    name = symbol.split('.')[0]
    csv_filename = name+'.csv'
    df.to_csv(csv_filename)
    return csv_filename
    
def read_stock_price_csv(csv_filename):
    '''
    Returns the data frame based on the price data of the 
    csv file
    '''
    return pd.read_csv(csv_filename, parse_dates=True, index_col=0)

def line_stock_price_data(df, column):
    '''
    Plots the line chart of data frame for the input column
    '''
    if len(column)>0:
        df[column].plot()
    else:
        df.plot()
    
    plt.show()
    return
    
def calculate_SMA(df, column, window_size, minimum_period):
    '''
    Returns a data Frame of Simple Moving Average of the data frame
    for specified columns with window size and minimum period
    '''
    return df[column].rolling(window=window_size, min_periods=minimum_period).mean()

    
def plot_adjusted_close_line_volume_bar(df):
    '''
    Plots speciic plot containing the 
    Adjusted close price of the data frame and Volume as bar 
    below the line chart
    '''
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

    ax1.plot(df.index, df['Adj Close'])
    #ax1.plot(df.index, df['100ma'])
    ax2.bar(df.index, df['Volume'])
    plt.show()
    return
    

def plot_candlestick_adjusted_close(df):
    '''
    Plots the candlestick chart for the adjusted close of the stock
    price data
    '''
    df_ohlc = df['Adj Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()
    
    df_ohlc = df_ohlc.reset_index()
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    
    #fig = plt.figure()
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1,sharex=ax1)
    ax1.xaxis_date()
    
    candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
    ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

    plt.show()
    return



def save_nifty50_company_names():
    '''
    Returns the list of NIFTY 50 companies
    '''
    response = requests.get(MONEY_CONTROL_TERMINAL)
    soup = bs.BeautifulSoup(response.text, 'lxml')
    links = soup.findAll('a', {'class': 'bl_12'})
    
    company_names = []
    for link in links:
        name = link.b.string
        company_names.append(name)
        
    with open("nifty50.pickle","wb") as f:
        pickle.dump(company_names,f)
        
    return company_names

def save_nifty50_tickers():
    '''
    Returns the list of ticker symbols for NIFTY 50
    from the table in the Wikipedia page
    '''
    resp = requests.get(WIKIPEIA_NIFTY_50)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker)
#        
    with open("nifty50tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers

def get_data_from_yahoo(reload_nifty50=False):
    '''
    Extracts Data from Yahoo for the NIFTY 50 Tickers
    '''
    if reload_nifty50:
        tickers = save_nifty50_tickers()
    else:
        with open("nifty50tickers.pickle","rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime(2016, 12, 31)
    
    print(tickers)
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            yahoo_symbol = ticker + ".NS"
            
            try:
                df = web.DataReader(yahoo_symbol, "yahoo", start, end)
            except Exception:
                continue
            
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

    return
    
def compile_data():
    '''
    Creates a data frame with Adjusted prices of all the tickers of 
    NIFTY 50
    '''
    with open("nifty50tickers.pickle","rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    
    for count,ticker in enumerate(tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close':ticker}, inplace=True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('nifty50_joined_closes.csv')

def visualize_data():
    '''
    Plots a correlation heatmap matrix 
    specifying the correlation among the stocks 
    listed in the NIFTY 50 index
    '''
    df = pd.read_csv('nifty50_joined_closes.csv')
    #df['AAPL'].plot()
    #plt.show()
    df_corr = df.corr()
    print(df_corr.head())
    df_corr.to_csv('nifty50corr.csv')
    
    data1 = df_corr.values
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.RdYlGn)
    fig1.colorbar(heatmap1)

    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap1.set_clim(-1,1)
    plt.tight_layout()
    #plt.savefig("correlations.png", dpi = (300))
    plt.show()
    
    return


def process_data_for_labels(ticker):
    '''
    Pre-processing for data 
    '''
    hm_days = 7
    df = pd.read_csv('nifty50_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    
    for i in range(1,hm_days+1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
        
    df.fillna(0, inplace=True)
    return tickers, df
    
def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0
    
def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)

    df['{}_target'.format(ticker)] = list(map( buy_sell_hold,
                                               df['{}_1d'.format(ticker)],
                                               df['{}_2d'.format(ticker)],
                                               df['{}_3d'.format(ticker)],
                                               df['{}_4d'.format(ticker)],
                                               df['{}_5d'.format(ticker)],
                                               df['{}_6d'.format(ticker)],
                                               df['{}_7d'.format(ticker)] ))
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:',Counter(str_vals))
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X,y,df
    
def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,
                                                        y,
                                                        test_size=0.25)
    #clf = neighbors.KNeighborsClassifier()

    clf = VotingClassifier([('lsvc',svm.LinearSVC()),
                            ('knn',neighbors.KNeighborsClassifier()),
                            ('rfor',RandomForestClassifier())])


    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('accuracy:',confidence)
    predictions = clf.predict(X_test)
    print('predicted class counts:',Counter(predictions))
    return confidence

## Executing the Machine Learning Startegies on all tickers
#from statistics import mean
#
#with open("sp500tickers.pickle","rb") as f:
#    tickers = pickle.load(f)
#
#accuracies = []
#for count,ticker in enumerate(tickers):
#
#    if count%10==0:
#        print(count)
#        
#    accuracy = do_ml(ticker)
#    accuracies.append(accuracy)
#    print("{} accuracy: {}. Average accuracy:{}".format(ticker,accuracy,mean(accuracies)))
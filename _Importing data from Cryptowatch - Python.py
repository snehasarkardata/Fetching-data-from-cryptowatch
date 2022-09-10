#!/usr/bin/env python
# coding: utf-8

# In[82]:


#pulling cryptocurrencies prices from a public API and download them as Excel files.


# In[83]:


import requests
import pandas as pd


# In[84]:


#pull data from Bitcoin and Ether, two of the most popular cryptocurrencies, for the last 7 days

def get_historic_price(symbol, exchange='bitfinex', after='2018-09-01'):
    url = 'https://api.cryptowat.ch/markets/{exchange}/{symbol}usd/ohlc'.format(
        symbol=symbol, exchange=exchange)
    resp = requests.get(url, params={
        'periods': '3600',
        'after': str(int(pd.Timestamp(after).timestamp()))
    })
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame(data['result']['3600'], columns=[
        'CloseTime', 'OpenPrice', 'HighPrice', 'LowPrice', 'ClosePrice', 'Volume', 'NA'
    ])
    df['CloseTime'] = pd.to_datetime(df['CloseTime'], unit='s')
    df.set_index('CloseTime', inplace=True)
    return df


# In[85]:


last_week = (pd.Timestamp.now() - pd.offsets.Day(7))
last_week


# In[86]:


btc = get_historic_price('btc', 'bitstamp', after=last_week)


# In[87]:


eth = get_historic_price('eth', 'bitstamp', after=last_week)


# In[88]:


#Bitcoin
btc.head()
btc['ClosePrice'].plot(figsize=(15, 7))


# In[89]:


#ether
eth.head()
eth['ClosePrice'].plot(figsize=(15, 7))
eth.head()


# In[90]:


#Dynamic plots with Bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook


# In[91]:


output_notebook()


# In[92]:


p1 = figure(x_axis_type="datetime", title="Crypto Prices", width=800)
p1.grid.grid_line_alpha=0.3
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Price'

p1.line(btc.index, btc['ClosePrice'], color='#f2a900', legend='Bitcoin')
#p1.line(eth.index, eth['ClosePrice'], color='#A6CEE3', legend='Ether')

p1.legend.location = "top_left"

show(p1)


# In[93]:


#Exporting to Excel
writer = pd.ExcelWriter('cryptosss.xlsx')


# In[94]:


#We'll now write both our Bitcoin and Ether data as separate sheets:

btc.to_excel(writer, sheet_name='Bitcoin')


# In[95]:


eth.to_excel(writer, sheet_name='Ether')


# In[96]:


writer.save()


# In[ ]:





# In[66]:





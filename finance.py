#import packages
import streamlit as st
import pandas as pd
import plotly_express as px
from PIL import Image
from streamlit.commands.page_config import Layout
import plotly.graph_objects as go  
import yfinance as yf
import datetime


#----------------------------#
# Upgrade streamlit library
# pip install --upgrade streamlit

#-----------------------------#
# Page layout
icon = Image.open('images/stocks.ico')

st.set_page_config(page_title='Financial Market Data Analysis',
                   page_icon=icon,
                   layout='wide',
                   initial_sidebar_state="auto",
                   menu_items=None)

st.title('Financial Market Data Analysis')

microsoft = yf.download('MSFT')
amazon = yf.download('AMZN')
netflix = yf.download('NFLX')
google = yf.download('GOOG')
apple = yf.download('AAPL')

@st.cache_data
def percent_change(data):
    change = round(((data.Close.values[-1] - data.Open.values[-1]) / data.Open.values[-1]) * 100, 2)
    return change

@st.cache_data
def closing(data):
    closing = round(data.Close.values[-1], 2)
    return closing

con1, con2, con3, con4, con5 = st.columns(5)
# Display the stock prices using st.metric
con1.metric(label="Microsoft", value=closing(microsoft), 
            delta=percent_change(microsoft))
con2.metric(label="Amazon", value=closing(amazon), delta=percent_change(amazon))
con3.metric(label="Netflix", value=closing(netflix), delta=percent_change(netflix))
con4.metric(label="Google", value=closing(google), delta=percent_change(google))
con5.metric(label="APPLE", value=closing(apple), delta=percent_change(apple))


#--------------------------------------------------+
# sidebar
# text imput ticker
with st.sidebar:
    st.subheader('Choose your tickers')
    ticker_symbols = st.text_input('Type Ticker', 'AAPL').split()

with st.sidebar:
    st.write('Some common ticker symbols :') 
    st.write('(AAPL) Apple, (MSFT) Microsoft, (GOOG) Google, (NFLX) Netflix, (BTC-USD) Bitcoin')
    st.subheader('')
    st.write('Tips: ')
    st.write('You can list multiple tickers separated by a space: AAPL MSFT GOOG')
    
#-------------------------------------------#
#download ticker 
@st.cache_data
def load(data):
    data = yf.download(data)
    return data

ticker = load(ticker_symbols)

#-------------------------------------------#

# display last 5 values of ticker dataset
st.subheader(ticker_symbols)
st.write(ticker.tail())

@st.cache_data
def download(df):
    return df.to_csv().encode('utf-8')

csv = download(ticker)
    
st.download_button('Download ticker data', csv, file_name='ticker_data.csv', mime='text/csv')

#-------------------------------------------#

st.title('')
# show index values of ticker
st.subheader('Time difference in data')
st.write('Start : ', ticker.index.min(), ' , End : ', ticker.index.max(), ' ,  Difference : ', abs(ticker.index.max() - ticker.index.min()))
st.title('')

#-------------------------------------------#

# candlestick
st.subheader('Price Chart')
candlestick = st.checkbox('Candlestick Chart (limit one ticker)')

if len(ticker_symbols) == 1 and candlestick:
    fig = go.Figure(data=[go.Candlestick(x=ticker.index,
                    open=ticker.Open,
                    high=ticker.High,
                    low=ticker.Low,
                    close=ticker.Close)])
    fig.update_layout(xaxis_rangeslider_visible=False, height=800, width=1200)
    fig.update_layout(title= str(ticker) + ' Price Action')
    st.write(fig)
elif len(ticker_symbols) != 1 and candlestick:
    st.error('You selected more than one ticker, cannot show candlesticks')
else:
    st.write(px.line(ticker.Close, title=str(ticker) + ' Price Action', template='presentation', labels={'value': 'USD'}, height=800, width=1200))
st.title('')

#-------------------------------------------#
# volume 
volume = st.button('Picked one ticker')
if volume or len(ticker_symbols)==1:
    st.subheader('Volume')
    st.subheader('Volume')
    st.write(px.line(ticker, y=ticker.Volume, x=ticker.index, log_y=True, height=800, width=1200))
else:
    st.error('Cannot show volume of multiple tickers. Please select one.')

st.title('')
st.title('')

#-------------------------------------------#

# filter dates
with st.sidebar:
    st.subheader('')
    st.subheader('Chose Date Filters')
    date_start = st.text_input('Input start date for data', '1980-01-01')
    date_end = st.text_input('Input end date', datetime.datetime.now().strftime('%Y-%m-%d'))

# summary stats

if date_start != '1980-01-01' or date_end != datetime.datetime.now().strftime('%Y-%m-%d'):
    st.subheader('Filtered Summary Statistics')
    st.write(ticker[date_start:date_end].describe())
else:
    st.subheader('Summary Statistics')
    st.write(ticker.describe())
st.title('')
#-----------------------------------#
with st.sidebar:
    st.subheader('')
    st.subheader('Chose MA')
    window = st.select_slider('Moving average window', [5, 10, 20, 50, 100, 200])
   

# Load MANGA 
amzn = load('AMZN')
aapl = load('AAPL')
goog = load('GOOG')
msft = load('MSFT')
nflx = load('NFLX')
nasdaq = load('QQQ')

# Combine stocks
stocks = pd.concat([amzn.Close, aapl.Close, goog.Close, msft.Close, nflx.Close, nasdaq.Close], axis=1,)
# label columns
stocks.columns = ['amzn', 'aapl', 'goog', 'msft', 'nflx', 'nasdaq']


st.subheader('Manga Stocks Comparison')
st.write(px.line(stocks, title='MANGA Stocks', template='presentation', labels={'value': 'USD'}, height=800, width=1200))
st.title('')
#-------------------------------------------#

selection = st.multiselect('Select stocks to compare', {'AMZN':amzn, 'AAPL':aapl, 'GOOG':goog, 'MSFT':msft, 'NFLX':nflx, 'Nasdaq':nasdaq})

@st.cache_data
def draw(data):
    fig = px.scatter(stocks, trendline="rolling", trendline_options=dict(window=window),
                    title=str(window)+ "  Day moving average")
    fig.data = [t for t in fig.data if t.mode == "lines"]
    fig.update_traces(showlegend=True) #trendlines have showlegend=False by default
    fig.update_layout(height=800, width=1200)
    return st.write(fig)

draw(stocks)
st.title('')
#-------------------------------------------#




st.write('Portfolio', 'https://jodiambra.github.io/')
st.write('LinkedIn', 'https://www.linkedin.com/in/jodiambra/')
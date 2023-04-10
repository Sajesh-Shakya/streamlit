import streamlit as st
import numpy as np
import time
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import streamlit_authenticator as stauth
from datetime import datetime
import database as db #bring all the functions from database into the app

if st.session_state['authentication_status']:
    st.write("""
        # Simple Stock Price APP

        This is showing the stock data for apple
        """)

    st.write("Authentication status", st.session_state['authentication_status'])
    symbols = ["AAPL","GOOG","KO","INTC","SBUX","MSFT","AMZN"]
    ticker = st.selectbox("select a stock to visulize",options=symbols)
    tickerData = yf.Ticker(ticker)
    # yahoo only gives 2020 => use alpha vantage
    # reloading site is long still bruv => st cache
    


    #create timestamp for now
    # just using date_time.now doesnt work, use this in write up
    if "now" not in st.session_state:
        st.session_state['now'] = datetime.now()

    t_range = st.slider("select period of time to view", min_value=datetime(1998,5,31), max_value= st.session_state['now'], value= (datetime(1998,5,31),st.session_state['now']),format="YYYY-MM-DD")
    s = t_range
    # hard to use => so create select box 
    #col1, col2, col3 , col4, col5, col6, col7 = st.columns([1,1,1,1,1,1,5]) #make mistake about not adding col 7
    #month = col1.button("1M")
    #months = col2.button("6M")
    #ytd = col3.button("YTD")
    #year = col4.button("1Y")
    #year_5 = col5.button("5Y")
    #max = col6.button("MAX")

    tickerDf = tickerData.history(period = "1d", start= s[0], end= s[1])

    
    graph = st.selectbox("select a stock to visulize",options=["line chart", "candle_stick"])
    if graph == "line chart":
        close_check = st.checkbox("Close")
        volume_check = st.checkbox("Volume")
        if close_check: 
            st.line_chart(tickerDf.Close)
            #interactive
            #fig = px.line(tickerDf, x = tickerDf.index, y = tickerDf.Close , title = ticker)
            #st.plotly_chart(fig)
        if volume_check: 
            st.line_chart(tickerDf.Volume)
            #interactive
            #fig = px.line(tickerDf, x = tickerDf.index, y = tickerDf.Volume , title = ticker)
            #st.plotly_chart(fig)
    else:
        fig = go.Figure() #  plotly figure object
        fig.add_trace(go.Candlestick(x = tickerDf.index, open=tickerDf.Open, high=tickerDf.High, low=tickerDf.Low, close=tickerDf.Close) )
        st.plotly_chart(fig)
    tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
    # use stocknews API and Alphavantage API
    

else:
    st.write("""
             # Login on the start page to view this page
             """)
    
    
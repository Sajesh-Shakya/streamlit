import streamlit as st
import numpy as np
import time
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import database as db #bring all the functions from database into the app
import requests
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from datetime import date
from datetime import date, timedelta
from tensorflow import keras



if st.session_state['authentication_status']:
    st.write("""
        # predictions using Fbprophet and LSTM model
        """)
    symbols = ["AAPL","GOOG","KO","INTC","SBUX","MSFT","AMZN"]
    ticker = st.selectbox("select a stock to visulize",options=symbols)


    #missing days so use yfinance
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='+str(ticker)+'&outputsize=full&apikey=FL5IQASMYV9TAGZM'
    r = requests.get(url)
    data = r.json()
    d = data["Time Series (Daily)"]
    tickerData = pd.DataFrame.from_dict(d, orient="index")
    tickerData = tickerData[:1200]
    tickerData
    tickerData.reset_index(inplace=True)
    tickerData.rename(columns = {'index':'ds', "4. close": "y"}, inplace= True)
    tickerData = tickerData[["ds","y"]]

    model = st.selectbox("select LSTM or Fbprophet to forecast", options = ["LSTM", "fbprophet"])
    if model == "fbprophet":
        m = Prophet()
        m.fit(tickerData)
        period = st.slider('How many days to predict', 0, 500, 25)
        future = m.make_future_dataframe(periods = period)
        forecast = m.predict(future)
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1)
        st.write(forecast.tail())

        show_components = st.checkbox("show components")
        if show_components:
            fig2 = m.plot_components(forecast)
            st.write(fig2)
    
    
    if model == "LSTM": 
        
        
        period = st.slider('How many days to predict', 0, 100, 25)

        tod = date.today()
        delta = timedelta(days = 18)# exchanges closed on weekends and certain holdays
        n_days_ago = tod - delta

        tick = yf.Ticker(ticker)
        tickdf = tick.history(start= n_days_ago, end = tod)

        X_test = tickdf[["Open", "High", "Low","Close"]].tail(10).to_numpy()
        #takes last 10 records
        #converts to numpy arrays so np commands can be used

        last_x = X_test

        mod_name = ticker+".h5" #make sting as he file name 
        new_model = keras.models.load_model(mod_name)
        validation_predictions=[]

        for x in range(period):
            pred = new_model.predict(last_x.reshape(-1,10,4))[0,0]
            validation_predictions.append(pred)

            last_x = np.roll(last_x, -1)
            last_x[-1] = pred

        st.line_chart(validation_predictions)
        

    
    



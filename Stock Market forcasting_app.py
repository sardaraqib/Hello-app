import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller


#..
app_title= "Forcasting Application for Brands"
st.title(app_title)

st.header("this application is for the forcast the stock market prices of the selected companies")
#add the image from online 
st.image("https://media.istockphoto.com/id/1094465844/photo/business-growth-progress-or-success-concept-businessman-is-drawing-a-growing-virtual-hologram.jpg?s=612x612&w=0&k=20&c=VgRs2Wc75IAC7bkFM_NPcYusYVkhTpWUV7_yeK6eNI0=")


#sidebar
st.sidebar.header("Select the Values from below")

start_date=st.sidebar.date_input("Start date",date(2022,1,1))
end_date=st.sidebar.date_input("End date",date(2023,8,11))

#add the ticker symbol list
ticker_list=['AAPL',"MSFT",'GOOG','META','TESLA','NVDA','ADBE','PYPL','INTC','CMCSA','NFLX','PEP']
ticker=st.sidebar.selectbox("Select the company",ticker_list)

#fetch data from the user 
data=yf.download(ticker,start=start_date ,end=end_date)
#adding date as a coulum to thte dataframe currentyly it is working as index

data.insert(0,'Date',data.index,True)
data.reset_index(drop=True,inplace=True)
st.write("Date From",start_date,'to',end_date)
st.write(data)

#plot of Data with respect to date
st.header("Data Visulization")
st.subheader('Line plot of Data')
fig=px.line(data,x='Date',y=data.columns,title="Closing prices of stocks",width=900,height=600) #using plotyly express
st.plotly_chart(fig)

#geeting colum fro user and  generating graph on it 
col=data.columns[1:] #columns start from 1

st.write ("You can select he specific date range from sidebar and specifc column to generate graph")
columns= st.selectbox('Select the column to Plot',col)
st.write("Selected Column")
New_data=data[['Date',columns]] #only the selected colum will come
st.write(New_data)
fig=px.line(New_data,x='Date',y=columns,title="Closing prices of stocks",width=700,height=600) #using plotyly express
st.plotly_chart(fig)

#ADF test check stationary (means it have any trend)
st.write("Is data is Stationary")
st.write(adfuller(data[columns])[1]<0.05)

#lets decompese the data
st.header('Decomposition of the data')
decomposition=seasonal_decompose(data[columns],model='additive',period=12)
st.write(decomposition.plot())

#makeing same decomposition plot in plotly
st.write("##Ploting the decomposition in Plotly")
st.plotly_chart(px.line(x=data['Date'],y=decomposition.trend,title='Trend',width=800,height=400,labels={'x':'Date','y':'Price'}).update_traces(line_color='Blue'))
st.plotly_chart(px.line(x=data['Date'],y=decomposition.seasonal,title='Seasonality',width=800,height=400,labels={'x':'Date','y':'Price'}).update_traces(line_color='Green'))
st.plotly_chart(px.line(x=data['Date'],y=decomposition.resid,title='Residuals',width=800,height=400,labels={'x':'Date','y':'Price'}).update_traces(line_color='Red' , line_dash='dot'))

#let Run the model
#user input for the three parametes of the model and seasonal order
p=st.slider("Select the value of p",0,5,2)
d=st.slider("Select the value of d",0,5,1)
q=st.slider("Select the value of q",0,5,2)
seaaonal_order=st.number_input('Select the value of seasonal p',0,24,12)

model=sm.tsa.statespace.SARIMAX(data[columns],order=(p,d,q),seasonal_order=(p,d,q,seaaonal_order))
model=model.fit()

#print model Summary
st.header('Model Summary')
st.write(model.summary())
st.write(".............................")

#predict the future forcasting values
st.write("<p style='color:green ; font-size: 50px ; font-weight:bold;'>Forecasting the data</p>",unsafe_allow_html=True)
forecast_period=st.number_input("Select the number of days to forecast",1,365,10)
#predict the future values
prediction=model.get_prediction(start=len(data),end=len(data)+forecast_period)
prediction=prediction.predicted_mean
#st.write(prediction)

#add the index to the prediction 
prediction.index=pd.date_range(start=end_date,periods=len(prediction),freq='D')
prediction=pd.DataFrame(prediction)
prediction.insert(0,'Date',prediction.index,True)
prediction.reset_index(drop=True,inplace=True)
st.write("Predictions",prediction)
st.write("Actual Data",New_data)

#lets plot the data
fig= go.Figure()

#add actucal data to plot
fig.add_trace(go.Scatter(x=data["Date"],y=data[columns],mode='lines',name='Actual',line=dict(color='blue')))
#add predicted data to the plot
fig.add_trace(go.Scatter(x=prediction["Date"],y=prediction["predicted_mean"],mode='lines',name='Predicted',line=dict(color='red')))
#set the title and axis labels
fig.update_layout(title='Actual vs Predicted',xaxis_title="Date", yaxis_title='Price',width=1000,height=600)
#display the plot
st.plotly_chart(fig)

#adding button for the plots
show_plots=False
if st.button("Show seperate Plots"):
    if not show_plots:
        st.write(px.line(x=data['Date'],y=data[columns], title='Actual',width=1200,height=400,labels={'x':'Date','y':'Price'}).update_traces(line_color='Yellow'))
        st.write(px.line(x=prediction['Date'],y=prediction["predicted_mean"], title='Predicted',width=1200,height=400,labels={'x':'Date','y':'Price'}))
        show_plots= True
    else:
        show_plots= False
  
hide_plots= False
if st.button("Hide Seperate Plots"):
    if not hide_plots:
        hide_plots=True
    else:
      hide_plots= False

st.write("---------------")

#st.header (" This application is Developed By Aqib Ali ")
#st.write("<p style='color:Yellow ; font-size: 50px ; font-weight:bold;'>This application is Developed By Aqib Ali </p>",unsafe_allow_html=True)
html_code = """
<div style="text-align: center;">
<p style='color:Grey; font-size: 50px; font-weight:bold;'>
This application is Developed By Aqib Ali
</p>  
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)
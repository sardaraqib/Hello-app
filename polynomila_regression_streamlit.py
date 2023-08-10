
#another example :
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

header=st.container()
datasets=st.container()
training=st.container()
linear_Regressio=st.container()
poly_regressio=st.container()
Predictions=st.container()
with header:
    st.title("Polynomial Regression Application")

with datasets:
 df=pd.read_csv('https://s3-us-west-2.amazonaws.com/public.gamelab.fun/dataset/position_salaries.csv')
 st.write(df.head())
 X=df.iloc[:, 1:2].values
 y=df.iloc[ : , 2].values
 st.write(X)

with training:
 from sklearn.model_selection import train_test_split
 X_train,X_test, Y_train, Y_test=train_test_split(X,y,test_size=0.2,random_state=0)

with linear_Regressio:
  from sklearn.linear_model import LinearRegression
  line_reg=LinearRegression()
  line_reg.fit(X,y)
  #visulization of data
  def viz_liner():
   fig,ax=plt.subplots()
   ax.scatter(X,y,color='red')
   ax.plot(X,line_reg.predict(X),color='Blue')
   ax.set_title('Truth or Bluff (liner Regression)')
   ax.set_xlabel('Position level')
   return fig
st.write(viz_liner()) 
  
st.subheader("Ploting the  Poly_regression line")

with poly_regressio:
  from sklearn.preprocessing import PolynomialFeatures
  poly_regression=PolynomialFeatures(degree=4) #mean x ki power
  X_poly=poly_regression.fit_transform(X)
  pol_regression=LinearRegression()
  pol_regression.fit(X_poly,y)
  def viz_liner():
   fig,ax=plt.subplots()
   ax.scatter(X,y,color='red')
   ax.plot(X,pol_regression.predict(poly_regression.fit_transform(X)),color='Blue')
   ax.set_title('Truth or Bluff (liner Regression)')
   ax.set_xlabel('Position level')
   return fig
st.write(viz_liner()) 

with Predictions:
  predict_liner=line_reg.predict([[11]])

precit_poly=pol_regression.predict(poly_regression.fit_transform([[11]]))
st.subheader("Prediction on linear")
st.write("Linear Regression :",predict_liner)
st.subheader("Prediction on POLY_regressioSn")
st.write("Poly regression:",precit_poly)
st.write ("Defference is :",predict_liner-precit_poly)
import streamlit as st
import pickle
import numpy as np
import pandas as pd
# import the model
df=pickle.load(open('df.pkl','rb'))    # df is a object created by the-serialisation process.
pipe=pickle.load(open('pipe.pkl','rb')) # pipe is a object created by the-serialisation process.

st.title("Laptop Price Predictor")

# dropdown for laptop brand
brand = st.selectbox('Brand',df['Company'].unique()) ## all unique categories of Company column will be fetched out as the dropdown

# dropdown for type of laptop
type = st.selectbox('Type',df['TypeName'].unique())

# Ram
ram=st.selectbox('Ram (in GB)',[2,4,6,8,12,16,24,32,64])

# Weight
weight=st.number_input('Weight of Laptop (in Kg)')

# touchscreen
touchscreen=st.selectbox('Touchscreen',['No','Yes'])

# IPS
ips=st.selectbox('IPS',['No','Yes'])

# to cal ppi take input screen size and screen resolution
# screen size

size=st.number_input('Screen Size (in Inches)')
# screen resolution
resolution=st.selectbox('Screen resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

# cpu brand
cpu=st.selectbox('Cpu',df['Cpu Brand'].unique())

# hard drive
hdd=st.selectbox('HDD (in GB)',[0,32,128,500,1000,2000])

# ssd
ssd=st.selectbox('SSD (in GB)',[ 0,8,16,32,64,128,180,240,256,512,768,1000, 1024])

# gpu brand
gpu=st.selectbox('Gpu',df['Gpu Brand'].unique())

# os
os=st.selectbox('Operating System',df['os'].unique())

# creating a button
# when user will press this button this function will be executed
if st.button('Predict Price'):

    ## input query (collecting all inputs)
    if touchscreen == 'Yes':
        touchscreen=1
    else:
        touchscreen=0
    if ips=='Yes':
        ips=1
    else:
        ips=0


    # calculating ppi by the input of screen size and resolution
    # resolution is taken as a string so, convert it into int for performing mathematical calculations.
    x_reso=int(resolution.split('x')[0])
    y_reso = int(resolution.split('x')[1])
    
    try:
        ppi = ((x_reso ** 2) + (y_reso ** 2) ** 0.5) / size
    except ZeroDivisionError:
        print("Do not Enter Size as Zero") 

    query = np.array([brand, type, ram, weight, touchscreen, ips, ppi, cpu, hdd, ssd, gpu, os])
    # reshaping query (n-d array)
    # as there are 12 columns (as input) with 1 row
    query=query.reshape(1,12)

    ## passing this input to pipe object
    ## predict() of pipe object will make prediction for this input(query).
    ## since we have applied the log transformation on output column , so now to predict the exact value we should the reverse
    ## of log operation i.e exponential of this predicted value.
    result = int(np.exp(pipe.predict(query))[0] ) # since it is in array, so to get value without brackets I should write 0th index value of array
    st.title("The Predicted Price of this Configuration is "+str(result))


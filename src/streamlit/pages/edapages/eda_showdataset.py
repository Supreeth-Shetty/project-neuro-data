import numpy as np
import pandas as pd
import os
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
#import excelpage
# @st.cache

#from DataTransfer.src.resource import *


@st.cache
def load_data():
    try:
        
        df=pd.read_csv('data/train.csv')
        lowercase = lambda x: str(x).lower()
        df.rename(lowercase, axis='columns', inplace=True)
        # if 'data' not in st.session_state:
        #     st.session_state['data'] = df
        return df
        
    except Exception as e:
        print(e)
    finally:
        pass
    
def app():
    df=load_data()
    st.header('*Your Dataset*')
    st.markdown("Filter Your Result")
    form = st.form(key='my-form')
    count = form.slider('No of records to show', min_value=1, max_value=len(df), value=5, step=5)
    order = form.radio("Select order", options=["Show Top Rows", "Show Bottom Row"], help="Select do you wanna dsiplay rows from top or bottom")
    submit = form.form_submit_button('Show')
    
    df_show=df
    
    if order=="Show Top Rows":
        df_show=df_show.head(count)
    else:
        df_show=df_show.tail(count)
        
    
    st.write(df_show)

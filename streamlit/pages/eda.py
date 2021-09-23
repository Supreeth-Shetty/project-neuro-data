# Import necessary libraries
import json
import joblib

import pandas as pd
import streamlit as st
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import os
def app():

    # Load the data 
    if 'main_data.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` option!")
    else:
        data_file = pd.read_csv('data/main_data.csv')
        df=data_file
        # Option to select EDA type
        eda_type = st.sidebar.radio("Select the type of EDA you want to run.", options=["Exploratory Data analysis", "Data Preprocessing","Feature Engineering"], help="Write about EDA")

        if eda_type == "Exploratory Data analysis":
            html_temp3 = """
            <div style="background-color:#98AFC7;padding:10px">
            <h4 style="color:white;text-align:center;">Upload file Your file in csv formate and perform Exploratory Data Analysis</h4>
            <h5 style="color:white;text-align:center;">Make sure your columns have correct data types before uploading.</h5>
            </div><br></br>"""
            st.markdown(html_temp3, unsafe_allow_html=True)
            st.subheader("Perform Exploratory data Analysis with Pandas Profiling Library, Click on Analyze button for EDA")
            #########################EDA Logic########################
            #data_file=pd.read_csv("data/main_data.csv")
            #df=data_file
            if st.button("Analyze"):
                if data_file is not None:
                    # Pandas Profiling Report
                    #df=data_file
                    pr = ProfileReport(df, explorative=True)
                    st.header('*User Input DataFrame*')
                    st.write(df)
                    st.write('---')
                    st.header('*Exploratory Data Analysis Report Using Pandas Profiling*')
                    st_profile_report(pr)
                else:
                    st.success("Upload file")


            #########################End EDA Logic###########
        if eda_type=="Data Preprocessing":
            st.write("Data Preprocessing options")
            df = pd.read_csv('data/main_data.csv')
            dp_type=st.sidebar.radio("Select the type for Data Preprocessing", options=["Data Cleaning", "Data Integration","Data Reduction","Data Transformation"],help="Write about Data Preprocessing")
            if dp_type == "Data Cleaning":
                st.write("Data Cleaning.....")
                percent_missing = round((df.isnull().sum() * 100/ len(df)),2).sort_values(ascending=False)
                st.write("Missing Percentage",percent_missing)
                #missing_value_df = pd.DataFrame({'column_name': df.columns,'percent_missing': percent_missing})
                #missing_value_df=missing_value_df.sort_values('percent_missing', inplace=True)
                #st.write("Missing Value ",missing_value_df)
                st.write("in our columns we have 95% of missing values user should drop this column")
                if st.button("Drop"):
                   st.write("Dropping Column")
                   missing_features = percent_missing[percent_missing > 0.95].index
                   df.drop(missing_features, axis=1, inplace=True)
                   st.write(df)
                else:
                    st.write("Not having missing value in column that can drop")


            if dp_type == "Data Integration":
                st.write("Data Integration")
            if dp_type == "Data Reduction":
                st.write("Data Reducation")
            if dp_type == "Data Transformation":
                st.write("Data Transformation")

        if eda_type == "Feature Engineering":
            fe_type = st.sidebar.radio("Select the type for feature engg.", options=["Handling Imbalanced data", "Handling categorical data"], help="Write about Feature Engg.")
            if fe_type=="Handling Imbalanced data":
                st.write("Handling Imbalanced data")
            if fe_type=="Handling categorical data":
                st.write("Handling categorical data")

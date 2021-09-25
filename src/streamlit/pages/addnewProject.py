import streamlit as st
import pandas as pd
from pathlib import Path
import sqlite3
from sqlite3 import Connection
from . import excelpage,dashboard
from .resource import *
from multipage import MultiPage
import numpy as np
import pandas as pd
#import excelpage
app1 = MultiPage()
# @st.cache
def app():
    st.markdown("Add New Project")
    project_name = st.text_input("Project Name")
    project_desc = st.text_area("Description")
    st.write("\n")
    app_mode_sr1 = st.selectbox("Upload Datasource from file", SOURCE1)
    if app_mode_sr1 == "Excel File":
        uploaded_file = st.file_uploader("Choose a file", type=['xlsx'])
        if uploaded_file is not None:
            if uploaded_file.name.endswith("xlsx"):
                app1.add_page("Execl", excelpage.app())
    app_mode_sr2 = st.selectbox("Upload Dataset From Other Resource", SOURCE2)
    if app_mode_sr2 == "POSTGRESQL":
        st.selectbox("Select DB for Sources 1", SOURCEDB2)

    #if bt=="Create New Project":
     #   app1.add_page("Dashboard",dashboard.app())
    URI_SQLITE_DB = "data/dashboard.db"
    #@st.cache(hash_funcs={Connection: id})
    conn=sqlite3.connect(URI_SQLITE_DB)
    database=conn.cursor()
    database.execute('CREATE TABLE IF NOT EXISTS dashboard(Project_Name TEXT, Project_Desc TEXT,Project_Type TEXT)')
    conn.commit()
    if st.button("Create New Project",key="bt1"):
        conn.execute('INSERT INTO dashboard (Project_Name, Project_Desc,Project_Type) VALUES (?,?,?)',(project_name,project_desc,app_mode_sr1))
        conn.commit()
        #app1.add_page("Dashboard",dashboard.app())
        #df = pd.read_sql("SELECT * FROM dashboard", con=conn)
        #st.dataframe(df)
        conn.close()
        if conn.Error==False:
            st.markdown("Project Created Successfully, go to Dashboard")





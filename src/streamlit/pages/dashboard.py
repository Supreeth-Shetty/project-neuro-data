import pandas as pd
import streamlit as st
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

#from DataTransfer.src.resource import *


def app():
    st.markdown("Welcome to Dashboard")
    st.markdown("My Projects")
    URI_SQLITE_DB = "data/dashboard.db"
    # @st.cache(hash_funcs={Connection: id})
    conn = sqlite3.connect(URI_SQLITE_DB)
    database = conn.cursor()
    df = pd.read_sql("SELECT * FROM dashboard", con=conn)
    bt=st.button("Continue")
    st.dataframe(df)
    conn.close()




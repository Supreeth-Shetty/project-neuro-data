import os
import streamlit as st
import numpy as np
from PIL import  Image
import pandas as pd

# Custom imports 
from multipage import MultiPage
from pages import addnewProject,dashboard,eda,datapreprocessing,featureengineering
# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
#####################pages################################
app.add_page("EDA", eda.app)
app.add_page("Data Preprocessing", datapreprocessing.app)
app.add_page("Feature Engineering", featureengineering.app)

###################End Pages#######################

# The main app
app.run()

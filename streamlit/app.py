import os
import streamlit as st
import numpy as np
from PIL import  Image
import pandas as pd

# Custom imports 
from multipage import MultiPage
from pages import addnewProject,dashboard,eda
# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
#display = Image.open('Logo1.png')
#display = np.array(display)
# st.image(display, width = 400)
# st.title("Data Storyteller Application")
#col1, col2 = st.columns(2)
#col1.image(display, width = 300)
#col2.title("Test")
#####################pages################################
app.add_page("Add New Project", addnewProject.app)
app.add_page("Dashboard", dashboard.app)
app.add_page("EDA", eda.app)

###################End Pages#######################

# The main app
app.run()

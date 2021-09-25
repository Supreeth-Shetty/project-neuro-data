import os
import streamlit as st
import numpy as np
from PIL import  Image
import pandas as pd

# Custom imports 
from pages.multipage import MultiPage
from pages.edapages import about
# import your pages here

# Create an instance of the app 
app = MultiPage()

# Title of the main page
#####################pages################################
app.add_page("About", about.app)

###################End Pages#######################

# The main app
app.run()

import os
import streamlit as st
import numpy as np
from PIL import  Image
import pandas as pd

# Custom imports 
from pages.multipage import MultiPage
from pages.edapages import about,pandasprofiler,eda_script,eda_outlier,eda_5pointsummary,eda_correlation,eda_showdataset
# import your pages here

# Create an instance of the app 
def app():
    local = MultiPage("Select Option")

    # Title of the main page
    #####################pages################################
    local.add_page("Help", about.app)
    local.add_page("Pandas Profiler", pandasprofiler.app)
    local.add_page("Show Dataset", eda_showdataset.app)
    local.add_page("Correlation Report", eda_correlation.app)
    local.add_page("Outlier Report", eda_outlier.app)
    local.add_page("Custom Script", eda_script.app)

    ###################End Pages#######################

    # The main app
    local.run()

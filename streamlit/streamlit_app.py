import streamlit as st
from src.resource import *
from multipage import MultiPage
from pages import dbconnect
app = MultiPage()

st.sidebar.title(SIDEBAR_TITLE)
st.markdown("Add New Project")
st.text_input("Project Name")
st.text_area("Description")
st.write("\n")

app_mode_sr1 = st.selectbox("Upload Datasource from file", SOURCE1)
app_mode_sr2 = st.selectbox("Upload Dataset From Other Resource", SOURCE2)

if app_mode_sr1=="MySQL":
    app.add_page("Upload Data", dbconnect.app)
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
if app_mode_sr2 == "POSTGRESQL":
    st.selectbox("Select DB for Sources 1", SOURCEDB2)
    st.write("Click on Button to connect with DB of Source 2")
    st.button("ConnectionSrc2")


app.run()

#def run_app():
 #   st.title("Transfer Data from Sources to Destination")

#if __name__ == "__main__":
    #main()

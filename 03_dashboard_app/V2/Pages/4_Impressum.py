import streamlit as st
import altair as alt
import pandas as pd


st.set_page_config(
    page_title="Impressum",
    page_icon = ":hearts:",
    layout="wide",
    menu_items={
        'Report a bug': "mailto:haanhhanoitran@gmail.com",
        'About': "Eine App hergestellt für die Visualisierung von Hypertonie Daten \n"
                 "Autor: Ludmila Janzen, Mahshid Ghasempour, Ha Anh Tran"
    }
)


st.title("Impressum")
st.header("Herausgeber")
st.subheader("Mahshid Ghasempour ")
st.write("Email: Ghasem.mahshid71@gmail.com")
st.subheader("Ludmila Janzen")
st.write("Email: ludmila.janzen@tu-dortmund.de")
st.subheader("Ha Anh Tran")
st.write("Email: haanhhanoitran@gmail.com")

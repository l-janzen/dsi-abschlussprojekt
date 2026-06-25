#ist dafür da, damit ich die App schnell auf Windows oder Mac öffne
#cd C:\Users\haanh\.vscode\DSI_Abschlussprojekt\dsi-abschlussprojekt
#streamlit run .\03_dashboard_app\V2\Streamlit_Hypertonie_V2.py
#streamlit run "/Users/haanhtran/Documents/Python/dsi-abschlussprojekt/03_dashboard_app/V2/Streamlit_Hypertonie_V2.py"



#docs.streamlit.io
#https://docs.streamlit.io/develop/quick-reference/cheat-sheet
#framework
import warnings
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from streamlit_javascript import st_javascript

BASE_DIR = Path(__file__).resolve().parent



#Name der App, Stil, Menu Leiste
st.set_page_config(
    page_title="Startseite",
    page_icon=":hearts:",
    layout="wide",
    menu_items={
        'Report a bug': "mailto:haanhhanoitran@gmail.com",
        'About': "Eine App hergestellt für die Visualisierung von Hypertonie Daten \n"
                 "Autor: Ludmila Janzen, Mahshid Ghasempour, Ha Anh Tran"
    }
)


#Überschrift
st.title("Risiko auf Hypertonie")
c1,c2 = st.columns([1,1])
theme = st_javascript("""
window.matchMedia('(prefers-color-scheme: dark)').matches
""")
if theme:
    with c1:
        st.image(str(BASE_DIR / "Image" / "ChatGPT Image 20. Juni 2026, 23_10_12.png"))
    
else:
    with c1:
        st.image(str(BASE_DIR / "Image" / "ChatGPT Image 20. Juni 2026, 23_10_17.png"))




st.subheader(":woman_health_worker: :man_health_worker: Informationen zur App ")
st.write(
    "Diese App dient dazu, das Bewusstsein für die hohe Verbreitung von Hypertonie (Bluthochdruck) zu"
    "stärken und das individuelle Risiko bzw. den Grad einer möglichen Hypertonie einzuschätzen.\n"
    "Darüber hinaus werden verschiedene Risikofaktoren untersucht, um deren "
    "Zusammenhang mit einem erhöhten Hypertonierisiko zu analysieren."
)
st.caption("Im Rahmen dieser Anwendung wird primär die arterielle Hypertonie betrachtet.")
st.subheader("Was ist Hypertonie?")
st.write(
    "Die arterielle Hypertonie, oft verkürzt auch Hypertonie (von altgriechisch ὑπέρ hyper ‚über(mäßig)‘"
    "und τείνειν teinein ‚spannen‘),[1] Hypertonus, Hypertension oder im täglichen"
    " Sprachgebrauch Bluthochdruck genannt, ist ein Krankheitsbild,"
    "bei dem der Blutdruck des arteriellen Gefäßsystems chronisch erhöht ist. Nach Definition der "
    "WHO gilt beim erwachsenen Menschen ein systolischer Blutdruck von"
    "mehr als 140 mmHg oder ein diastolischer Blutdruck von mehr als 90 mmHg als Hypertonie. Nicht in dieser Definition"
    "eingeschlossen sind vorübergehende Blutdruckerhöhungen durch Erkrankung, Medikamente, Schwangerschaft oder bei körperlicher"
    "Anstrengung."
    "\n Quelle : https://www.stiftung-gesundheitswissen.de/hypertonie/allgemeines"
)

st.subheader("Was sind die Nachteile von Hypertonie?")

st.subheader("Wie ist Diagnose?")




st.page_link(
    "Pages/1_Zeitreihenanalyse.py",
    label="Zeitreihenanalyse",
    icon="🏠"
)

plumb = st.button(label="page 2")
if plumb == True:
    st.page_link("Pages/2_Risikofaktoren.py", label="Page 1", icon="1️⃣")

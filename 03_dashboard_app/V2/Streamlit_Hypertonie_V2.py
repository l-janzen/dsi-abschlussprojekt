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




st.header(":woman_health_worker: :man_health_worker: Informationen zur App ")
st.write(
    "Diese App dient dazu, das Bewusstsein für die hohe Verbreitung von Hypertonie (Bluthochdruck) zu"
    "stärken und das individuelle Risiko bzw. den Grad einer möglichen Hypertonie einzuschätzen.\n"
    "Darüber hinaus werden verschiedene Risikofaktoren untersucht, um deren "
    "Zusammenhang mit einem erhöhten Hypertonierisiko zu analysieren."
)
st.caption("Im Rahmen dieser Anwendung wird primär die arterielle Hypertonie betrachtet.")
st.header("Was ist Hypertonie?")
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

st.header("Wie wird der Blutdruck gemessen?")
st.write("Der Blutdruck wird in Millimeter Quecksilbersäule, kurz mmHg, gemessen. Dabei sind zwei Werte interessant: der obere oder systolische Wert und der untere, der diastolische Wert.")


st.write("Der obere Blutdruckwert wird gemessen, während sich das Herz zusammenzieht und Blut in die Arterien pumpt. Der untere Wert wird gemessen, während sich das Herz entspannt und wieder mit Blut füllt. In der Entspannungsphase strömt kein Blut vom Herzen in die Arterien. Deshalb ist der untere Blutdruckwert auch immer niedriger als der obere.")

spalte_m, spalte_k,gff = st.columns([2,4,1])
with spalte_m:
    st.image(BASE_DIR  /"Image" /"2023_11_29_Blutdruckmessgerät_v1TS.png.webp")

with spalte_k:
    st.write(
    "Man spricht beim Erwachsenen von Hypertonie, wenn")
    st.write(
    "- der obere (systolische) Blutdruck im Ruhezustand bei 140 mmHg oder höher liegt und/oder")
    st.write(
    "- der untere (diastolische) Blutdruck im Ruhezustand bei 90 mmHg oder höher liegt.")
    st.write(
    "Umgangssprachlich werden bei Blutdruckangaben beide Werte kurz als Verhältnis zusammengefasst. Man sagt zum Beispiel: „Der Blutdruck ist 140 zu 90.“ Zur schriftlichen Dokumentation des Blutdrucks wird in der Regel die Kurzform „140/90 mmHg“ verwendet.")

st.subheader("Wie verläuft Bluthochdruck ohne Behandlung?")
st.write("Bei Bluthochdruck muss das Herz das Blut mit mehr Anstrengung in die Blutgefäße pumpen. Dies kann negative gesundheitliche Folgen auslösen. Ein dauerhaft erhöhter Blutdruck schädigt die Blutgefäße und fördert das Entstehen von Herz-Kreislauf-Erkrankungen. ")
spalte_l, spalte_e,gsdfff = st.columns([2,4,1])
with spalte_l:
    st.image(BASE_DIR  /"Image" /"Hypertonie_Folgeerkrankungen_online.png.webp")

with spalte_e:
    st.write("Durch den zu hohen Blutdruck können verschiedene Organe Schaden nehmen. Mögliche Folgen von Hypertonie sind:")
    st.write("- Herzinfarkte")
    st.write("- Herzinfarkte")
    st.write("- Schlaganfall")
    st.write("- Nierenschwäche")
    st.write("- Durchblutungsstörungen in den Beinen")
    st.caption("Die nebenstehende Grafik fasst wesentliche Folgeerkrankungen von Bluthochdruck zusammen. ")


 




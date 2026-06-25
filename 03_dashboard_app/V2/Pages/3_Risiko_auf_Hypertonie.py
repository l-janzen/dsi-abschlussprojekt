import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import warnings
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import  OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score,precision_recall_curve,roc_auc_score
from sklearn.metrics import ConfusionMatrixDisplay





st.set_page_config(
    page_title="Risiko auf Hypertonie",
    page_icon = ":hearts:",
    layout="wide",
    menu_items={
        'Report a bug': "mailto:haanhhanoitran@gmail.com",
        'About': "Eine App hergestellt für die Visualisierung von Hypertonie Daten \n"
                 "Autor: Ludmila Janzen, Mahshid Ghasempour, Ha Anh Tran"
    }
)

st.title("Hypertonie-Screening: Risikoeinschätzung")
st.header(":hearts: Informationen zur Seite")
st.write("Die Auswahl dieser Faktoren basiert auf den verfügbaren NHANES-Daten und ihrer fachlichen Relevanz für die Risikoeinschätzung. Die Anwendung dient als Screening-Hinweis und ersetzt keine ärztliche Diagnose oder Blutdruckmessung.")


st.header("Fragebogen")
st.subheader("Hier können Sie anhand ihrer Daten ihr Risiko berechnen lassen.")
st.write("Geben Sie einige Gesundheits- und Lebensstilfaktoren ein. Das Modell schätzt anschließend die Wahrscheinlichkeit für Hypertonie. ")
def Alkoholpegel():
    if st.session_state.alkohol == "Keinen Konsum":
        st.session_state.pumpen = 0

    elif st.session_state.alkohol == "Geringer Konsum":
        st.session_state.pumpen = 33

    elif st.session_state.alkohol == "Mittlerer Konsum":
        st.session_state.pumpen = 66

    elif st.session_state.alkohol == "Hoher Konsum":
        st.session_state.pumpen = 90

def spass():
    if st.session_state.pumpen == 0:
        st.session_state.alkohol = "Keinen Konsum"
    elif st.session_state.pumpen <= 33:
        st.session_state.alkohol = "Geringer Konsum"
    elif st.session_state.pumpen <= 66:
        st.session_state.alkohol = "Mittlerer Konsum"
    elif st.session_state.pumpen <= 100 :
        st.session_state.alkohol = "Hoher Konsum"



spalte_1, spalte_2, spalte_3 = st.columns([1,1,1])

with spalte_1:
    alter = st.number_input(
        "Alter",
        key="alter",
        placeholder="Gebe eine Zahl ein ...",
        min_value = 0,
        max_value = 115,
        step=1
    )

    st.write(f"Alter: {st.session_state.alter}")

    rauchen = st.selectbox(
        "Rauchen",
        ("Ja", "Nein"),
        placeholder = "Wähle eine Option aus ...",
        key = "rauchen"
    )

    st.write("You selected:", rauchen)

with spalte_2:
    st.session_state.sex = st.selectbox(
        "Geschlecht",
        ("männlich", "weiblilch"),
        placeholder = "Wähle ein Geschlecht aus ..."
    )

    st.write("You selected:", st.session_state.sex)

    alkohol = st.selectbox(
        "Alkoholkonsum",
        ("Keinen Konsum", "Geringer Konsum", "Mittlerer Konsum", "Hoher Konsum"),
        key = "alkohol",
        on_change = Alkoholpegel
    )
    pumpen = st.slider("Alkoholkonsum", min_value = 0, max_value = 100, value = 100,
                       on_change= spass,
                        key = "pumpen"
                        )

    st.write("You selected:", st.session_state.alkohol, st.session_state.pumpen)

    if st.session_state.pumpen == 0:
        st.write(":milk_glass:")
    else:
        lala = st.session_state.pumpen / 10 + 1
        st.write(int(lala) * ":beer:" )


with spalte_3:
    BMI = st.number_input("BMI", value=None, placeholder="Gebe eine Zahl ein ...",
                             key = "BMI",
                             disabled=False)

    st.write("The current number is ", st.session_state.BMI)

    st.slider("körperlicher Aktivität", min_value = 0, max_value = 100, value = 100)

st.write("Vorerkrankung")
check_diabetis = st.checkbox("Diabetis")
check_niere = st.checkbox("Nierenerkrankung")
check_chol = st.checkbox("Hohes Cholesterin")
check_smoke = st.checkbox("Rauchen")

active = st.selectbox(
        "AKtivitätsniveau",
        ("nicht aktiv", "moderat aktiv", "intensiv aktiv"))

sit = st.slider("Sitzdauer", min_value = 1, max_value = 24, value = 23,
                        key = "sitting"
                        )


with st.form("my_form"):
    st.write(st.session_state)
    submitted = st.form_submit_button("Submit")





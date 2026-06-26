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

import joblib

BASE_DIR = Path(__file__).resolve().parents[3]

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



#################################
#Daten werden geladen
#@st.cache_data
#def load_data():
#    data_path = BASE_DIR / "02_ml_analysis" / "notebooks" / "nhanes_cleand.csv"
#    return  pd.read_csv(data_path
#    )

#data_nhanes = load_data()
#df = data_nhanes.copy()

#df['gender'] = df['gender'].replace({
#    'Male' : '1',
#    'Female' : '2'
#})

#df['gender'] = pd.to_numeric(df['gender'], errors= 'coerce')

@st.cache_resource
def load_model():
    return joblib.load("log_model.pkl")

try:
    log_model = load_model()
except FileNotFoundError:
    # Nur wenn kein Modell vorhanden ist, trainieren
    ############################################
    #Hier fängt der ML teil an

    #feature and target
    #features 
    X = df[
        [
            "age",
            "gender",
            "bmi",
            "high_cholesterol",
            "waist_circumference(cm)",
            "sitting_hours_per_day",
            "current_smoker",
            "regular_alcohol_12m",
            "diabetes",
            "kidney_disease",
            "activity_level"
            
        ]
    ]


    #Target 
    y = df["hypertension"]


    # Train-Test-Split 
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    #Modelltraining  nach Klasse logistische Regression 
    # daten standardisiert
    log_model = Pipeline ([
        ('scaler', StandardScaler()),
        ('model', LogisticRegression(max_iter= 1000,
                                    class_weight= 'balanced'))
    ])

    #model trainieren 
    log_model.fit(X_train, y_train)


label = [
        "age",
        "gender",
        "bmi",
        "high_cholesterol",
        "waist_circumference(cm)",
        "sitting_hours_per_day",
        "current_smoker",
        "regular_alcohol_12m",
        "diabetes",
        "kidney_disease",
        "activity_level"
    ]

test_list = [50, 1, 23, 1, 95, 10, 1, 1, 1, 1, 2]

test_dict = dict(zip(label, test_list))

input_data = pd.DataFrame([test_dict])

# Entscheidungsschwellenwert
threshold = 0.4
# Wahrscheinlichkeit für Hypertonie berechnen
proba_hypertension = log_model.predict_proba(input_data)[:, 1][0]






#############################################################





st.title("Hypertonie-Screening: Risikoeinschätzung")
st.header(":hearts: Informationen zur Seite")
st.write("Die Auswahl dieser Faktoren basiert auf den verfügbaren NHANES-Daten und ihrer fachlichen Relevanz für die Risikoeinschätzung. Die Anwendung dient als Screening-Hinweis und ersetzt keine ärztliche Diagnose oder Blutdruckmessung.")


st.header("Fragebogen")
st.subheader("Hier können Sie anhand ihrer Daten ihr Risiko berechnen lassen.")
st.write("Geben Sie einige Gesundheits- und Lebensstilfaktoren ein. Das Modell schätzt anschließend die Wahrscheinlichkeit für Hypertonie. ")



#########################################################
#on changee Funktion
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


def update_slider():
    mapping = {
        "nicht aktiv": 5,
        "moderat aktiv": 40,
        "intensiv aktiv": 70,
    }

def update_selectbox():
    value = st.session_state.activity_slider

    if value < 15:
        st.session_state.active = "nicht aktiv"
    elif value < 60:
        st.session_state.active = "moderat aktiv"
    else:
        st.session_state.active = "intensiv aktiv"


################################################################
person_dict = {}

st.write("#### Körper")
spalte_1, spalte_2, spalte_3, spalte_4 = st.columns([1,1,1,1])
st.write("#### Lebensstil")
spalte_5, spalte_6, spalte_7, spalte_8 = st.columns([1,1,1,1])
st.write("#### Vorerkrankung")
spalte_a, spalte_s, spalte_d, spalte_f = st.columns([1,1,1,1])


with spalte_1:
    alter = st.number_input(
        "Alter",
        key="alter",
        placeholder="Gebe eine Zahl ein ...",
        value=50,
        min_value = 0,
        max_value = 115,
        step=1
    )

    st.write(f"Alter: {st.session_state.alter} Jahre")

    person_dict["age"] = st.session_state.alter


    

with spalte_2:
    st.session_state.sex = st.selectbox(
        "Geschlecht",
        ("männlich", "weiblilch"),
        placeholder = "Wähle ein Geschlecht aus ..."
    )

    st.write("Geschlecht:", st.session_state.sex)
    if st.session_state.sex == "männlich":
        person_dict["gender"] = 1
    else:
        person_dict["gender"] = 2



with spalte_3:
    BMI = st.number_input("Body-Mass-Index (BMI)",  
        key = "BMI",
        disabled=False,
        value=20,
        min_value = 5,
        max_value = 60,
        step=1
    )

    st.write("BMI:", st.session_state.BMI)
    person_dict["bmi"] = st.session_state.BMI



with spalte_4:
    waist = st.number_input(
        "Taillenumfang (cm)",  
        key = "waist",
        disabled=False,
        value=88,
        min_value = 20,
        max_value = 180,
        step=1)

    st.write("Taillenumfang:", st.session_state.waist, "cm")
    person_dict["waist_circumference(cm)"] = st.session_state.waist



with spalte_5:
    
    rauchen = st.selectbox(
        "Aktueller Rauchstatus",
        ("Ja", "Nein"),
        placeholder = "Wähle eine Option aus ...",
        key = "rauchen"
    )
    st.write("Rauchen:", rauchen)
    if rauchen == "Ja":
        person_dict["current_smoker"] = 1
    else:
        person_dict["current_smoker"] = 0



with spalte_6:
    alkohol = st.selectbox(
        "Alkoholkonsum in den letzten 12 Monate",
        ("Keinen Konsum", "Geringer Konsum", "Mittlerer Konsum", "Hoher Konsum"),
        key = "alkohol",
        on_change = Alkoholpegel
    )
    pumpen = st.slider("Alkoholkonsum", min_value = 0, max_value = 100, value = 100,
                       on_change= spass,
                        key = "pumpen"
                        )

    st.write("Alkoholkonsum:", st.session_state.alkohol, st.session_state.pumpen)

    if st.session_state.pumpen == 0:
        st.write(":milk_glass:")
    else:
        lala = st.session_state.pumpen / 10 + 1
        st.write(int(lala) * ":beer:" )
    if st.session_state.pumpen > 5:
        person_dict["regular_alcohol_12m"] = 1
    else:
        person_dict["regular_alcohol_12m"] = 0



with spalte_7:
    st.selectbox(
        "Aktivitätsniveau",
        ("nicht aktiv", "moderat aktiv", "intensiv aktiv"),
        key="active",
        on_change=update_slider
    )

    st.slider(
        "Körperliche Aktivität",
        min_value=0,
        max_value=100,
        key="activity_slider",
        on_change=update_selectbox
    )
    st.write("Aktivitätsniveau:",st.session_state.activity_slider, st.session_state.active)
    if st.session_state.active == "nicht aktiv":
        person_dict["activity_level"] = 0
    elif st.session_state.active =="moderat aktiv":
        person_dict["activity_level"] = 1
    else:
        person_dict["activity_level"] = 2



with spalte_8:
    sitting = st.slider("Sitzdauer pro Tag", min_value = 1, max_value = 24, value = 23,
                        key = "sitting"
                        )
    st.write("Sitzdauer pro Stunde:", st.session_state.sitting)
    person_dict["sitting_hours_per_day"] = st.session_state.sitting




with spalte_a:
    with st.container(border=True):
        check_diabetis = st.checkbox("Diabetis")
        if check_diabetis:
            person_dict["diabetes"]=1
        else:
            person_dict["diabetes"]=0

with spalte_s:
    with st.container(border=True):
        check_niere = st.checkbox("Nierenerkrankung")
    if check_niere:
        person_dict["kidney_disease"] = 1
    else:
        person_dict["kidney_disease"] = 0

with spalte_d:
    with st.container(border=True):
        check_chol = st.checkbox("Hohes Cholesterin")
    if check_chol:
        person_dict["high_cholesterol"] = 1
    else:
        person_dict["high_cholesterol"] = 0


################################################################################



st.header("Zusammenfassung")
with st.form("my_form"):
    
    form1, form2, form3 = st.columns(3)
    
    with form1:
        st.write(f"Alter: {st.session_state.alter} Jahre")
        st.write("Geschlecht:", st.session_state.sex)
        st.write("BMI:", st.session_state.BMI)
        st.write("Taillenumfang:", st.session_state.waist, "cm")
    with form2:
        st.write("Rauchen:", rauchen)
        st.write("Alkoholkonsum:", st.session_state.alkohol, st.session_state.pumpen)
        st.write("Aktivitätsniveau:",st.session_state.activity_slider, st.session_state.active)
        st.write("Sitzdauer pro Stunde:", st.session_state.sitting)
    with form3:
        st.write("Diabetis:", check_diabetis) 
        st.write("Nierenerkrankung:", check_niere) 
        st.write("Hohes Cholesterin:", check_chol) 

    submitted = st.form_submit_button("Einreichen")
df_person = pd.DataFrame([person_dict])
column_order = [
        "age",
        "gender",
        "bmi",
        "high_cholesterol",
        "waist_circumference(cm)",
        "sitting_hours_per_day",
        "current_smoker",
        "regular_alcohol_12m",
        "diabetes",
        "kidney_disease",
        "activity_level"
    ]
df_person = df_person[column_order]
if submitted:
    st.session_state.df_person = df_person.copy()


    # Wahrscheinlichkeit berechnen
    proba_hypertension = log_model.predict_proba(df_person)[:, 1][0]

    # Eigener Threshold
    threshold = 0.4

    if proba_hypertension >= threshold:
        prediction = "Erhöhtes Hypertonie-Risiko"
        st.session_state.farbe = "red"
    else:
        prediction = "Kein erhöhtes Hypertonie-Risiko"
        st.session_state.farbe = "green"


if submitted:
    st.session_state.prediction = prediction
    st.session_state.proba = proba_hypertension


st.header("Ergebnis")
if "prediction" not in st.session_state:
    st.write("Um Ihr Risiko zu berechnen, drücken Sie auf Einreichen.")

elif not st.session_state.df_person.equals(df_person):
    st.warning("🚨 Eingabe ist nicht mehr aktuell. Bitte erneut auf 'Einreichen' klicken!")


if "prediction" in st.session_state:
    ss, sss = st.columns([1,3])
    if st.session_state.farbe=="green":
        
        with ss:
            st.success(f"Wahrscheinlichkeit: {st.session_state.proba:.2%}")
            st.success(f"{st.session_state.prediction}")
    if st.session_state.farbe=="red":
        with ss:
            st.error(f"Wahrscheinlichkeit: {st.session_state.proba:.2%}")
            st.error(f"{st.session_state.prediction}")

if st.toggle("Dataframe (Eingabe ins ML)"):
    st.dataframe(df_person)
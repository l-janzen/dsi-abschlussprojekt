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

from function import *


st.set_page_config(
    page_title="Risikofaktor",
    page_icon = ":hearts:",
    layout="wide",
    menu_items={
        'Report a bug': "mailto:haanhhanoitran@gmail.com",
        'About': "Eine App hergestellt für die Visualisierung von Hypertonie Daten \n"
                 "Autor: Ludmila Janzen, Mahshid Ghasempour, Ha Anh Tran"
    }
)




###################################################
#das wird später gelöscht, zeile 28 - 102
#dummy frame für die Zeitfilterung
np.random.seed(42)
data = pd.DataFrame({
    "timestamp": pd.date_range("2025-01-01", periods=2000, freq="D"),
    "value a": np.random.randn(2000).cumsum(),
    "value b" : np.random.randn(2000).cumsum()
})


df = pd.DataFrame({
    "timestamp": pd.date_range("2025-01-01", periods=2000, freq="D"),
    "value a": np.random.randn(2000).cumsum(),
    "value b" : np.random.randn(2000).cumsum()
})

#schaut nach min und max Datum
first_date = df["timestamp"].min().to_pydatetime()
last_date = df["timestamp"].max().to_pydatetime()


#fügt die Achsenamen in die Seitenleiste als pills und filtert duplikate
selected_options = st.sidebar.pills("Auswahl", data.columns[1:].drop_duplicates(), selection_mode ="multi")

#schaut ob eine Pill ausgewählt wird
test_value = selector(selected_options)

#Zeitfilterung
date_range = (first_date, last_date)
selected_date_range = st.sidebar.slider(
    "Wähle deinen Zeitraum",
    min_value = first_date,
    max_value = last_date,
    value = date_range , #setzt den Zeitrahmen auf dem vollen Zeitraum
    format = "YYYY-MM-DD",
    step = pd.Timedelta(weeks=1).to_pytimedelta(), #stellt sicher, dass der slider in 1 Woche schritten arbeitet
    disabled = test_value,
    key = "hallo3"
)


#Daterange Implementierung
if selected_options:
    df = df[
        (df["timestamp"]>=selected_date_range[0]) &
        (df["timestamp"]<=selected_date_range[1])
    ]




chart = create_chart(df, selected_options)
    

###################################################

##Data loading
@st.cache_data
def load_data():
    return  pd.read_csv(r".\02_ml_analysis\notebooks\nhanes_cleand.csv"
    )

data_nhanes = load_data()
df_nh = data_nhanes.copy()





##############






st.title("Was fördert Hypertonie")
##################################################################
#Anfang der Körper
st.subheader("Faktor: Körper")

#erstellt Spalten
body_col, fil_col_b = st.columns([2,1])
#################################################################
#filter für Körper
with fil_col_b:
    st.write("#### Thema der Graphen")
    st.write("Hier kannst du das Thema der Graphen ändern.")

    theme = st.radio("Thema", ["Streamlit", "Altair"])
    st.write("Du hast:", "_"+ theme + "_", "ausgewählt.")
    if theme == "Streamlit":
        chart_theme = "streamlit"
    else:
        chart_theme = None
    
    st.write("#### Typ der Graphen")
    st.write("Hier kannst du den Typ der Graphen ändern.")

    type_chart = st.radio("Typ", ["Donut", "Balken"])
    st.write("Du hast:", "_"+ type_chart + "_", "ausgewählt.")
    if type_chart == "Donut":
        type_chart = "Donut"
    else:
        type_chart = "Balken"
#########################################################################
#erstellen von tabs für Körper
with body_col:
    tab_alter, tab_gender, tab_bmi, tab_taille = st.tabs(["Alter", "Geschlecht", "BMI", "Taille"])




############################################################################
#Alter tab
age_order = ["<20", "20-29", "30-39", "40-49", "50-59", "60+"]
age_hyp = (
    df_nh.groupby("age_category")["hypertension"]
    .mean()
    .reindex(age_order)
    * 100
).reset_index()

#parameter Donut

chart_age_donut = create_donut_chart(age_hyp, x_axis="age_category",y_axis="hypertension")


#parameter Balken
chart_age_bar = create_bar_chart(age_hyp, x_axis="age_category",y_axis="hypertension")


chart = create_chart(df, selected_options)
with tab_alter:
    if type_chart == "Donut":
        st.altair_chart(chart_age_donut, theme=chart_theme, use_container_width=True)
    else:
        st.altair_chart(chart_age_bar, theme=chart_theme, use_container_width=True)


######################################################
#erstellt df für Geschlechter

gender_hyp = pd.crosstab(
    df_nh["gender"],
    df_nh["hypertension"],
    normalize="index"
) * 100
#formatiert df für Altair
df_long2 = crosstab_conversion(gender_hyp, selected_options = None, x_axis = "gender", y_axis = "Anteil (%)", serie ="Hypertonie")
#
chart_gender_donut = (
    alt.Chart(df_long2)
    .mark_arc(
        innerRadius=50,
        outerRadius=100
    )
    .encode(
        theta="Anteil (%):Q",
        color="Hypertonie:N"
    )
    .properties(
    width=200,
    height=250
    )
    .facet(
        column="gender:N",
        spacing = 30
    )
)

chart_gender_bar = (
    alt.Chart(df_long2)
    .mark_bar()
    .encode(
        x="gender:N",
        xOffset="Hypertonie:N",
        y="Anteil (%):Q",
        color="Hypertonie:N"
    )
    .interactive()
)


####################################################################
with tab_gender:
    st.write("s")
    if type_chart == "Donut":
        col1, col2, col3 = st.columns([1,5,1])
        with col1:
            st.write(' ')

        with col2:
            st.altair_chart(chart_gender_donut, theme=chart_theme, use_container_width=False)

        with col3:
            st.write(' ')
    else:    
        st.altair_chart(chart_gender_bar, theme=chart_theme, use_container_width=True)

######################################################################
#alter chart
bmi_order = ["underweight", "normal_weight", "overweight", "obesity"]
bmi_hyp = (
    df_nh.groupby("bmi_category")["hypertension"]
    .mean()
    .reindex(bmi_order)
    * 100
).reset_index()

chart_BMI_donut = create_donut_chart(bmi_hyp, x_axis="bmi_category",y_axis="hypertension")

chart_BMI_bar = create_bar_chart(bmi_hyp, x_axis="bmi_category",y_axis="hypertension")



with tab_bmi:
    st.subheader("BMI")
    if type_chart == "Donut":

        st.altair_chart(chart_BMI_donut, theme=chart_theme, use_container_width=True)
    else:    
        st.altair_chart(chart_BMI_bar, theme=chart_theme, use_container_width=True)
###############################################################
#Taillenumfang
#https://www.fittrack.de/deine-taille-wie-viel-sollte-sie-messen/
#81 cm (zu klein Frau) - 102 cm (zu dick Mann)
df_nh["waist_category"] = pd.cut(
    df_nh["waist_circumference(cm)"],
    bins=[0, 81, 102, float("inf")],
    labels=[
        "Kleine Taille",
        "Normale Taille",
        "Große Taille"
    ],
    right=False
)

waist_hyp = pd.crosstab(
    df_nh["waist_category"],
    df_nh["hypertension"],
    normalize="index"
) * 100

st.write(waist_hyp)

df_waist = crosstab_conversion(waist_hyp, selected_options=None, x_axis= "waist_category", y_axis="Anteil (%)", serie="Hypertonie" )

chart_waist_bar = (
    alt.Chart(df_waist)
    .mark_bar()
    .encode(
        x="waist_category:N",
        xOffset="Hypertonie:N",
        y="Anteil (%):Q",
        color="Hypertonie:N"
    )
)

chart_waist_donut = (
    alt.Chart(df_waist)
    .mark_arc(
        innerRadius=50,
        outerRadius=100
    )
    .encode(
        theta="Anteil (%):Q",
        color="Hypertonie:N"
    )
    .properties(
    width=200,
    height=250
    )
    .facet(
        column="waist_category:N",
        spacing = 30
    )
)



with tab_taille:
    st.subheader("Taillenumfang")
    
    if type_chart == "Donut":
        st.altair_chart(chart_waist_donut, theme=chart_theme, use_container_width=True)
    else:
        st.altair_chart(chart_waist_bar, theme=chart_theme, use_container_width=True)


#################################################################
#Anfang Lebenstil
st.subheader("Faktor Lebensstil")

#erstellt Spalten
lifestyle_col, fil_col_l = st.columns([2,1])
#################################################################
#filter für Körper
with fil_col_l:
    st.write("#### Thema der Graphen")
    st.write("Hier kannst du das Thema der Graphen ändern.")

    theme_b = st.radio("Thema", ["Streamlit", "Altair"], key = "body_radio")
    st.write("Du hast:", "_"+ theme + "_", "ausgewählt.")
    if theme_b == "Streamlit":
        chart_theme = "streamlit"
    else:
        chart_theme = None
    
    st.write("#### Typ der Graphen")
    st.write("Hier kannst du den Typ der Graphen ändern.")

    type_chart = st.radio("Typ", ["Donut", "Balken"], key ="type_b")
    st.write("Du hast:", "_"+ type_chart + "_", "ausgewählt.")
    if type_chart == "Donut":
        type_chart = "Donut"
    else:
        type_chart = "Balken"




st.subheader("Vorerkrankung")

st.write("hallo")

st.write(":hearts:")








st.subheader("Was kann dagegen gemacht werden")


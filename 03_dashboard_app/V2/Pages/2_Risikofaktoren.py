import warnings
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt

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

##############
def selector(selected_option):
    if selected_option:
        return False
    else:
        selected_option = False
        return  True


def create_chart(df, selected_options, x_axis = "timestamp", y_axis = "Wert", serie ="Serie"):
    x_axis = x_axis + ":T"
    y_axis = y_axis
    serie = serie
    return (
        alt.Chart(df)
        .transform_fold(
            pill_list(selected_options),
            as_= [serie ,y_axis]
        )
        .mark_line()
        .encode(
            x= x_axis,
            y=y_axis + ":Q",
            color= serie + ":N",
            tooltip=[x_axis, serie + ":N", y_axis+ ":Q"]
        )
        .interactive()
    )

#helps with creating pills
def pill_list(option):
    item_list = []
    for items in option:
        item_list.append(items)
    return item_list


##############
st.title("Risikofaktoren")

st.write("hallo")

st.write(":hearts:")






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

if not test_value:
    chart = create_chart(df, selected_options)

    tab1, tab2 = st.tabs(
        ["Streamlit theme (default)", "Altair native theme"]
    )

    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    with tab2:
        st.altair_chart(chart, theme=None, use_container_width=True)
else:
    st.write("Wähle in der Seitenleiste eine Option aus")
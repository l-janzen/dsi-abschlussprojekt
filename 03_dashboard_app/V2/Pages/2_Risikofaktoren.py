import warnings
import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt

BASE_DIR = Path(__file__).resolve().parents[3]


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
#helps with creating pills
def pill_list(option):
    item_list = []
    for items in option:
        item_list.append(items)
    return item_list

#helps with creating chart with different y values
def create_chart(df, selected_options, x_axis = "timestamp", x_name = "Datum", x_type = "T", y_axis = "Wert", y_scale = False, serie ="Serie", custom_labels = False, sort = [], show_legend=False):
    x_axis = x_axis + ":" + x_type
    y_axis = y_axis
    serie = serie
    if custom_labels == False:
        return (
            alt.Chart(df)
            .transform_fold(
                pill_list(selected_options),
                as_= [serie ,y_axis]
            )
            .mark_line()
            .encode(
                x= alt.X( x_axis, 
                         title= x_name,
                         scale=alt.Scale(zero=False)
                        ),
                y= alt.Y(
                    y_axis + ":Q",
                    scale=alt.Scale( zero = False)
                ),
                color= alt.Color(
                        serie + ":N",
                        legend=None if not show_legend else alt.Legend()
                    ),
                
                tooltip=[x_axis, serie + ":N", y_axis+ ":Q"],
                
            )
            .interactive()
        )
    else:
        expr = " : ".join(
            [f"datum.{serie} == '{k}' ? '{v}'"
            for k, v in custom_labels.items()]
            ) + f" : datum.{serie}"
        return (
            alt.Chart(df)
            .transform_fold(
                pill_list(selected_options),
                as_= [serie ,y_axis]
            )
            .transform_calculate(SerieLabel=expr)
            .mark_line()
            .encode(
                x= alt.X( x_axis, title= x_name ),
                y=alt.Y(
                    y_axis + ":Q",
                    scale=alt.Scale( zero = False)
                ),
                color= alt.Color("SerieLabel:N", title=serie,sort= sort ),
                tooltip=[x_axis, "SerieLabel:N", y_axis+ ":Q"]
            )
            .interactive()
        )

#hilft ob ein stock ausgewählt wurde
def selector(selected_option):
    if selected_option:
        return False
    else:
        selected_option = False
        return  True

###################################################

##Data loading
@st.cache_data
def load_data():
    data_path = BASE_DIR / "02_ml_analysis" / "notebooks" / "nhanes_cleand.csv"
    return  pd.read_csv(data_path
    )

data_nhanes = load_data()
df_nh = data_nhanes.copy()





##############
st.title("Was fördert Hypertonie")

st.subheader("Körperliche Eigenschaften")

st.subheader("Lebenstil risikofaktro")

st.subheader("Vorerkrankung")

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
trt = st.container()

#Daterange Implementierung
if selected_options:
    df = df[
        (df["timestamp"]>=selected_date_range[0]) &
        (df["timestamp"]<=selected_date_range[1])
    ]



st.button("gaga")


chart = create_chart(df, selected_options)
with trt:
    tab5, tab6 = st.tabs(
        ["Hallo", "sss"])
    with tab5:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)


tab1, tab2 = st.tabs(
    ["Streamlit theme (default)", "Altair native theme"])
    

if not test_value:
    chart = create_chart(df, selected_options)
    with tab1:
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    with tab2:
        st.altair_chart(chart, theme=None, use_container_width=True)
else:
    st.write("Wähle in der Seitenleiste eine Option aus")


st.subheader("Was kann dagegen gemacht werden")


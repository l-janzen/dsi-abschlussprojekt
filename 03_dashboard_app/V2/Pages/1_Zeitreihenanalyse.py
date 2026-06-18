import warnings
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt


st.set_page_config(
    page_title="Zeitreihenanalyse",
    page_icon = ":hearts:",
    layout="wide",
    menu_items={
        'Report a bug': "mailto:haanhhanoitran@gmail.com",
        'About': "Eine App hergestellt für die Visualisierung von Hypertonie Daten \n"
                 "Autor: Ludmila Janzen, Mahshid Ghasempour, Ha Anh Tran"
    }
)

################################################################################
##functions

#helps with creating pills
def pill_list(option):
    item_list = []
    for items in option:
        item_list.append(items)
    return item_list

#helps with creating chart with different y values
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



#hilft ob ein stock ausgewählt wurde
def selector(selected_option):
    if selected_option:
        return False
    else:
        selected_option = False
        return  True



##Data loading
@st.cache_data
def load_data():
    return  pd.read_csv(r"..\dsi-abschlussprojekt\01_public_health_analysis\data\processed\germany_hypertension_public_health_2000_2019.csv", 
    parse_dates=["Year"],
    date_format="%Y"
    )
data_year = load_data()
df_hyper_year = data_year.copy()

@st.cache_data
def load_data2():
    return  pd.read_csv(r"..\dsi-abschlussprojekt\01_public_health_analysis\data\raw\hypertension-adults-30-79.csv", 
    parse_dates=["Year"],
    date_format="%Y"
    )
data_country = load_data2()
df_country = data_country.copy()

################################################################################
st.title("Entwicklung von Hypertonie")
st.subheader(":hearts:")
#####

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



st.write(df_hyper_year)
#schaut nach min und max Datum
first_date = df["timestamp"].min().to_pydatetime()
last_date = df["timestamp"].max().to_pydatetime()

#schaut für df_hyper

first_date_h = df_hyper_year["Year"].min().to_pydatetime()
last_date_h = df_hyper_year["Year"].max().to_pydatetime()

#df_country
first_date_c = df_country["Year"].min().to_pydatetime()
last_date_c = df_country["Year"].max().to_pydatetime()


##########################################

st.sidebar.subheader("Filtereinstellung")
st.sidebar.write("Hier kannst du die Graphen filtern")

#fügt die Achsenamen in die Seitenleiste als pills und filtert duplikate
selected_options = st.sidebar.pills("Auswahl", data.columns[1:].drop_duplicates(), selection_mode ="multi")


#Geschlechtfilterung

selected_gender = st.sidebar.pills("Auswahl Geschlecht", data_year.columns[3:6].drop_duplicates(), selection_mode ="multi")

#Länderfilterung
selected_country = st.sidebar.pills("Auswahl Land", data_country.iloc[:,1].drop_duplicates(), selection_mode ="multi")


filtered_country = df_country[data_country.iloc[:,1].isin(selected_country)]



#################################################
#Zeiteinstelllung



#with st.sidebar.popover("Zeit-Einstellung"):
#    date_range = (first_date, last_date)
#    if selected_options:
#        selected_date_range = st.slider(
#            "Wähle deinen Zeitraum",
#            min_value = first_date,
#            max_value = last_date,
#            value = date_range , #setzt den Zeitrahmen auf dem vollen Zeitraum
#            format = "YYYY-MM-DD",
#            step = pd.Timedelta(weeks=1).to_pytimedelta(), #stellt sicher, dass der slider in 1 Wochen schritten arbeitet
#           key = "hallo1"
#        )
#        teste = False
#    else:
#        selected_date_range = False
#        teste = True


test_value = selector(selected_options)


date_range = (first_date, last_date)
selected_date_range = st.sidebar.slider(
    "Wähle deinen Zeitraum",
    min_value = first_date,
    max_value = last_date,
    value = date_range , #setzt den Zeitrahmen auf dem vollen Zeitraum
    format = "YYYY-MM-DD",
    step = pd.Timedelta(weeks=1).to_pytimedelta(), #stellt sicher, dass der slider in 1 Wochen schritten arbeitet
    disabled = test_value,
    key = "hallo3"
)

###############################
#schaut ob eine Pill ausgewählt wird
pick_gender = selector(selected_gender)


#Zeitfilterung

years = pd.date_range(
    first_date_h,
    last_date_h,
    freq="YS"  # Year Start
)

date_range_h = (first_date_h, last_date_h)
selected_date_range_h = st.sidebar.select_slider(
    "Wähle deinen Zeitraum",
    options=years,
    format_func=lambda x: x.strftime("%Y"),
    value=[years[0], years[-1] ],
    disabled = pick_gender,
    key = "hyper_year_range"
)

###############################
#schaut ob eine Pill ausgewählt wird

pick_country = selector(selected_country)

#Zeitfilterung bei Ländern

years = pd.date_range(
    first_date_c,
    last_date_c,
    freq="YS"  # Year Start
)

date_range_c = (first_date_c, last_date_c)
selected_date_range_c = st.sidebar.select_slider(
    "Wähle deinen Zeitraum",
    options=years,
    format_func=lambda x: x.strftime("%Y"),
    value=[years[0], years[-1] ],
    disabled = pick_country,
    key = "country_year_range"
)

st.write("country")
st.write(selected_date_range_c)
st.write(filtered_country)
##########################################


#Daterange Implementierung
if selected_options:
    df = df[
        (df["timestamp"]>=selected_date_range[0]) &
        (df["timestamp"]<=selected_date_range[1])
    ]


#Daterange Implementierung für selected gender
if selected_gender:
    df_hyper_year = df_hyper_year[
        (df_hyper_year["Year"]>=selected_date_range_h[0]) &
        (df_hyper_year["Year"]<=selected_date_range_h[1])
    ]

#Daterange Implementierung für selected country

if selected_country:
    filtered_country = filtered_country[
        (filtered_country["Year"]>=selected_date_range_c[0]) &
        (filtered_country["Year"]<=selected_date_range_c[1])
    ]

##################################################


st.write("hallo")
spalte_1, spalte_2 = st.columns([1,2])
with spalte_1:
    options = st.multiselect(
        "What are your favorite colors?",
        ["Green", "Yellow", "Red", "Blue"],
        default=["Yellow", "Red"],
    )

st.write("You selected:", options)
for items in options:
    if items == "Green":
        st.write("Green is in the seleceted item")

st.subheader("Zeitspanne :alarm_clock:")
if selected_date_range:
    st.write(selected_date_range, selected_date_range[0], selected_date_range[1])


################################################


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
    st.write("Wähle in der Seitenleiste ein Land aus")



if not pick_gender:
    chart_hyper = create_chart(df_hyper_year, selected_gender, x_axis = "Year", y_axis = "Prävalenz", serie ="Serie")

    tab3, tab4 = st.tabs(
        ["Streamlit theme (default)", "Altair native theme"]
    )
    chart_hyper = chart_hyper.mark_circle(size=80) + chart_hyper
    with tab3:
        st.altair_chart(chart_hyper, theme="streamlit", use_container_width=True)

    with tab4:
        st.altair_chart(chart_hyper, theme=None, use_container_width=True)

    
else:
    st.write("Wähle ein Geschlecht aus")



if not pick_country:
    df_merge_country = None
    for country in selected_country:
        country_data = filtered_country[filtered_country.iloc[:,1] == country]

        if df_merge_country is None:
            st.write(country)
            df_merge_country = country_data[["Year", "Prevalence of hypertension in adults aged 30-79"]]
            df_merge_country["Jahr"]=df_merge_country["Year"]
            df_merge_country = df_merge_country.rename(columns={"Prevalence of hypertension in adults aged 30-79": country})

        elif df_merge_country.index.name != "Year":

            country_data = country_data[["Year", "Prevalence of hypertension in adults aged 30-79"]]
            country_data = country_data.rename(columns={"Prevalence of hypertension in adults aged 30-79": country})
            df_merge_country = df_merge_country.set_index("Year").join(country_data.set_index("Year"),how="inner")

        else:

            country_data = country_data[["Year", "Prevalence of hypertension in adults aged 30-79"]]
            country_data = country_data.rename(columns={"Prevalence of hypertension in adults aged 30-79": country})
            df_merge_country = df_merge_country.join(country_data.set_index("Year"),how="inner")




    tab5, tab6 = st.tabs(
        ["Streamlit theme (default)", "Altair native theme"]
    )
    chart_country = create_chart(df_merge_country, selected_country, x_axis = "Jahr", y_axis = "Prävalenz", serie ="Länder")
    with tab5:
        st.altair_chart(chart_country, theme="streamlit", use_container_width=True)

    with tab6:
        st.altair_chart(chart_country, theme=None, use_container_width=True)

    
else:
    st.write("Wähle ein Land aus")


#################################################################




st.subheader("Zusammenfassung")

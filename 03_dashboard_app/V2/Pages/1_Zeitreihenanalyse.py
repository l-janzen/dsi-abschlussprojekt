import warnings
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
from streamlit_html_sidebar import create_sidebar


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
################################################################################
st.header("Deutschland Hypertonie :alarm_clock:")



##########################################
#Seiteneliste
with st.sidebar:
    st.subheader("Themaeinstellung der Graphen")
    st.write("Hier kannst du das Thema der Graphen ändern")

    theme = st.radio("Thema", ["Streamlit", "Altair"])
    st.write("You selected:", theme)
    if theme == "Streamlit":
        chart_theme = "streamlit"
    else:
        chart_theme = None

    st.subheader("Filtereinstellung")
    st.write("Hier kannst du die Graphen filtern")


##################################################
#schaut nach min und max Datum

#schaut für df_hyper

first_date_h = df_hyper_year["Year"].min().to_pydatetime()
last_date_h = df_hyper_year["Year"].max().to_pydatetime()








###############################
#schaut ob eine Pill ausgewählt wird
#pick_gender = selector(selected_gender)


#Zeitfilterung

years = pd.date_range(
    first_date_h,
    last_date_h,
    freq="YS"  # Year Start
)
with st.popover("Zeit-Einstellung"):
    date_range_h = (first_date_h, last_date_h)

    selected_date_range_h = st.select_slider(
        "Wähle deinen Zeitraum",
        options=years,
        format_func=lambda x: x.strftime("%Y"),
        value=[years[0], years[-1] ],
        #disabled = pick_gender,
        key = "hyper_year_range"
    )







################################################
#Erstellung eines Graphen

tab3, tab4, tab_stirb, tab_relation = st.tabs(
    ["Prävalenz bei den Geschlechtern", "Geschlechterdifferenz", "Sterblichkeit", "Beziehung zwischen Prävalenz und Sterblichkeit"]
)

with tab3:
    st.subheader("Prävalenz von Hypertonie von Deutschen (30 - 79 Jahren)")
    erste_spalte, zweite_spalte = st.columns([5, 1])
    with zweite_spalte:
        custom_labels = {
            "hypertension_women": "Frau",
            "hypertension_men": "Mann",
            "hypertension_prevalence": "Gesamt"
        }
        columns = data_year.columns[3:6].drop_duplicates()
        new_columns = [custom_labels.get(col, col) for col in columns]

        #Geschlechtfilterung erstellt pills

        selected_gender = st.pills("Auswahl Geschlecht", new_columns, selection_mode ="multi", key ="gender_pill")

        gender_list = []
        for items in selected_gender:
            if items == "Gesamt":
                gender_list.append("hypertension_prevalence")
            if items == "Mann":
                gender_list.append("hypertension_men")
            if items == "Frau":
                gender_list.append("hypertension_women")


        ##########################################
        #Daterange Implementierung für selected gender
        # ändert auch df

        if selected_gender:
            df_hyper_year = df_hyper_year[
                (df_hyper_year["Year"]>=selected_date_range_h[0]) &
                (df_hyper_year["Year"]<=selected_date_range_h[1])
            ]

    with erste_spalte:
        if selected_gender:
            chart_hyper = create_chart(df_hyper_year, gender_list, x_axis = "Year", y_axis = "Prävalenz", serie ="Geschlecht", custom_labels=custom_labels, sort =["Gesamt"], show_legend= True)
            chart_hyper = chart_hyper.mark_circle(size=80) + chart_hyper
            st.altair_chart(chart_hyper, theme = chart_theme, use_container_width=True)

        else:
            st.subheader("🚨")
            st.warning("Bitte wähle ein Geschlecht aus, um fortzufahren.")


    st.write("Hier kann ein Text kommen. tab3")

with tab4:
    st.subheader("Geschlechterdifferenz bei Hypertonie in DEU")
    chart_gap = create_chart(df_hyper_year, ["gender_gap_men_minus_women"], x_axis = "Year", y_axis = "Prävalenz", serie ="Serie")
    chart_gap = chart_gap.mark_circle(size=80) + chart_gap
    st.altair_chart(chart_gap, theme = chart_theme, use_container_width=True)

with tab_stirb:
    st.subheader("Sterblichkeit bei Hypertonie in DEU")
    chart_stirb = create_chart(df_hyper_year, ["hypertensive_heart_disease_death_rate"], x_axis = "Year", y_axis = "Sterblichkeit", serie ="Hallo")
    chart_stirb = chart_stirb.mark_circle(size=80) + chart_stirb
    st.altair_chart(chart_stirb, theme = chart_theme, use_container_width=True)

with tab_relation:
    st.subheader("Beziehung zwischen Prävalenz und Sterblichkeit")
    chart_relation = create_chart(df_hyper_year, ["hypertensive_heart_disease_death_rate"], x_axis = "hypertension_prevalence", x_name = "Hypertonie (%)", x_type= "Q" , y_axis = "Sterblichkeit", serie ="Serie")
    chart_relation = chart_relation.mark_circle(size=80) 
    st.altair_chart(chart_relation, theme = chart_theme, use_container_width=True)

df_generate = st.button("Dataframe")
switch = 1
if df_generate == True:
    st.write(df_hyper_year)


#################################################################




st.header("Zusammenfassung für DE")


st.write("Dummy Text")




#############################################################

#Start der Länderfilterung
st.header("Zusatz: Länder Hypertonie")


#df_country schaut nach min und max Datum
first_date_c = df_country["Year"].min().to_pydatetime()
last_date_c = df_country["Year"].max().to_pydatetime()


#Länderfilterung
selected_country = st.sidebar.pills("Auswahl Land", data_country.iloc[:,1].dropna().drop_duplicates().sort_values(), selection_mode ="multi")


filtered_country = df_country[data_country.iloc[:,1].isin(selected_country)]

###############################
#schaut ob eine Pill ausgewählt wird

pick_country = selector(selected_country)

#Zeitfilterung bei Ländern

years = pd.date_range(
    first_date_c,
    last_date_c,
    freq="YS"  # Year Start
)

with st.popover("Zeit-Einstellung"):
    date_range_c = (first_date_c, last_date_c)
    if selected_country:
        selected_date_range_c = st.select_slider(
            "Wähle deinen Zeitraum",
            options=years,
            format_func=lambda x: x.strftime("%Y"),
            value=[years[0], years[-1] ],
            disabled = pick_country,
            key = "country_year_range"
        )



#Daterange Implementierung für selected country

if selected_country:
    filtered_country = filtered_country[
        (filtered_country["Year"]>=selected_date_range_c[0]) &
        (filtered_country["Year"]<=selected_date_range_c[1])
    ]







if not pick_country:
    df_merge_country = None
    for country in selected_country:
        country_data = filtered_country[filtered_country.iloc[:,1] == country]

        if df_merge_country is None:
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
    chart_country = create_chart(df_merge_country, selected_country, x_axis = "Jahr", y_axis = "Prävalenz", serie ="Länder", show_legend= True)
    with tab5:
        st.altair_chart(chart_country, theme="streamlit", use_container_width=True)

    with tab6:
        st.altair_chart(chart_country, theme=None, use_container_width=True)

    
else:
    st.write("Wähle ein Land aus")



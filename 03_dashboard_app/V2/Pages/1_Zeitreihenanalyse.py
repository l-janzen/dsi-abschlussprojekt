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
import re

from function import *
BASE_DIR = Path(__file__).resolve().parents[3]



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


##Data loading
@st.cache_data
def load_data():
    data_path = BASE_DIR / "01_public_health_analysis" / "data" / "processed" / "germany_hypertension_public_health_2000_2019.csv"
    return  pd.read_csv(data_path, 
    parse_dates=["Year"],
    date_format="%Y"
    )
data_year = load_data()
df_hyper_year = data_year.copy()

@st.cache_data
def load_data2():
    data_path = BASE_DIR / "01_public_health_analysis" / "data" / "raw" / "hypertension-adults-30-79.csv"
    return  pd.read_csv(data_path, 
    parse_dates=["Year"],
    date_format="%Y"
    )
data_country = load_data2()
df_country = data_country.copy()

@st.cache_data
def load_data3():
    data_path = BASE_DIR / "01_public_health_analysis" / "data" / "raw" / "death-rate-from-hypertensive-heart-disease-who-ghe-age-standardized.csv"
    return  pd.read_csv(data_path, 
    parse_dates=["Year"],
    date_format="%Y"
    )
data_stirb = load_data3()
df_stirb = data_stirb.copy()






################################################################################
st.title("Entwicklung der Hypertonie-Prävalenz")
st.header(":hearts: Informationen zur Seite")
st.write(
    "Diese Seite zeigt die zeitliche Entwicklung der Hypertonie-Prävalenz in Deutschland "
    "für Erwachsene im Alter von 30 bis 79 Jahren im Zeitraum 2000 bis 2019. "
    "Ergänzend werden geschlechtsspezifische Unterschiede, die Sterberate durch "
    "hypertensive Herzerkrankungen sowie die gemeinsame Betrachtung von Prävalenz und "
    "Mortalität dargestellt."
)
################################################################################
st.header(":alarm_clock: Hypertonie in Deutschland")
st.write(
    "Die zugrunde liegenden WHO-Daten wurden für Deutschland aufbereitet und auf den "
    "gemeinsamen Beobachtungszeitraum 2000 bis 2019 eingeschränkt. Die Visualisierungen "
    "helfen dabei, langfristige Trends und Unterschiede zwischen Männern und Frauen "
    "kompakt nachzuvollziehen."
)





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
#############################
#An dieser Stelle kommen die Graphen
#Funktionen, wie Zeitfilterung müssen Sachen machen bevor Grafik dargestellt wird
zeit_container = st.container()

################################
#erstellt Spalten

main_col, filter_col = st.columns(
    [5, 1],
    gap = "medium"
)


##########################################
#Seiteneliste
with filter_col:
    st.write("#### Thema der Graphen")
    st.write("Hier kannst du das Thema der Graphen ändern.")

    theme = st.radio("Thema", ["Streamlit", "Altair"])
    st.write("Du hast:", "_"+ theme + "_", "ausgewählt.")
    if theme == "Streamlit":
        chart_theme = "streamlit"
    else:
        chart_theme = None




#############################
#widget für die Zeitfilterung
with filter_col:
    st.write("#### Zeitfilterung")
    st.write("Hier kannst du den Zeitraum ändern")
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
#Erstellung Graphen
#Tab Navigation
with main_col:
    tab3, tab4, tab_stirb, tab_relation = st.tabs(
        ["Prävalenz bei den Geschlechtern", "Geschlechterunterschied", "Sterberate", "Beziehung zwischen Prävalenz und Sterberate"]
)

###########################
#dic um spaltennamen zu ändern
custom_labels = {
    "hypertension_women": "Frau",
    "hypertension_men": "Mann",
    "hypertension_prevalence": "Gesamt"
}
#erstellt eine Liste von den neuen Spaltennamen
columns = data_year.columns[3:6].drop_duplicates()
new_columns = [custom_labels.get(col, col) for col in columns]



##############################
with zeit_container:
    with tab3:
        st.subheader("Entwicklung der Hypertonie-Prävalenz in Deutschland, 2000-2019")
        #Geschlechtfilterung erstellt pills

        selected_gender = st.pills("Auswahl Geschlecht", new_columns, selection_mode ="multi",default = "Gesamt", key ="gender_pill")

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


        if selected_gender:
            chart_hyper = create_chart(df_hyper_year, gender_list, x_axis = "Year", y_axis = "Prävalenz (%)", serie ="Geschlecht", custom_labels=custom_labels, sort =["Gesamt"], show_legend= True)
            chart_hyper = chart_hyper.mark_circle(size=80) + chart_hyper
            st.altair_chart(chart_hyper, theme = chart_theme, use_container_width=True)

        else:
            st.subheader("🚨")
            st.warning("Bitte wähle ein Geschlecht aus, um fortzufahren.")


        st.write(
            "Die Gesamtprävalenz der Hypertonie ging im Beobachtungszeitraum deutlich "
            "zurück. Im Datensatz sinkt der Wert von 40,2 % im Jahr 2000 auf 29,7 % im "
            "Jahr 2019. Auch in den geschlechtsspezifischen Reihen zeigt sich damit ein "
            "klarer langfristiger Abwärtstrend."
        )

with tab4:
    st.subheader("Geschlechterunterschied bei der Hypertonie-Prävalenz in Deutschland")
    chart_gap = create_chart(df_hyper_year, ["gender_gap_men_minus_women"], x_axis = "Year", y_axis = "Geschlechterdifferenz in Prozentpunkte", serie ="Serie")
    chart_gap = chart_gap.mark_circle(size=80) + chart_gap
    st.altair_chart(chart_gap, theme = chart_theme, use_container_width=True)
    st.write(
        "Männer weisen über den gesamten Zeitraum hinweg eine höhere Hypertonie-Prävalenz "
        "auf als Frauen. Zu Beginn lag der Abstand bei rund 10 bis 11 Prozentpunkten. "
        "Ab etwa 2011 wird die Lücke etwas kleiner und erreicht 2019 noch etwa "
        "9,4 Prozentpunkte."
    )

with tab_stirb:
    st.subheader("Sterberate aufgrund einer hypertensiven Herzerkrankung in Deutschland, 2000-2019")
    chart_stirb = create_chart(df_hyper_year, ["hypertensive_heart_disease_death_rate"], x_axis = "Year", y_axis = "Sterberate pro 100.000 Einwohner", serie ="Hallo")
    chart_stirb = chart_stirb.mark_circle(size=80) + chart_stirb
    st.altair_chart(chart_stirb, theme = chart_theme, use_container_width=True)
    st.write(
        "Im Gegensatz zur sinkenden Prävalenz steigt die Sterberate durch hypertensive "
        "Herzerkrankungen im Zeitverlauf zunächst an. Sie erhöht sich von 7,58 Todesfällen "
        "pro 100.000 Einwohner im Jahr 2000 auf einen Höchststand um 2015 und liegt 2019 "
        "mit 11,22 weiterhin über dem Ausgangsniveau."
    )

with tab_relation:
    st.subheader("Beziehung zwischen Prävalenz und Sterberate")
    chart_relation = create_chart(df_hyper_year, ["hypertensive_heart_disease_death_rate"], x_axis = "hypertension_prevalence", x_name = "Hypertonie (%)", x_type= "Q" , y_axis = "Sterberate pro 100.000 Einwohner", serie ="Serie")
    chart_relation = chart_relation.mark_circle(size=80) 
    st.altair_chart(chart_relation, theme = chart_theme, use_container_width=True)

    st.write(
        "Die Punktdarstellung zeigt eine gegenläufige Entwicklung von Prävalenz und "
        "Sterberate im Beobachtungszeitraum. Dieser Zusammenhang sollte jedoch nicht "
        "kausal interpretiert werden, da beide Kennzahlen stark vom Zeitverlauf geprägt "
        "sind und weitere medizinische oder demografische Faktoren hier nicht berücksichtigt "
        "werden."
    )



if st.toggle("Dataframe anzeigen"):
    st.dataframe(df_hyper_year)



#################################################################




st.header("Zusammenfassung für Deutschland")
st.write(
    "Die Analyse für Deutschland zeigt zwischen 2000 und 2019 einen stetigen Rückgang "
    "der Hypertonie-Prävalenz. Dieser Rückgang ist sowohl in der Gesamtbevölkerung als "
    "auch getrennt nach Geschlecht sichtbar."
)
st.write(
    "Männer sind im gesamten Zeitraum stärker betroffen als Frauen, auch wenn sich der "
    "Abstand im Zeitverlauf leicht verringert. Gleichzeitig steigt die Sterberate durch "
    "hypertensive Herzerkrankungen über viele Jahre an. Insgesamt macht die Auswertung "
    "deutlich, dass eine sinkende Prävalenz nicht automatisch mit einer sinkenden "
    "krankheitsspezifischen Mortalität einhergeht."
)




#############################################################


st.header("Zusatz: Länder Hypertonie")

###############################
#erstellt Spalten


main_col_c, filter_col_c = st.columns([5,1], gap="medium")


#macht das die Graphen hier angezeigt werden
country_container = st.container()


##############################################################
#Start der Länderfilterung
#df_country schaut nach min und max Datum
first_date_c = df_country["Year"].min().to_pydatetime()
last_date_c = df_country["Year"].max().to_pydatetime()


#Länderfilterung


st.write("Hier kannst du nach Ländern filtern")
selected_country = st.pills("Länderauswahl", data_country.iloc[:,1].dropna().drop_duplicates().sort_values(), selection_mode ="multi")


filtered_country = df_country[data_country.iloc[:,1].isin(selected_country)]

filtered_stirb = df_stirb[df_stirb.iloc[:,1].isin(selected_country)]

###############################
#schaut ob eine Pill ausgewählt wird

pick_country = selector(selected_country)

#Zeitfilterung bei Ländern

years = pd.date_range(
    first_date_c,
    last_date_c,
    freq="YS"  # Year Start
)
with filter_col_c:
    st.write("#### Thema der Graphen")
    st.write("Hier kannst du das Thema der Graphen ändern.")

    theme_c = st.radio("Thema", ["Streamlit", "Altair"], key =("theme2"))
    st.write("Du hast:", "_"+ theme_c + "_", "ausgewählt.")
    if theme_c == "Streamlit":
        chart_theme = "streamlit"
    else:
        chart_theme = None
    st.write("#### Zeitfilterung")
    st.write("Hier kannst du den Zeitraum ändern")
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
    filtered_stirb = filtered_stirb[
        (filtered_stirb["Year"]>=selected_date_range_c[0]) &
        (filtered_stirb["Year"]<=selected_date_range_c[1])
    ]







if not pick_country:
    df_merge_country = None
    df_merge_stirb = None
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
########################################
#Sterblichkeit
        if bool(re.search(r"WHO", country, re.IGNORECASE)):
            continue
        stirb = filtered_stirb[filtered_stirb.iloc[:,1] == country]
        

        if df_merge_stirb is None:
            df_merge_stirb = stirb[["Year", "Age-standardized death rate from hypertensive heart disease among both sexes"]]
            df_merge_stirb["Jahr"]=df_merge_stirb["Year"]
            df_merge_stirb = df_merge_stirb.rename(columns={"Age-standardized death rate from hypertensive heart disease among both sexes": country})

        elif df_merge_stirb.index.name != "Year":

            stirb = stirb[["Year", "Age-standardized death rate from hypertensive heart disease among both sexes"]]
            stirb = stirb.rename(columns={"Age-standardized death rate from hypertensive heart disease among both sexes": country})
            df_merge_stirb = df_merge_stirb.set_index("Year").join(stirb.set_index("Year"),how="inner")

        else:

            stirb = stirb[["Year", "Age-standardized death rate from hypertensive heart disease among both sexes"]]
            stirb = stirb.rename(columns={"Age-standardized death rate from hypertensive heart disease among both sexes": country})
            df_merge_stirb = df_merge_stirb.join(stirb.set_index("Year"),how="inner")




    with country_container:
        with main_col_c:
            tab5, tab6 = st.tabs(
                ["Prävalenz", "Sterberate"]
            )
            chart_country = create_chart(df_merge_country, selected_country, x_axis = "Jahr", y_axis = "Prävalenz (%)", serie ="Länder", show_legend= True)



            with tab5:
                st.altair_chart(chart_country, theme=chart_theme, use_container_width=True)
                if st.toggle("Dataframe Prävalenz anzeigen"):
                    try:
                        df_merge_stirb.pop("Year")
                    except:
                        l = 1
                    cols = df_merge_country.columns.tolist()
                    cols.remove("Jahr")
                    cols.insert(0, "Jahr")

                    df_merge_country = df_merge_country[cols]
                    st.dataframe(df_merge_country)

            chart_stirb = create_chart(df_merge_stirb, selected_country, x_axis = "Jahr", y_axis = "Sterberate pro 100.000 Einwohner", serie ="Länder", show_legend= True)
            with tab6:
                st.altair_chart(chart_stirb, theme=chart_theme, use_container_width=True)
                st.caption("In den Jahren zwischen 1990 - 2000 gibt es keine Daten")
                st.caption("Für die WHO-Pillen gibt es keine Daten für die Sterberate")

                if st.toggle("Dataframe Sterberate anzeigen"):
                    if df_merge_stirb is None:
                        st.error("Für die WHO-Pillen gibt es keine Daten für die Sterberate")
                        st.stop()
                    try:
                        df_merge_stirb.pop("Year")
                    except:
                        l = 1
                    cols = df_merge_stirb.columns.tolist()
                    cols.remove("Jahr")
                    cols.insert(0, "Jahr")

                    df_merge_stirb = df_merge_stirb[cols]
                    st.dataframe(df_merge_stirb)

    
else:
    with country_container:
        with main_col_c:
            st.subheader("🚨")
            st.warning("Bitte wähle ein Land unten aus, um fortzufahren.")



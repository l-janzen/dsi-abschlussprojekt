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



###################################################

##Data loading
@st.cache_data
def load_data():
    data_path = BASE_DIR / "02_ml_analysis" / "notebooks" / "nhanes_cleand.csv"
    return  pd.read_csv(data_path
    )

data_nhanes = load_data()
df_nh = data_nhanes.copy()



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
#Titel
st.title("Was fördert Hypertonie?")


st.write("hallo")

st.write(":hearts:")

##################################################################
#Anfang der Körper
st.header("Faktor: Körper")

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

chart_age_donut = create_donut_chart(age_hyp, x_axis="age_category", x_name="Alterskategorie",y_axis="hypertension", inner_r=80 ,outer_r=130)


#parameter Balken
chart_age_bar = create_bar_chart(age_hyp, x_axis="age_category",y_axis="hypertension", x_name="Alter (Jahren)",y_name="Teilnehmeranteil mit Hypertonie (%)", sort=["<20"])



with tab_alter:
    st.subheader("Alter")
    if type_chart == "Donut":
        st.altair_chart(chart_age_donut, theme=chart_theme, use_container_width=True)
    else:
        st.altair_chart(chart_age_bar, theme=chart_theme, use_container_width=True)
    if st.toggle("Dataframe(Alter) anzeigen"):
        st.dataframe(age_hyp)


######################################################
#erstellt df für Geschlechter

gender_hyp = pd.crosstab(
    df_nh["gender"],
    df_nh["hypertension"],
    normalize="index"
) * 100
#formatiert df für Altair
df_long2 = crosstab_conversion(gender_hyp, selected_options = None, x_axis = "gender", y_axis = "Anteil (%)", serie ="Hypertonie")
#ändert 

chart_gender_donut = create_donut_chart(df_long2, x_axis="Hypertonie", x_name="Hypertonie",y_axis="Anteil (%)", inner_r=50 ,outer_r=100)

chart_gender_donut = extension_donut(chart_gender_donut, facet_title="Geschlecht")



########################################
#bar chart

chart_gender_bar = create_bar_chart(df_long2, "gender", y_axis="Anteil (%)",serie="Hypertonie",x_name="Geschlecht",y_name="Hypertonie-Anteil (%)", show_legend=True)


################################################################################
#umbenennen der Werte in der Achse

labels = {
    "Female": "Frau",
    "Male": "Mann"
}

chart_gender_donut = rename_axis(chart_gender_donut, labels, x_axis= "gender")
chart_gender_bar = rename_axis(chart_gender_bar, labels, x_axis= "gender")

####################################################################
with tab_gender:
    st.subheader("Geschlecht")
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
    if st.toggle("Dataframe(Geschlecht) anzeigen"):
        st.dataframe(gender_hyp)

######################################################################
#alter chart
bmi_order = ["underweight", "normal_weight", "overweight", "obesity"]
bmi_hyp = (
    df_nh.groupby("bmi_category")["hypertension"]
    .mean()
    .reindex(bmi_order)
    * 100
).reset_index()

chart_BMI_donut = create_donut_chart(bmi_hyp, x_axis="bmi_category", x_name="BMI-Kategorie",y_axis="hypertension", y_name="Hypertonie" ,inner_r=80 ,outer_r=130)

chart_BMI_bar = create_bar_chart(bmi_hyp, x_axis="bmi_category", x_name="BMI Kategorie", y_axis="hypertension", y_name="Teilnehmeranteil mit Hypertonie (%)")


BMI_ger = ["Untergewicht", "Sollgewicht", "Übergewicht", "Fettleibigkeit"]
BMI_labels = dict(zip(bmi_order,BMI_ger))

#nimmt ein Dict an und übersetzt die Kategorienamen
chart_BMI_donut = rename_axis(chart_BMI_donut, BMI_labels, x_axis="bmi_category")
chart_BMI_bar = rename_axis(chart_BMI_bar, BMI_labels, x_axis="bmi_category")

with tab_bmi:
    st.subheader("Body Mass Index (BMI)")
    if type_chart == "Donut":

        st.altair_chart(chart_BMI_donut, theme=chart_theme, use_container_width=True)
    else:    
        st.altair_chart(chart_BMI_bar, theme=chart_theme, use_container_width=True)

    if st.toggle("Dataframe(BMI) anzeigen"):
        st.dataframe(bmi_hyp)
###############################################################
#Taillenumfang
#https://www.fittrack.de/deine-taille-wie-viel-sollte-sie-messen/
#81 cm (zu klein Frau) - 102 cm (zu dick Mann)
df_nh["waist_category"] = pd.cut(
    df_nh["waist_circumference(cm)"],
    bins=[0, 81, 102, float("inf")],
    labels=[
        "Kleine Taille (< 81 cm)",
        "Normale Taille (81-102 cm)",
        "Große Taille (> 102 cm)"
    ],
    right=False
)

waist_hyp = pd.crosstab(
    df_nh["waist_category"],
    df_nh["hypertension"],
    normalize="index"
) * 100



df_waist = crosstab_conversion(waist_hyp, selected_options=None, x_axis= "waist_category", y_axis="Anteil (%)", serie="Hypertonie" )

chart_waist_bar = create_bar_chart(df_waist, x_axis= "waist_category", x_name="Taillenkategorie", y_axis= "Anteil (%)",y_name="Hypertonie-Anteil (%)", show_legend="True", serie="Hypertonie", sort=[
        "Kleine Taille",
        "Normale Taille",
        "Große Taille"
    ])

chart_waist_donut = create_donut_chart(df_waist,x_axis="Hypertonie",x_name="Taillenkategorie",y_axis="Anteil (%)", y_name="Hypertonie-Anteil (%)", inner_r=45, outer_r=90)

chart_waist_donut = extension_donut(chart_waist_donut, width= 100, height=250,facet_column="waist_category", facet_title="Taillenkategorie",sort=[
        "Kleine Taille",
        "Normale Taille",
        "Große Taille"
    ])


def_waist =[
        "Kleine Taille (< 81 cm)",
        "Normale Taille (81-102 cm)",
        "Große Taille (> 102 cm)"
    ]

ab_waist= [
        "Kleine Taille",
        "Normale Taille",
        "Große Taille"
    ]
waist_dict = dict(zip(def_waist,ab_waist ))

chart_waist_bar = rename_axis(chart_waist_bar, waist_dict, x_axis="waist_category")



with tab_taille:
    st.subheader("Taillenumfang")
    
    if type_chart == "Donut":
        col1, col2, col3 = st.columns([1,50,1])
        with col1:
            st.write(' ')

        with col2:
            st.altair_chart(chart_waist_donut, theme=chart_theme, use_container_width=False)

        with col3:
            st.write(' ')
        
    else:
        st.altair_chart(chart_waist_bar, theme=chart_theme, use_container_width=True)
    st.caption("Kleine Taille (< 81 cm), Normale Taille (81-102 cm) und Große Taille (> 102 cm)")
    if st.toggle("Dataframe(Taille) anzeigen"):
        st.dataframe(waist_hyp)


#################################################################
#Anfang Lebenstil
st.header("Faktor: Lebensstil")

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


with lifestyle_col:
    tab_smoke, tab_alc, tab_sit = st.tabs(["Rauchen","Alkohol","Aktivität und Sitzdauer"])

########################################################################
#rauchen
smoke_hyp = (
    df_nh.groupby("current_smoker")["hypertension"]
    .mean()
    * 100
).reset_index()

#bar chart
chart_smoke_bar = create_bar_chart(smoke_hyp, x_axis="current_smoker", x_name="Rauchstatus", y_axis="hypertension",y_name="Hypertonie-Anteil (%)")

#donut chart
chart_smoke_donut = create_donut_chart(smoke_hyp, x_axis="current_smoker", x_name="Rauchstatus", y_axis="hypertension",y_name="Hypertonie-Anteil (%)")

#dict smoke
old_smoke = [0,1]
new_smoke_list = ["Nichtraucher", "Raucher"]
dict_smoke = dict(zip(old_smoke, new_smoke_list))
#werte umbenennen
chart_smoke_bar = rename_axis(chart_smoke_bar, dict_smoke, x_axis="current_smoker")
chart_smoke_donut = rename_axis(chart_smoke_donut, dict_smoke, x_axis="current_smoker")
#smoke graph
with tab_smoke:
    st.subheader("Anteil von Hypertonie nach aktuellem Rauchstatus")

    if type_chart == "Donut":
        st.altair_chart(chart_smoke_donut, theme=chart_theme, use_container_width=True)
      
    else:
        st.altair_chart(chart_smoke_bar, theme=chart_theme, use_container_width=True)
    if st.toggle("Dataframe(Rauchen) anzeigen"):
        st.dataframe(smoke_hyp)

##########################################################################
#Alkohol
alc_hyp = (
    df_nh.groupby("regular_alcohol_12m")["hypertension"]
    .mean()
    * 100
).reset_index()

#bar chart
chart_alc_bar = create_bar_chart(alc_hyp, x_axis="regular_alcohol_12m", x_name="Alkholkonsumstatus", y_axis="hypertension",y_name="Hypertonie-Anteil (%)", sort =["0","1"])



#donut chart
chart_alc_donut = create_donut_chart(alc_hyp, x_axis="regular_alcohol_12m", x_name="Alkholkonsumstatus", y_axis="hypertension",y_name="Hypertonie-Anteil (%)")


#dict alc
old_alc = [1,0]
new_alc_list = ["Alkoholgruppe","Abstinenzgruppe"]
dict_alc = dict(zip(old_alc, new_alc_list))


#werte umbenennen
chart_alc_bar = rename_axis(chart_alc_bar, dict_alc, x_axis="regular_alcohol_12m")
chart_alc_donut = rename_axis(chart_alc_donut, dict_alc, x_axis="regular_alcohol_12m")



#alc graph erstellen
with tab_alc:
    st.subheader("Anteil von Hypertonie nach 12 monatigen Alkoholkonsum")

    if type_chart == "Donut":
        st.altair_chart(chart_alc_donut, theme=chart_theme, use_container_width=True)
      
    else:
        st.altair_chart(chart_alc_bar, theme=chart_theme, use_container_width=True)
    if st.toggle("Dataframe(Alohol) anzeigen"):
        st.dataframe(alc_hyp)
################################################################################

activity_summary = (
    df_nh.groupby("activity_level_label")
    .agg(
        n=("hypertension", "count"),
        hypertonie_anteil=("hypertension", "mean"),
        mittlere_sitzzeit=("sitting_hours_per_day", "mean"),
        median_sitzzeit=("sitting_hours_per_day", "median")
    )
)

df_nh["sitting_category"] = pd.cut(
    df_nh["sitting_hours_per_day"],
    bins=[0, 4, 6, 10, float("inf")],
    labels=[
        "Niedrig (<4h)",
        "Mäßig (4-6h)",
        "Hoch (6-10h)",
        "Sehr hoch (>10h)"
    ],
    right=False
)

bubble_df = (
    df_nh.groupby(
        ["activity_level_label", "sitting_category"],
        observed=True
    )["hypertension"]
    .mean()
    .reset_index()
)

bubble_df["hypertonie_anteil"] = (
    bubble_df["hypertension"] * 100
)
min_val = bubble_df["hypertonie_anteil"].min()
max_val = bubble_df["hypertonie_anteil"].max()


chart = (
    alt.Chart(bubble_df)
    .mark_circle()
    .encode(
        x=alt.X(
            "sitting_category:N",
            title="Sitzdauer pro Tag",
            axis=alt.Axis(
                labelAngle=0
                ),
            sort=[
                "Niedrig (<4h)",
                "Mäßig (4-6h)",
                "Hoch (6-10h)",
                "Sehr hoch (>10h)"
            ]
        ),
        y=alt.Y(
            "activity_level_label:N",
            title="Aktivitätsniveau"
        ),
        size=alt.Size(
            "hypertonie_anteil:Q",
            title="Hypertonie-Anteil (%)",
            scale=alt.Scale(
                range=[100, 2000]
            )
        ),
        color=alt.Color(
            "hypertonie_anteil:Q",
            title="Hypertonie-Anteil (%)",
            scale=alt.Scale(
                domain=[25, 40, 55],
                range=[
                    "#2E8B57",  # Grün
                    "#F4B400",  # Goldgelb
                    "#D32F2F"   # Rot
                ]
                
            ),
            legend=alt.Legend(
                values=[20, 30, 40, 50, 60]
            )
        ),
        tooltip=[
            "activity_level_label:N",
            "sitting_category:N",
            alt.Tooltip(
                "hypertonie_anteil:Q",
                format=".1f",
                title="Hypertonie (%)"
            )
        ]
    )
    .properties(
        width=500,
        height=320
    )
)


with tab_sit:
    st.subheader("Anteil von Hypertonie nach Aktivität und Sitzdauer")

    st.altair_chart(chart, theme=chart_theme, use_container_width=True)
      
    
    if st.toggle("Dataframe(Sitzdauer) anzeigen"):
        activity_summary["hypertonie_anteil"] = activity_summary["hypertonie_anteil"]*100
        st.dataframe(activity_summary)
        bubble_df.pop("hypertension")
        st.dataframe(bubble_df)





#################################################################
st.header("Faktor: Vorerkrankung")


#erstellt Spalten
disease_col, fil_col_d = st.columns([2,1])
#################################################################
#filter für disease
with fil_col_d:
    st.write("#### Thema der Graphen")
    st.write("Hier kannst du das Thema der Graphen ändern.")

    theme_d = st.radio("Thema", ["Streamlit", "Altair"], key = "disease_radio")
    st.write("Du hast:", "_"+ theme + "_", "ausgewählt.")
    if theme_d == "Streamlit":
        chart_theme = "streamlit"
    else:
        chart_theme = None
    
    st.write("#### Typ der Graphen")
    st.write("Hier kannst du den Typ der Graphen ändern.")

    type_chart = st.radio("Typ", ["Donut", "Balken"], key ="type_d")
    st.write("Du hast:", "_"+ type_chart + "_", "ausgewählt.")
    if type_chart == "Donut":
        type_chart = "Donut"
    else:
        type_chart = "Balken"


#################################################################################disease in einen Df

pre_existing_conditions = ["diabetes", "kidney_disease", "high_cholesterol"]

condition_summary = []

for col in pre_existing_conditions:
    temp = (
        df_nh.groupby(col)["hypertension"]
        .agg(
            n="count",
            hypertonie_anteil="mean"
        )
        .reset_index()
    )
    
    temp["hypertonie_anteil"] = temp["hypertonie_anteil"] * 100
    temp["vorerkrankung"] = col
    
    temp = temp.rename(columns={col: "status"})
    
    condition_summary.append(temp)

condition_summary = pd.concat(condition_summary, ignore_index=True)

condition_summary = condition_summary.round(2)

condition_summary ["status"] = condition_summary ["status"].replace({
    1: "ja",
    0: "nein"
    
})


#Parameter char
#bar chart
chart_disease_bar = create_bar_chart(condition_summary, x_axis="vorerkrankung", x_name="Vorerkrankung",y_axis="hypertonie_anteil", y_name="Hypertonie-Anteil (%)",serie="status", sort=["ja"], show_legend=True)
#donut chart disease
chart_disease_donut = create_donut_chart(condition_summary, x_axis="status", x_name="Hypertonie",y_axis="hypertonie_anteil", y_name="Hypertonie-Anteil (%)",sort=["ja","nein"])

chart_disease_donut = extension_donut(chart_disease_donut, facet_column="vorerkrankung",facet_title="Vorerkrankung")

#Vorerkrankung umbenennen im graph

disease_new = ["Diabetis", "Nierenerkrankung", "Hohes Cholesterin"]
disease_dict = dict(zip(pre_existing_conditions,disease_new))

chart_disease_donut = rename_axis(chart_disease_donut,disease_dict, "vorerkrankung" )
chart_disease_bar = rename_axis(chart_disease_bar,disease_dict, "vorerkrankung" )


chart_disease_bar = chart_disease_bar.properties(
        height=420
    )


with disease_col:
    if type_chart == "Donut":
        st.altair_chart(chart_disease_donut, theme=chart_theme, use_container_width=True)
    else:
        st.altair_chart(chart_disease_bar, theme=chart_theme, use_container_width=True)

if st.toggle("Dataframe(Vorerkrankung) anzeigen"):
    st.dataframe(condition_summary)



st.write("hallo")

st.write(":hearts:")



st.header("Was kann dagegen gemacht werden?")


import warnings
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import altair as alt
import re



################################################################################
##functions

#helps with creating pills
def pill_list(option):
    item_list = []
    for items in option:
        item_list.append(items)
    return item_list

#helps with creating chart with different y values
def create_chart(df, selected_options, x_axis = "timestamp", x_name = "Datum", x_type = "T", y_axis = "Wert", serie ="Serie", custom_labels = False, sort = [], show_legend=False):
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
    

def lo():
    return "Hello"

####################################################
#macht df kompatibel für Altair
def crosstab_conversion(
    df,
    selected_options=None,
    x_axis="timestamp",
    y_axis="Wert",
    serie="Serie"
):
    df = df.copy()
    df.columns = df.columns.astype(str)
    df = df.reset_index()
#konvertiert True und False
    if "1.0" in df.columns:
        df["ja"] = pd.to_numeric(df["1.0"])

    if "0.0" in df.columns:
        df["nein"] = pd.to_numeric(df["0.0"])
#wenn keine Angabe, welche Spalten
    if selected_options is None:
        selected_options = [
            c for c in df.columns
            if c not in [x_axis, "0.0", "1.0"]
        ]#wählt die ja und nein aus
    else:
        selected_options = pill_list(selected_options)

    return df.melt(
        id_vars=x_axis,
        value_vars=selected_options,
        var_name=serie,
        value_name=y_axis
    )
####################################################
#einfache Parameter Eingabe für bar

def create_bar_chart(
    df,
    x_axis,
    y_axis,
    serie=None,
    x_name=None,
    y_name=None,
    show_legend=False,
    sort=None
):
    if x_name is None:
        x_name = x_axis

    if y_name is None:
        y_name = y_axis

    if sort is None:
        sort = []

    encoding = {
        "x": alt.X(
            f"{x_axis}:N",
            title=x_name,
            sort=sort
        ),
        "y": alt.Y(
            f"{y_axis}:Q",
            title=y_name
        )
    }

    if serie is not None:
        encoding["xOffset"] = alt.XOffset(f"{serie}:N")
        encoding["color"] = alt.Color(
            f"{serie}:N",
            legend=alt.Legend() if show_legend else None
        )
    else:
        encoding["color"] = alt.Color(
            f"{x_axis}:N",
            legend=alt.Legend() if show_legend else None
        )

    return (
        alt.Chart(df)
        .mark_bar()
        .encode(**encoding)
        .interactive()
    )

#einfache Parameter Eingabe für donut
def create_donut_chart(df, x_axis, y_axis):
    return (
    alt.Chart(df)
    .mark_arc(
        innerRadius=100
    )
    .encode(
        theta= y_axis+":Q",
        color= x_axis+":N"
    )
)

def rename_axis(chart, labels: dict, x_axis: str):
    expr = (
        " : ".join(
            [f"datum.{x_axis} == '{k}' ? '{v}'"
             for k, v in labels.items()]
        )
        + f" : datum.{x_axis}"
    )

    return chart.transform_calculate(**{x_axis: expr})
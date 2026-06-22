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
    

def lo():
    return "Hello"

####################################################

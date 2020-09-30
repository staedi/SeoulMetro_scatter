# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

# import generic
import pandas as pd
import numpy as np
from datetime import datetime
import math
import time
import altair as alt
import pydeck as pdk
import streamlit as st

# color_set = {'1호선':'#0052A4','2호선':'#009D3E','3호선':'#EF7C1C','4호선':'#00A5DE','5호선':'#996CAC','6호선':'#CD7C2F','7호선':'#747F00','8호선':'#EA545D','9호선':'#A17E46','경의/중앙선':'#77C4A3','수인/분당선':'#F5A200','경강선':'#003DA5','경춘선':'#0C8E72','우이신설선':'#B0CE18','공항철도':'#0090D2'}


# Module to display sidebar
def display_sidebar(data):
    min_date, max_date = None, None
    st.sidebar.header('Choose Selections below')
    # 1) Minimum / Maximum dates to display
    st.sidebar.markdown('Choose dates below')
    date_ranges = data['Date'].str[:7].unique().tolist()
    min_date = st.sidebar.selectbox('Start date',date_ranges)
    date_ranges = [date for date in date_ranges if date>=min_date]
    max_date = st.sidebar.selectbox('End date',date_ranges)

    # # 2) Data group
    # st.sidebar.markdown('Choose grouping units below')
    # if min_date and max_date and min_date != max_date:
    #     group_list = ['Daily','Monthly']
    # else:
    #     group_list = ['Daily']
    # sel_unit = st.sidebar.selectbox('Group units',group_list)

    return min_date, max_date


def animate_maps(data,color_set,min_date,max_date):
    st.subheader(f'Subway usages from {min_date} to {max_date}')
    st.write('Line color: Colorset of subway line')
    st.write('Scatter size: Number of Users')

    data = data.drop(data.loc[(data['Date'].str[:7]<min_date) | (data['Date'].str[:7]>max_date),].index)

    def hex_to_rgb(hex):
        hex = hex.lstrip('#')
        # return tuple(int(hex[i:i+2],16) for i in (0,2,4))
        return list(int(hex[i:i+2],16) for i in (0,2,4))

    data.loc[:,'color'] = data['color'].apply(hex_to_rgb)
    data.loc[:,'users'] = (data.loc[:,'EntriesN']+data.loc[:,'ExitsN'])
    data.loc[:,'size'] = data.loc[:,'users']/data.loc[:,'users'].max()

    date_ranges = list(data['Date'].unique())
    current_date = st.markdown('Current date: ')
    map = st.empty()

    for idx, date in enumerate(date_ranges):
        current_date.markdown(f"Current date: {date}")
        r = show_map(data.loc[data['Date']==date,])
        time.sleep(0.2)
        map.pydeck_chart(r, use_container_width=True)

def show_map(data):
    # st.subheader(f'Subway usages from {min_date} to {max_date}')
    view_state = pdk.ViewState(
        latitude = data['Latitude'].mean(),
        longitude = data['Longitude'].mean(),
        zoom=9)

    scatterplotlayer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        pickable=True,
        opacity = 0.6,
        auto_highlight=True,
        # stroked=True,
        filled=True,
        radius_scale=1000,
        radius_min_pixels=3,
        radius_max_pixels=100,
        get_fill_color='color',
        get_position='[Longitude,Latitude]',
        get_radius='size',
    )
    tooltip = {"html":"<b>Line:</b> {Line} <br /><b>Station:</b> {Station} <br /><b>Entries:</b> {EntriesN} <br /><b>Exits: </b> {ExitsN}"}


    r = pdk.Deck(
        layers=[scatterplotlayer],
        initial_view_state=view_state,
        map_style=pdk.map_styles.LIGHT,
        tooltip=tooltip,
        )

    return r


# # def show_chart(data,items):
# #     stat = {'rank':'Rank','All Employees':'All Employees (1K)','Avg Hourly Wages':'Avg Hourly Wages','eWage':'Pricing Power','score':'Employment Strengths','eCPI':'Price Index'}
# #
# #     stat_text = list(stat.values())
# #     stat_keys = list(stat.keys())
# #     items = [key for key, value in items.items() if value!=0]
# #
# #     data = data[['year','cbsa_area','Metro area']+stat_keys+items]
# #
# #     st.subheader('Employment strengths')
# #
# #     # Employment strengths scatter
# #     scatter = (alt.Chart(data)
# #         .mark_circle()
# #         .encode(
# #             x=alt.X(stat_keys[1],title=stat_text[1]),
# #             y=alt.Y(stat_keys[2],title=stat_text[2]),
# #             size=alt.Size(stat_keys[4],legend=None),
# #             tooltip=[alt.Tooltip('Metro area'),alt.Tooltip(stat_keys[0],title=stat_text[0]),alt.Tooltip(stat_keys[1],title=stat_text[1]),alt.Tooltip(stat_keys[2],title=stat_text[2],format='$')]
# #         )
# #     )
# #
# #     st.altair_chart(scatter,use_container_width=True)
# #
# #     st.subheader('Price Index')
# #
# #     # Price Index stacked_bar
# #     stacked_cpi = (alt.Chart(data)
# #         .transform_fold(items,['Item','Price Index'])
# #         .mark_bar()
# #         .encode(
# #             x=alt.X('Price Index:Q'),
# #             y=alt.Y('Metro area:N',sort=alt.EncodingSortField(field=stat_keys[5],order='descending')),
# #             color=alt.Color('Item:N'),
# #             tooltip=[alt.Tooltip('Metro area'),alt.Tooltip('Item:N'),alt.Tooltip('Price Index:Q'),alt.Tooltip(stat_keys[5],title=stat_text[5])]
# #         )
# #     )
# #
# #     st.altair_chart(stacked_cpi,use_container_width=True)
# #
# #     st.subheader('Pricing Power')
# #
# #     # Employment strengths scatter
# #     stacked_pp = (alt.Chart(data)
# #         .mark_bar()
# #         .encode(
# #             x=alt.X(stat_keys[3],title=stat_text[3]),
# #             y=alt.Y('Metro area:N',sort=alt.EncodingSortField(field=stat_keys[3],order='descending')),
# #             tooltip=[alt.Tooltip('Metro area'),alt.Tooltip(stat_keys[2],title=stat_text[2]),alt.Tooltip(stat_keys[5],title=stat_text[5]),alt.Tooltip(stat_keys[3],title=stat_text[3])]
# #         )
# #     )
# #
# #     st.altair_chart(stacked_pp,use_container_width=True)

# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

'''
app.py: Frontend runner file for SeoulMetro Visualization Streamlit application

Dependencies
data: geojson (Latitude and Longitude)
modules:
frontend.py: Front-end works
generic.py: Load necessary files (daily statistics, map)
'''

import streamlit as st
import pandas as pd
import generic
import frontend
import pydeck as pdk
import math

file_path = {'data':'data/SeoulMetro_'}
# file_list = {'map':'Stations.csv','raw':['202004.csv','202005.csv']}
file_list = {'map':'Stations.csv','raw':['202004.csv','202005.csv','202006.csv','202007.csv','202008.csv','202009.csv']}

line_mapping = {'1호선':['1호선','경원선', '경인선', '경부선', '장항선'],'3호선':['3호선','일산선'],'4호선':['4호선','안산선','과천선'],'9호선':['9호선','9호선2~3단계'],'수인/분당선':['수인선','분당선'],'경의/중앙선':['경의선','중앙선'],'공항철도':['공항철도 1호선']}

color_set = {'1호선':'#0052A4','2호선':'#009D3E','3호선':'#EF7C1C','4호선':'#00A5DE','5호선':'#996CAC','6호선':'#CD7C2F','7호선':'#747F00','8호선':'#EA545D','9호선':'#A17E46','수인/분당선':'#F5A200','우이신설선':'#B0CE18','공항철도':'#0090D2'}


################################################################
# Header and preprocessing

# Set Title
st.title('Greater Seoul area Subway usages')

# Preset data load for sidebar display
update_status = st.markdown("Loading raw data...")

data = generic.preprocess(file_path['data'],[file_list['raw'],file_list['map']],line_mapping,color_set)
update_status.markdown('Load complete!')

################################################################
# Sidebar section (Supersector, Region and Year of interest)
min_date, max_date = frontend.display_sidebar(data)

################################################################
# Main section

# Display chart and map
# frontend.show_chart(merged_data,weights[int(sel_focus[0])])
frontend.animate_maps(data,color_set,min_date,max_date)


# Caption for credits
st.subheader('Credits')
data_source = 'SeoulMetro'
st.write('Data source: ' + data_source)
st.write('Map provider: Mapbox, OpenStreetMap')

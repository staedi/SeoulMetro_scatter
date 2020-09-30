# pylint: disable=unused-variable
# pylint: disable=anomalous-backslash-in-string

import numpy as np
import pandas as pd
from datetime import datetime
import streamlit as st

##################################################################
## Preprocessing parts
def preprocess(filepath, typelist, line_mapping, color_set):
    raw = read_dataset(filepath,typelist[0]).copy()
    map = read_dataset(filepath,typelist[1]).copy()
    raw = clean_dataset('raw',raw,color_set,line_mapping)
    map = clean_dataset('map',map,color_set)
    data = merge_dataset(raw,map)
    return data

@st.cache#(allow_output_mutation=True)
def read_dataset(filepath, filelist):
    # dateparse = lambda x:datetime.strptime(x,'%Y%m%d')
    if type(filelist) == list:
        for idx, filename in enumerate(filelist):
            ds = pd.read_csv(filepath+filename)
            # ds = pd.read_csv(filepath+filename,parse_dates=['사용일자'],date_parser=dateparse).copy()
            ds = ds.iloc[:,:-1]
            ds.columns = ['Date','Line','Station','EntriesN','ExitsN']
            ds['Date'] = ds['Date'].astype(str).apply(lambda x:x[:4]+'-'+x[4:6]+'-'+x[6:])
            ds['Station'] = ds['Station'].str.split('(',expand=True)[0]
            ds = ds.sort_values(by='Date')
            if idx == 0:
                data = ds
            else:
                data = pd.concat([data,ds],axis=0)

    else:
        data = pd.read_csv(filepath+filelist)

    return data

def clean_dataset(type,data,color_set,line_mapping=None):
    if type == 'raw':
        data.loc[(data['Station'].isin(['서빙고','옥수','왕십리','응봉','이촌','청량리','한남'])) & (data['Line']=='경원선') ,'Line'] = '경의/중앙선'

        for dest, src in line_mapping.items():
            data['Line'] = data['Line'].replace(src,dest)

    elif type == 'map':
        data = data.groupby(['Station','Line'])[['Latitude','Longitude']].mean().reset_index()

        data['color'] = data['Line'].apply(lambda x:color_set.get(x))
        data.dropna(inplace=True)

    return data

def merge_dataset(dataset1, dataset2):
    return pd.merge(dataset1,dataset2,how='inner',on=['Station','Line'])

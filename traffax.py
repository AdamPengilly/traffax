#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:35:37 2020

@author: adampengilly
"""

import streamlit as st

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
#import seaborn as sns 
#import shapefile as shp
# import joypy

import folium
import folium.plugins as plugins
from streamlit_folium import folium_static


#import ipywidgets
#from ipywidgets import interact, interactive, fixed, interact_manual
import scikitplot as skplt

import json

# from scipy import stats
# import statsmodels.api as sm  
# from statsmodels.tsa.stattools import acf, pacf
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
# from statsmodels.tsa.seasonal import seasonal_decompose

import datetime
from datetime import timedelta

import pickle
# from tqdm import tqdm

# import os
# import glob

# from sklearn.preprocessing import PowerTransformer
# from sklearn.metrics import mean_squared_error



# -*- coding: utf-8 -*-


#CREATE A FUNCTION TO LOAD DATA SO CAN CACHE DATA SUCH THAT IT DOESN'T HAVE TO BE RELOADED EACH TIME
@st.cache
def load_df_traffic():
    #the edited df_traffic dataframe
    path = '/Users/adampengilly/Desktop/Capstone Data/pickles/'
    filename = 'df_traffic_filled_pickle_rev2'
    df_traffic =pickle.load(open(path+filename, 'rb'))
    return df_traffic
df_traffic = load_df_traffic()

@st.cache
def load_geo_json():
    # load geo_json (for Choropleth map)
    with open('/Users/adampengilly/Desktop/Capstone Data/2417_4263_bundle_archive/london_boroughs.json') as f:
        geojson_borough = json.load(f)
    # add feature 'id' local_authority_name code to geojson (so can be matched with dataframe)
    # access features
    for i in geojson_borough['features']:
        i['id'] = i['properties']['name']
    return geojson_borough
geo_json_borough = load_geo_json()
    
@st.cache
def load_london_df():
    #compiled london dataframe (shortened to only features used in this app)
    path = '/Users/adampengilly/Desktop/Projects/'
    filename = 'london_slim_pickle'
    london = pickle.load(open(path+filename, 'rb'))
    london.Veh_Type_Grouped = london.Veh_Type_Grouped.map(lambda x : ", ".join(x))
    return london
london = load_london_df()


@st.cache
def trans_pick_short():
    #Heat map won't work if there is a small amount of data. Use this list of the top occuring veh_types
    transport_pick_short = list(london.Veh_Type_Grouped.value_counts().sort_values(ascending=False)[:20].index)
    transport_pick_short.insert(0,'ALL') #insert to start of list
    return tuple(transport_pick_short)
transport_pick_short = trans_pick_short()



#Function that plots accidents by vehicle type over london
def heatmap_ts(veh_types='ALL', map_type='OpenStreetMap'):  
    
    time_index = []
    lat_long_monthly =[]
    for year in range(2005,2016):
        for month in range(1,13):
            idx = "'"+str(year)+', '+str(month)+"'"
            time_index.append(idx)
            if veh_types == 'ALL':
                temp = london
            else:
                temp = london[london.Veh_Type_Grouped == veh_types]
                
            lat_long_monthly.append(temp.loc[idx][['Latitude', 'Longitude']].values.tolist())
   
    f = folium.Figure(width=1000, height=700) #for some reason the map is too small in this notebook and can't be rescaled. Adding this figures is a way to allow resizing
    m = folium.Map([51.5080, -0.1], tiles=map_type, zoom_start=11)
    f.add_child(m)
    
    hm = plugins.HeatMapWithTime(
        lat_long_monthly,
        index=time_index,
        auto_play=False,
        max_opacity=0.4
    )
    hm.add_to(m)
    
    return m

#START OF PAGE INPUT...

veh_select = st.sidebar.selectbox('Vehicle Combination', transport_pick_short)
map_select = st.sidebar.selectbox('Map Style', ('OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'CartoDB Dark_Matter'))

# other maps include 'Thunderforest.Neighbourhood', 'CyclOSM', 'Stamen.Watercolor', 
# BUT as these are custom... need to add 'attr' parameter to give credit

st.title("London Traffic Accident Data (2005-15)")
st.header("header")
st.subheader("subheader")
folium_static(heatmap_ts(veh_types=veh_select, map_type=map_select), width=900, height=700)





#num = st.sidebar.slider("no_veh", 1, 6)

#fig = acc_veh_combos(num_veh)
#st.pyplot(fig)
#st.pyplot(acc_veh_combos(num))



#UK MAP
#fig = plt.figure(figsize=(6,10))
#ax = fig.add_subplot()
#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)
#ax.axis('off')
#ax = plt.scatter(acc_0515['Longitude'], acc_0515['Latitude'], s =0.0001)

#st.pyplot(fig)


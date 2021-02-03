#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 21:35:37 2020

@author: adampengilly
"""

import streamlit as st

#import pandas as pd
#import numpy as np

import matplotlib.pyplot as plt
import folium
import folium.plugins as plugins
from streamlit_folium import folium_static
#import json
#import datetime
import pickle

#LOAD IN DATA
    
london = pickle.load(open('london_slim_pickle', 'rb'))

@st.cache
def df_filter(df=london, vehicle='ALL'):
    if vehicle == 'ALL':
        return  london   
    elif vehicle == 'Pedal cycle (ALL)':
        return  df[df.Veh_Type_Grouped.str.contains('Pedal')]    
    elif vehicle == 'Car (ALL)':
        return  df[df.Veh_Type_Grouped.str.contains('Car')]
    elif vehicle == 'Motorcycle (ALL)':
        return  df[df.Veh_Type_Grouped.str.contains('Motorcycle')]
    elif vehicle == 'Bus/Coach (ALL)':
        return  df[df.Veh_Type_Grouped.str.contains('Bus')]    
    elif vehicle == 'LGV/HGV (ALL)':
        return df[df.Veh_Type_Grouped.str.contains('LGV') | london.Veh_Type_Grouped.str.contains('HGV')]
    else:
        return  df[df.Veh_Type_Grouped == vehicle]


@st.cache
def trans_pick_short():
    #Heat map won't work if there is a small amount of data. Use this list of the top occuring veh_types
    transport_pick_short = list(london.Veh_Type_Grouped.value_counts().sort_values(ascending=False)[:20].index)
    transport_pick_short.insert(0,'ALL') #insert to start of list
    transport_pick_short.insert(1,'Pedal cycle (ALL)')
    transport_pick_short.insert(2,'Car (ALL)')
    transport_pick_short.insert(3,'Motorcycle (ALL)')
    transport_pick_short.insert(4,'Bus/Coach (ALL)')
    transport_pick_short.insert(5,'LGV/HGV (ALL)')
    return tuple(transport_pick_short)
transport_pick_short = trans_pick_short()

#Function that plots accidents by vehicle type over london over time
def heatmap_ts(df=london, veh_types='ALL', map_type='OpenStreetMap'):  
    
    time_index = []
    lat_long_monthly =[]
    for year in range(2005,2016):
        for month in range(1,13):
            idx = "'"+str(year)+', '+str(month)+"'"
            time_index.append(idx)
            lat_long_monthly.append(df.loc[idx][['Latitude', 'Longitude']].values.tolist())
   
    f = folium.Figure(width=50, height=40) #for some reason the map is too small in this notebook and can't be rescaled. Adding this figures is a way to allow resizing
    m = folium.Map([51.5080, -0.1], tiles=map_type, zoom_start=11)
    f.add_child(m)
    
    hm = plugins.HeatMapWithTime(
        lat_long_monthly,
        index=time_index,
        auto_play=True,
        max_opacity=0.4
    )
    hm.add_to(m)
    
    return m


#START OF PAGE INPUT...


st.title("London Traffic Accident Map (2005-15)")
#st.header("header")
#st.subheader("subheader")

#fig_size_list = range(1,10,1)

#fig_size_select = st.selectbox('Fig. Size', fig_size_list)
veh_select = st.selectbox('Vehicle Combination', transport_pick_short)

# other maps include 'Thunderforest.Neighbourhood', 'CyclOSM', 'Stamen.Watercolor', 
# BUT as these are custom... need to add 'attr' parameter to give credit

#Return a Dataframfe with the select vehicles types in
df = df_filter(london, vehicle=veh_select)

#LONDON ACCIDENT PLOT

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot()    
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.axis('off')
ax = plt.scatter(london['Longitude'], london['Latitude'], s =4)
ax = plt.scatter(df['Longitude'], df['Latitude'], s =1.5, color='orange')
plt.legend(['Total', 'Selected Vehicle/s'], markerscale=3)
st.pyplot(fig)

#HEATMAP
st.header("Accident Heat Map")
st.subheader("Each frame represents a month of data for the selected vehicle/s. Zoom in to see accident spots in detail (watch out for roundabouts!)")
map_select = st.selectbox('Map Style', ('OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'CartoDB Dark_Matter'))
folium_static(heatmap_ts(df=df, veh_types=veh_select, map_type=map_select), width=1200, height=700)




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


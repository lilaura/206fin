# Laura Li, Ariel Huang
# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import requests
import time

import pandas as pd
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np 
plotly.tools.set_credentials_file(username='ilaurali', api_key = 'BQa9lpMPhgZinYACdL1l')

def write_csv(calc_file, calc_lst, elev_dict):
    with open(calc_file,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['lgn','lat','temperature','wind speed','precipitation', 'visibility'])
        for row in calc_lst:
            csv_out.writerow(row)
        csv_out.writerow([])   
        csv_out.writerow(['state', 'average elevation of airports'])
        for a,b in elev_dict.items():
            csv_out.writerow([a,b])
    


def calc_avg_elev(conn, cur):
    cur.execute('SELECT state, elevation FROM Airports ORDER BY state')
    avg_elev={}
    for row in cur:
        state=row[0]
        elevation=row[1]
        avg_elev[state]=avg_elev.get(state,[])+([elevation])
    for key in avg_elev:
        avg_elev[key]=sum(avg_elev[key])/len(avg_elev[key])
    return avg_elev

def map_calc(conn,cur):
    d = []
    cur.execute('SELECT temp_high, temp_low,latitude, longitude, precip_int, wind_speed, visibility from Weather')
    for row in cur:
        d.append([row[3], row[2], row[5], (row[0]+row[1])/2, row[4], row[6]])
    d = sorted(d, key=lambda row: row[2], reverse=True)
    return d

def bubble_map(csvfile):
    df = pd.read_csv(csvfile,nrows=321)
    
    df.head()

    df['text'] = 'Wind Speed: ' + (df['wind speed']).astype(str) + '<br>Visibility: ' + (df['visibility']).astype(str) + '<br>Precipitation: ' + (df['precipitation']).astype(str)
    limits = [(0,6),(7,41),(42,92),(93,141),(142,320)]
    legends = [(73,79),(69,72),(63,69),(53,63),(2,53)]
    colors = ["red","yellow","green","blue","lightgrey"]
    airports1 = []

    for i in range(len(limits)):
        lim = limits[i]
        leg = legends[i]
        df_sub = df[lim[0]:lim[1]]
        port = go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['lgn'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = go.scattergeo.Marker(
                size = df_sub['temperature']*4,
                
                color = colors[i],
                line = go.scattergeo.marker.Line(
                    width=0.5, color='rgb(40,40,40)'
                ),
                sizemode = 'area'
            ),
            name = '{0} - {1} miles/hour'.format(leg[0],leg[1]) )
        airports1.append(port)

    layout = go.Layout(
            title = go.layout.Title(
                text = "Today's wind speed and temperature at airports in US\nSize: Temperature\nColor: Wind Speed"
            ),
            showlegend = True,
            geo = go.layout.Geo(
                scope = 'usa',
                projection = go.layout.geo.Projection(
                    type='albers usa'
                ),
                showland = True,
                landcolor = 'rgb(217, 217, 217)',
                subunitwidth=1,
                countrywidth=1,
                subunitcolor="rgb(255, 255, 255)",
                countrycolor="rgb(255, 255, 255)"
            )
        )

    fig = go.Figure(data=airports1, layout=layout)
    py.plot(fig, filename='airports-bubblemap',auto_open = True)

def sort_elev_top_ten(avg_elev):
    top_sort=sorted(avg_elev.items(),key=lambda t: t[1],reverse=True)
    return top_sort[:10]

def barchart_avg_elev_by_state(top_elev_dict):
    x=[]
    y=[]
    for item in top_elev_dict:
        x.append(item[0])
        y.append(item[1])
    fig, ax=plt.subplots()
    ax.bar(x,y)
    ax.set_xlabel('State')
    ax.set_ylabel('Average elevation of all airports')
    ax.set_title('Top10 States in average airport elevation')
    fig.savefig('Top10States_avg_airport_elevation.png')
    plt.show()


if __name__ == "__main__":
    conn=sqlite3.connect('db_fin_new.sqlite')
    cur=conn.cursor()
    elev_dict=calc_avg_elev(conn,cur)
    top_elev_dict=sort_elev_top_ten(elev_dict)
    

    map_dict = map_calc(conn,cur)
    write_csv("calc.csv",map_dict,elev_dict)
    bubble_map("calc.csv")
    barchart_avg_elev_by_state(top_elev_dict)


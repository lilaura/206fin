# Import statements
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
import json
import requests
import time

def write_calculation(calc_file, calc_dict):

    dumped_json = json.dumps(calc_dict) # serialize dictionary to a JSON formatted string 
    fw = open(calc_file,"w") # open the cache file
    fw.write(dumped_json) # write the JSON
    fw.close() 

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

def avg_temp(conn,cur):
    d = {}
    templist = []
    preciplist = []
    vislist = []
    lnglist = []
    latlist = []
    windlist = []
    cur.execute('SELECT temp_high, temp_low,latitude, longitude, precip_int, wind_speed, visibility from Weather')
    for row in cur:
        templist.append((row[0]+row[1])/2)
        preciplist.append(row[4])
        vislist.append(row[6])
        latlist.append(row[2])
        windlist.append(row[5])
        lnglist.append(row[3])
    d["longitude"] = lnglist
    d["latitude"] = latlist
    d["temprature"] = templist
    d["visibility"] = vislist
    d["precipitation"] = preciplist
    d["wind speed"] = windlist
    return d

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
    fig.savefig('Top10 States in average airport elevation.png')
    plt.show()


if __name__ == "__main__":
    conn=sqlite3.connect('db_fin_new.sqlite')
    cur=conn.cursor()
    elev_dict=calc_avg_elev(conn,cur)
    top_elev_dict=sort_elev_top_ten(elev_dict)
    write_calculation("calc.json",elev_dict)

    map_dict = avg_temp(conn,cur)
    z = {}
    z["elevation"] = elev_dict
    z["map data"] = map_dict
    write_calculation("calc.json",z)

    barchart_avg_elev_by_state(top_elev_dict)


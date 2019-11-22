from pymongo import MongoClient
import folium
import pandas as pd
import json


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies','starbucks')

#filtering for wanted lists
starbucks = list(coll.find({"name":"Starbucks"}))
mycompanies = list(coll.find({"name":{"$exists":True}}))


#on folium
map_city = folium.Map(location=[40.707122, -74.004981], zoom_start=12)

for branch in starbucks:
    folium.Marker(branch['geolocation']['coordinates'][::-1],
                    radius=2,
                    icon=folium.Icon(icon='cloud',color='red'), 
                   ).add_to(map_city)
    
for company in mycompanies:
    folium.Marker(company['geolocation']['coordinates'][::-1],
                    radius=2,
                    icon=folium.Icon(icon='cloud',color='blue'), 
                   ).add_to(map_city)


map_city


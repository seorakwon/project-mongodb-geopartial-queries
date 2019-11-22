from pymongo import MongoClient
import folium
import pandas as pd
import json


def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies','starbucks1')
db, coll = connectCollection('companies','mycompanies')
db, coll = connectCollection('companies', 'vegan1')



#filtering for wanted lists
starbucks = list(coll.find({"name":"Starbucks"}))
mycompanies = list(coll.find({"name":{"$exists":True}}))
vegan = list(coll.find({"name": {"$exists": True}}))


#on folium - locating starbucks, vegan restaurants and selected offices

map_city=folium.Map(location=[40.707954, -74.011114], zoom_start=12)

for branch in starbucks:
    folium.Marker(branch['geolocation']['coordinates'][::-1],
                    radius=5000,
                    icon=folium.Icon(icon='cloud',color='red'), 
                   ).add_to(map_city)

for company in mycompanies:
    folium.Marker(company['geolocation']['coordinates'][::-1],
                 radius = 1000, 
                 icon = folium.Icon(icon = 'cloud', color = 'blue'),
                 ).add_to(map_city)

for rest in vegan:
    folium.Marker(rest['geolocation']['coordinates'][::-1],
                 radius = 1000, 
                 icon = folium.Icon(icon = 'cloud', color = 'green'),
                 ).add_to(map_city)

map_city

map_city


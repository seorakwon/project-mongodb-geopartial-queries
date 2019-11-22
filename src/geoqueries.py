from pymongo import MongoClient
import pandas as pd

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies','starbucks1')
db1, coll1 = connectCollection('companies', 'vegan1')

# function to get the number of starbucks/restaurants within a distance from each company location
def getClose(lat, long,radius = 1000):
    db, coll = connectCollection('companies', 'starbucks1')
    results = coll.find({
        "geolocation":{
            "$near":{
                "$geometry":{
                    "type":"Point",
                    "coordinates":[lat,long]
                },
                "$maxDistance": 1000,
            }
        }
    })
    return list(results)

def getClose2(lat, long,radius = 1000):
    db, coll = connectCollection('companies', 'vegan1')
    results = coll.find({
        "geolocation":{
            "$near":{
                "$geometry":{
                    "type":"Point",
                    "coordinates":[lat,long]
                },
                "$maxDistance": 1000,
            }
        }
    })
    return list(results)


#calling radius function
c1star = getClose(-74.011114,40.707954)
print(len(c1star))
c1veg = getClose2(-74.011114,40.707954)
print(len(c1veg))

c2star = getClose(-74.0136605,40.7078343)
print(len(c2star))
c2veg = getClose2(-74.0136605,40.7078343)
print(len(c2veg))

c3star = getClose(-73.994797, 40.727216)
print(len(c3star))
c3veg = getClose2(-73.994797, 40.727216)
print(len(c3veg))

c4star = getClose(-73.990967, 40.73343)
print(len(c4star))
c4veg = getClose2(-73.990967, 40.73343)
print(len(c4veg))

c5star = getClose(-73.987764, 40.744618)
print(len(c5star))
c5veg = getClose2(-73.987764, 40.744618)
print(len(c5veg))


c6star = getClose(-73.985506, 40.757929)
print(len(c6star))
c6veg = getClose2(-73.985506, 40.757929)
print(len(c6veg))


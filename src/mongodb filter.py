from pymongo import MongoClient
import pandas as pd
import re
import folium

def connectCollection(database, collection):
    client = MongoClient()
    db = client[database]
    coll = db[collection]
    return db, coll

db, coll = connectCollection('companies','companies')


# mongodb queries (offices with less than 10 years, that have not gone bankrupt, and that have the latitute). The colum for total money raised has also been chosen as not empty.
extraer = [
    { "$unwind": "$offices"},
    {"$match": {"$and":
            [{"founded_year": {"$gte": 2009}},
             {"deadpooled_year": None},
             {"total_money_raised": {"$exists": True, "$ne": "$0"}},
             {"offices.latitude": {"$exists": True, "$ne": None}},
             {"offices.longitude": {"$exists": True, "$ne": None}}]}}]

oficinas_fuera = list(coll.aggregate(extraer))


# function to get the coordinates and add them as a new field
def getLocation(companies):
    for i in range(len(companies['offices'])):
        longitude = companies['offices']['longitude']
        latitude = companies['offices']['latitude']
        loc = {
            'type':'Point',
            'coordinates':[longitude, latitude]
        }
        return loc

for cp in oficinas_fuera:
    value = {"$set": {'geolocation':getLocation(cp)}}
    coll.update_one(cp, value)


# converting the json into a pandas dataframe
companies_df = pd.DataFrame(oficinas_fuera)


# choosing columns that are relevant for the project
companies_df1 = companies_df[["name","category_code","founded_year","total_money_raised","geolocation"]]


# the categories relevant have been changed to a group name:tech, in order to be able to eliminate others
category_list = {'web': 'tech', 'games_video': 'tech', 'software':'tech', 'advertising':'tech', 
                 'mobile':'tech', 'ecommerce':'tech', 'biotech':'tech', 'search':'tech',
                 'cleantech':'tech','hardware':'tech', 'netword_hosting':'tech', 'security':'tech', 
                 'analytics':'tech'}
        
companies_df2 = companies_df1.replace(to_replace = category_list, inplace=False) 
companies_df3 = companies_df2[['tech' in x for x in companies_df2['category_code']]]


#  now the column for total_money_raised is handled, where if M is in, it is kept, otherwise rows deleted.
# the values were in k's and M's, and as the condition is $1M, and it is the lowest currency, it was assumend that if it had M, it was at least 1M$
companies_df3.total_money_raised = companies_df3.total_money_raised.str.replace(r'(\d+)([A-Za-z])', r'\1 \2')
companies_df3 = companies_df3[['M' in x for x in companies_df3['total_money_raised']]]


# index reset
companies_df3 = companies_df3.reset_index(drop=True)


# export dataframe to json
companies_df3.to_json('./mycompanies_clean.json', orient='records')

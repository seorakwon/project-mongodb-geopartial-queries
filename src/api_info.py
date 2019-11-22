import requests
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd


# yellp request function
def requestyelp(business):
    yelp_api_key = os.getenv("YELP_API_KEY")
    if not yelp_api_key:
        raise ValueError("No key provided")
    else:
        print("The key provided is: ", yelp_api_key[0:5])

    url='https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer %s' % yelp_api_key}

    info = []
    for offset in range(0, 1000, 50):
        params = {'limit': 50,'term':business,'location':'new york','offset': offset, 'radius':5000}
        req=requests.get(url, params=params, headers=headers)

        if req.status_code == 200:
                info += req.json()['businesses']
        elif req.status_code == 400:
                print('400 Bad Request')
                break
                      
    print('The status code is {}'.format(req.status_code))
    
    return info

starbucks = requestyelp("starbucks")
vegan = requestyelp("vegan")


# function to get relevant columns out of the json file
def tabla(company):
    info = []
    for i in company:
        venues={ 
            'name': i['name'],
            'categories': i['alias'],
            'city': i['location']['city'],
            'geolocation': {'type': 'Point', 'coordinates':[i['coordinates']['longitude'],i['coordinates']['latitude']]}                    }
        info.append(venues)
    company_info = pd.DataFrame(info)
    return company_info

starbucks_df = tabla(starbucks)
vegan_df = tabla(vegan)


# filter for real Starbucks
starbucks_df = starbucks_df[['Starbucks' in x for x in starbucks_df['name']]]
vegan_df = vegan_df[['vegan' in x for x in vegan_df['name']]]


#output to json file
starbucks_df.to_json('./starbucks1_api.json', orient='records')
vegan_df.to_json('./vegan1_api.json', orient='records')




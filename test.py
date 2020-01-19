import json
import time
from urllib import request
import pandas as pd
from pickling import unpickle_data

df = unpickle_data('data/df_listing.pickle')

def get_coordinates(address):
    map_key= 'AIzaSyCZHQIOMDfWZkpS-fbYVijURAEuq51xUnY'
    address = address.strip()
    address = address.replace(',','').replace(' ','+').replace('#','')

    url_ = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+ map_key

    try:
        response = request.urlopen(url_)
        time.sleep(.05)
    except Exception as e:
        print('Error while requesting url for coordinates')
        print(e)

    result = json.loads(response.read())

    if result['status'] == 'OK':
        lat = result['results'][0]['geometry']['location']['lat']
        lng = result['results'][0]['geometry']['location']['lng']
        return (lat, lng)

    else:
        print('Error while getting coordinates. \naddress: '+address+'\nresult[status]')
        raise Exception(result['status'])



addresses = df.loc[15:20,'address']
print(addresses)
for adr in addresses:
    (lat, lng) = coordinates(adr)
    print(lat,lng)

#print(lat,lng)

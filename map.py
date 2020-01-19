import folium
import time
from config import map_name
from urllib import request
import json

def get_coordinates(address):
    map_key= 'AIzaSyCZHQIOMDfWZkpS-fbYVijURAEuq51xUnY'
    address = address.strip()
    address = address.replace(',','').replace(' ','+').replace('#','')

    url_ = 'https://maps.googleapis.com/maps/api/geocode/json?address='+address+'&key='+ map_key

    try:
        response = request.urlopen(url_)
        time.sleep(1)
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

def create_map(df):

    if df.empty:
        print('No houses found undervalued')
        return

    df.reset_index(inplace=True)
    df.loc[:,'lat'] = 0
    df.loc[:,'lon'] = 0

    # get coordinates
    i=0
    try:
        for addrs in list(df['address']):
            (lat, lng) = get_coordinates(addrs)
            print(i,lat,lng,addrs)
            df.loc[i, 'lon'] = lng
            df.loc[i, 'lat'] = lat
            i+=1
    except Exception as e:
        print('error while obtaining coordinates')
        print(e)

    # get mls link
    def get_mls_link(x):
        mls = x.strip().split(' ')[-1]
        mls = 'https://www.har.com/search/dosearch?for_sale=1&mlsnum='+mls
        return mls

    df.loc[:,'mls_link'] = df['mls']

    for i in range(len(df['mls'])):
        df.at[i,'mls_link'] = get_mls_link(df.loc[i,'mls'])

    # TODO: edit map url to open link in new tab

    # create map
    map = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=13)
    fg = folium.FeatureGroup(name='My_Map')

    for i in list(df.index.values):
        pop_up_text = df.loc[i,'mls']+'\nUndervalued: $'+str(int(df.loc[i,'undervalue_delta']))
        my_popup = folium.Popup('<a href='+df.loc[i,'mls_link']+'>'+pop_up_text+'</a>')
        fg.add_child(folium.Marker(location=[df.loc[i,'lat'], df.loc[i,'lon']], popup=my_popup, icon=folium.Icon(color=df.loc[i,'tag_color'])))

    map.add_child(fg)
    map.save('./folium/'+map_name+'.html')



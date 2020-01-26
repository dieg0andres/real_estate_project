import bs4 as bs
from requests import get
import pandas as pd
from statistics import mean
from config import param


def get_url(zip_code, page, min_p, max_p, bedroom_min, bath_min):
    url_ = 'https://www.har.com/search/soldsearch?page='+str(page)+'&sort=closedate&region_id=1&soldperiod=2&property_class_id=1&' \
           'zip_code='+str(zip_code)+'&listing_price_min='+str(min_p)+'&listing_price_max='+str(max_p)+'&bedroom_min='+str(bedroom_min)+'&full_bath_min='+str(bath_min)+'&for_sale=1&' \
           'streetaddress=&city=&subdivisions=&nid=&map_tools_nwlat=&map_tools_nwlng=&map_tools_selat=&map_tools_selng=&' \
           'map_tools_polygon=&fips_code=&schoolid=&mlsnum=&property_status=&bedroom_max=&full_bath_max=&square_feet_min=&' \
           'square_feet_max=&year_built_min=&year_built_max=&stories=&lotsize_min=&lotsize_max=&style=&garage_num=&' \
           'garage_desc=&price_sqft_min=&price_sqft_max=&mlsnums=&listing_officeid=&listing_agentid=&search_id=&community=&hoa_fee_max='
    return url_

def scrape_page(url_):

    response = get(url_)

    if response.status_code != 200:
        raise Exception('response from zillow was: {}'.format(response.status_code))

    soup = bs.BeautifulSoup(response.text, 'lxml')

    properties = soup.find_all('div', class_='prop_item status-sold')

    prop = {
            'mls' : [],
            'price' : [],
            'max_p' : [],
            'min_p' : [],
            'avg_p' : [],
            'address' : [],
            'zip' : [],
            'style' : [],
            'bed' : [],
            'bath' : [],
            'yr_built' : [],
            'sqft' : [],
            'pool' : [],
            'garage' : []
        }

    for p in properties:
        prop['mls'].append(p.find('div', class_='mpi_mls').text.strip())
        prop['price'].append(p.find('div', class_='price').text.strip())
        prop['max_p'].append(int(prop['price'][-1].replace(',','').replace('$','').replace('$','').split('-')[1]))
        prop['min_p'].append(int(prop['price'][-1].replace(',','').replace('$','').replace('$','').split('-')[0]))
        prop['avg_p'].append(mean([prop['max_p'][-1],prop['min_p'][-1]]))
        prop['address'].append(p.find('a',class_='address').text.strip())
        prop['zip'].append(prop["address"][-1][-5:])
        prop['style'].append(p.find('p').text.strip())

        for item in p.find_all('div', class_='mpf_item'):
            if 'Bed' in item.text: prop['bed'].append(int(item.text.strip()[0]))
            if 'Full' in item.text: prop['bath'].append(float(item.text[1]))
            if 'Half' in item.text: prop['bath'][-1] += float(item.text[ item.text.index('Half') -2])/2.
            if 'Built' in item.text: prop['yr_built'].append(int(item.text[-4:].strip()))
            if 'Building Sqft' in item.text: prop['sqft'].append(int(item.text.replace('.','').replace(',','').strip()[:4]))
            if 'Has Private Pool' in item.text: prop['pool'].append(True)
            if 'Garage' in item.text: prop['garage'].append(int(item.text.strip()[0]))

        if len(prop['yr_built']) < properties.index(p) + 1: prop['yr_built'].append(None)
        if len(prop['sqft']) < properties.index(p) + 1: prop['sqft'].append(None)
        if len(prop['pool']) < properties.index(p) + 1: prop['pool'].append(False)
        if len(prop['garage']) < properties.index(p) + 1: prop['garage'].append(None)

    length = len(prop['mls'])
    for key in prop.keys():
        if length != len(prop[key]):
            raise Exception('not all lists have same length in HAR_sold_scraping!')

    df = pd.DataFrame(prop)
    return df

def scrape_har_sold():

    df_master = pd.DataFrame()

    step = 50000
    min_prices = range(param['price_min'],param['price_max'],step)
    max_prices = range(param['price_min']+step,param['price_max']+step,step)

    for zip_ in param['zip']:

        print('scraping HAR_sold zip: '+str(zip_))
        for (min_p, max_p) in zip(min_prices,max_prices):

            page = 1
            while True:

                df = scrape_page( get_url(zip_, page, min_p, max_p, param['bedroom_min'], param['bath_min']))
                df_master = pd.concat([df_master,df], ignore_index=True)
                page +=1

                if df.empty: break

    return df_master

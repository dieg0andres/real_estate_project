import bs4 as bs
from requests import get
import pandas as pd
from config import param


def get_url(zip_code, page, min_p, max_p, bedroom_min, bedroom_max, bath_min, bath_max):
    url_ = 'https://www.har.com/search/dosearch/?page='+str(page)+'&for_sale=1&zip_code='+str(zip_code)+\
           '&listing_price_min='+str(min_p)+'&listing_price_max='+str(max_p)+'&bedroom_min='+\
           str(bedroom_min)+'&bedroom_max='+str(bedroom_max)+'&full_bath_min='+str(bath_min)+'&full_bath_max='+str(bath_max)
    return url_

def scrape_page(url_):

    response = get(url_)
    soup = bs.BeautifulSoup(response.text,'lxml')
    properties = [x.parent for x in soup.find_all('div', class_ = 'mpi_info')]

    mls = []
    price = []
    address = []
    zip = []
    style = []
    bed = []
    bath = []
    new_construction = []
    yr_built = []
    sqft = []
    pool = []
    garage = []

    for prop in properties:
        mls.append(prop.find('div', class_='mpi_mls').text.strip())
        price.append(int(prop.find('div', class_='price').text.strip().replace(' ','').replace('$','').replace(',','')))
        address.append(prop.find('a', class_ = 'address').text.strip())
        zip.append(address[-1][-5:])
        style.append(prop.find('p').text)

        # get property attributes
        attributes = prop.find_all('div', class_='mpf_item')

        bed.append(int(attributes[0].text[0]))
        bath.append(float(attributes[1].text.replace('.', '')[0]))

        # half baths
        try: bath[-1]+= float(attributes[1].text[attributes[1].text.index('Half') - 2])/2
        except: pass

        try:    new_construction.append(prop.find('span', title='new construction').text)
        except: new_construction.append(False)

        for item in attributes:
            if 'Built in' in item.text: yr_built.append(int(item.text[-4:].strip().strip(',')))
            if 'Building Sqft' in item.text: sqft.append(int(item.text.split(' ')[0].strip().strip('.').replace(',','')))
            if 'Has Private Pool' in item.text: pool.append(True)
            if 'Garage' in item.text: garage.append(int(item.text[0]))

        if len(yr_built) < properties.index(prop) + 1: yr_built.append(None)
        if len(sqft) < properties.index(prop) + 1: sqft.append(None)
        if len(pool) < properties.index(prop) + 1: pool.append(False)
        if len(garage) < properties.index(prop) + 1: garage.append(None)

    prop_dict = {
        'mls' : mls,
        'price' : price,
        'address' : address,
        'zip' : zip,
        'style' : style,
        'bed' : bed,
        'bath' : bath,
        'new_construction' : new_construction,
        'yr_built' : yr_built,
        'sqft' : sqft,
        'pool' : pool,
        'garage' : garage
    }

    length = len(price)
    for key in prop_dict.keys():
        if length != len(prop_dict[key]):
            raise Exception('not all lists have same length in HAR_listing_scraping!')

    df = pd.DataFrame(prop_dict)
    return df

def scrape_har_listing():

    df_master = pd.DataFrame()

    step = 50000
    min_prices = range(param['price_min'],param['price_max'],step)
    max_prices = range(param['price_min']+step,param['price_max']+step,step)

    for zip_ in param['zip']:

        print('scraping HAR_listing zip: ' + str(zip_))
        for (min_p, max_p) in zip(min_prices,max_prices):

            page = 1
            while True:

                df = scrape_page(get_url(zip_, page, min_p, max_p, param['bedroom_min'], param['bedroom_max'],\
                                         param['bath_min'], param['bath_max']))
                df_master = pd.concat([df_master,df], ignore_index=True)
                page +=1

                if df.empty: break

    return df_master

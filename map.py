import folium
from analysis_market import run_analysis
from selenium import webdriver
import time
from config import map_name


def setup_webdriver():
    driver = -1
    try:
        driver = webdriver.Firefox(executable_path = './geckodriver')
        driver.set_window_position(-150000, 150000)
        driver.set_page_load_timeout(60)

    except Exception as e:
        msg = 'an error occurred while setting up webdriver\n' + str(e)
        print(msg)

    finally:
        return driver


def create_map(df):

    if df.empty:
        print('No houses found undervalued')
        return

    df.reset_index(inplace=True)
    df.loc[:,'lat'] = 0
    df.loc[:,'lon'] = 0

    driver = setup_webdriver()

    # get coordinates
    i = 0
    try:
        for addrs in list(df['address']):

            driver.get('https://www.google.com/maps')
            time.sleep(5)
            driver.find_element_by_xpath("//input[@class='tactile-searchbox-input']").send_keys(addrs)
            time.sleep(1)
            driver.find_element_by_xpath("//button[@id='searchbox-searchbutton']").click()
            time.sleep(9)

            url_ = str(driver.current_url)
            url_ = url_.split(',')

            df.loc[i, 'lon'] = float(url_[-2])
            df.loc[i, 'lat'] = float(url_[-3].split('@')[-1])

            print('got coordinates for',i+1)
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

    driver.close()

    # create map
    map = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=13)
    fg = folium.FeatureGroup(name='My_Map')

    for i in list(df.index.values):
        pop_up_text = df.loc[i,'mls']+'\nUndervalued: $'+str(int(df.loc[i,'undervalue_delta']))
        my_popup = folium.Popup('<a href='+df.loc[i,'mls_link']+'>'+pop_up_text+'</a>')
        fg.add_child(folium.Marker(location=[df.loc[i,'lat'], df.loc[i,'lon']], popup=my_popup, icon=folium.Icon(color=df.loc[i,'tag_color'])))

    map.add_child(fg)
    map.save('./folium/'+map_name+'.html')

    return df



df_value = run_analysis()

print(df_value.head())
print(df_value.shape)

df=create_map(df_value)


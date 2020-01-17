from har_listing_scraping import scrape_har_listing
from har_sold_scraping import scrape_har_sold
import threading
from pickling import pickle_df
from analysis_market import run_analysis

def listing_thread():
    df = scrape_har_listing()
    pickle_df('./data/df_listing.pickle',df)

def sold_thread():
    df = scrape_har_sold()
    pickle_df('./data/df_sold.pickle', df)

def run_scraping():
    t_list = threading.Thread(target=listing_thread)
    t_sold = threading.Thread(target=sold_thread)

    t_list.start()
    t_sold.start()

    t_list.join()
    t_sold.join()

    print('\ndone scraping')

def main():

    run_scraping()
    run_analysis()



if __name__ == '__main__':
    main()
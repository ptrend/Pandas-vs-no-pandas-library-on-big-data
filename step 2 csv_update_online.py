'''
updating online car_list_csv.csv file
args : car_list_csv.csv
returns: car_list_csv_updated.csv
info: scraping data from autocentrum.pl I have missed that electric cars
     have diffrent html table for range
     also new column: battery will be added to dataframe
     data not fully comparable some producers show:
         Maksymalny zasięg przy oszczędnej jeździe na długiej trasie,
         or
         Średni maksymalny zasięg
'''

import pandas as pd

df = pd.read_csv('car_list_csv.csv', sep = ';', encoding="utf-8-sig", index_col = False)
# we have 143 electric cars 
# print('Electric car rows: ', (df['car_engine_type'] == 'elektryczny').sum())
# show rows
# print(df[df['car_engine_type'] == 'elektryczny'])
# print(df.loc[df['car_engine_type'] == 'elektryczny', :])

# electric cars id and link to dictionary without numeric index
df_electric = df[df['car_engine_type'] == 'elektryczny'][['car_id', 'link']].set_index('car_id')
my_dict = df_electric['link'].to_dict()
my_dict_len = len(my_dict)
item_counter = 0

import requests
from scrapy import Selector
import re
from datetime import datetime
import time
import os
import numpy as np

def get_values(link):
    request_object = requests.get(link)
    # response_200 = request_object.status_code 
    html = request_object.content
    sel = Selector(text = html)
    try:
        range_km_string = sel.xpath('//div[@data-label = "Maksymalny zasięg przy oszczędnej jeździe na długiej trasie"]/following-sibling::div[1]/span[1]/text()').extract()[0]
    except:
        range_km_string = sel.xpath('//div[@data-label = "Średni maksymalny zasięg"]/following-sibling::div[1]/span[1]/text()').extract()[0]
    battery_string = sel.xpath('//div[@data-label = "Pojemność akumulatora"]/following-sibling::div[1]/span[1]/text()').extract()[0]
    range_km_numeric = int(re.findall(r'\d+', range_km_string)[0])
    battery_numeric = int(re.findall(r'\d+', battery_string)[0])
    return (range_km_numeric, battery_numeric)

if not os.path.isfile('electric_set.csv'):
    start_time = datetime.now()
    my_result_dict = {}
    for car_id, link in my_dict.items():
        error_counter = 0
        item_counter += 1
        while error_counter != 3:
            try:
                my_result_dict[car_id] = get_values(link)
                print(f'{round(100 * (item_counter / my_dict_len), 1)} %')
                break
            except:
                print(f'error {error_counter + 1}\non car_id: {car_id},\nlink: {link}')
                time.sleep(0.5) # 3 seconds bettter for sleep, if error due to internet conection will try again, until error_counter == 3
                my_result_dict[car_id] = [0, 0]
                error_counter += 1

    import pickle
    # df_electric assign new data
    df_electric = pd.DataFrame.from_dict(my_result_dict, orient='index', columns = ['range_km', 'battery_kwh']).reset_index()
    
    if (df_electric['range_km'] > 0).sum() < (item_counter / 2):
        print('Check internet connection, not all data downloaded')
    else:
        df_electric.reset_index()
        df_electric.to_csv('electric_set.csv', sep = ';', encoding="utf-8-sig", index = False)
        pickle.dump(my_result_dict, open('filename.pickle', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        end_time = datetime.now()
        d_count = (df_electric['range_km'] > 0).sum()
        print(f'\n\nScraping time: {end_time - start_time}{chr(10)}Downloaded {d_count}')
else:
    print('Electric car set file exists:''\n{}'.format(os.path.realpath('electric_set.csv')))
# from df

df_electric = pd.read_csv('electric_set.csv', sep = ';').rename({'index' : 'car_id'}, axis = 1)
df['battery_kwh'] = np.nan

# from df_electric
# by update range_km -> range_city,  needs index
def change_by_update():
    global df_electric
    global df
    df_electric.set_index('car_id', inplace = True)
    df.set_index('car_id', inplace = True)
    df['range_city'].update(df_electric['range_km'])
    df['battery_kwh'].update(df_electric['battery_kwh'])

# using dictionary made from dataframe
# print(df_dict.keys()) # keys 'range_km', 'battery_kwh', we have dict level  0 and 1
# dict.get(key) metod may be sometimes more accurate ->do not raise error 
# with no automatic handling errors, in this case I want to see if there is somtehing missing
    
def change_by_dict_1(): # dict made from df_df_electric, iterating dict keys
    df_dict = df_electric.set_index('car_id').to_dict()
    for key, value in df_dict['range_km'].items():
        df.loc[df['car_id'] == key, 'range_city'] = value
    for key, value in df_dict['battery_kwh'].items():
        df.loc[df['car_id'] == key, 'battery_kwh'] = value

def change_by_dict_2(): # more elegant way, we know keys so just iterate range_km or battery_kwh keys:
    df_dict = df_electric.set_index('car_id', inplace=True).to_dict()
    for key, value in df_dict['range_km'].items():
        df.loc[df['car_id'] == key, ['range_city', 'battery_kwh']] = [value, df_dict['battery_kwh'][key]]
        
def change_by_list():
    df_list = df_electric.values.tolist()
    for item_i in range(0, len(df_list)):
        df.loc[df['car_id'] == df_list[item_i][0], ['range_city', 'battery_kwh']] = [df_list[item_i][1], df_list[item_i][2]]

# change_by_update()
my_change_func = {
    'by_update' : change_by_update,
    'by_dict_1' : change_by_dict_1,
    'by_dict_2' :change_by_dict_2,
    'by_list' :change_by_list
        }
# reset indexes and move col ='link' to last (long values of cell,in excel not friendly to read, most often barely used column)
def reset_indexes(x,y):
    x.reset_index(inplace = True)
    y.reset_index(inplace = True)
    move_col = x.pop('link')
    x.insert(len(x.columns), 'link', move_col)
    
# function run from dictionary
my_change_func['by_update']() # change_by_update()
reset_indexes(df, df_electric)
# updated database to new file car_list_csv_updated
df.to_csv('car_list_csv_updated.csv', sep = ';', encoding="utf-8-sig", index = False)
# Our modified rows df[df['battery_kwh'].notnull()]


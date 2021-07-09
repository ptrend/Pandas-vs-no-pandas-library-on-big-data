'''
    importing pickle data to dataframe
    args: final_data26486.pickle
    return: dataframe
    info: pickle data in list of dictionaries, each car may have different dict len,
            cos of list of dicts 'transmission', 
            key: 'transmission' value: list of transmission details
    raises: may need use encoding="utf-8-sig"
    primary items in each car data: car_id, link, car_primary, transmission
    importing data to csv if file do not exist
'''
import copy
import os
import pandas as pd
import re
import numpy as np
from datetime import datetime


class my_regex_fun_Class: # instead classes of functions maybe more readable would be dictionary of functions
    @staticmethod
    def car_digits_with_dot(val):
        try:
            return float(re.search(r'[0-9]+.[0-9]+', val).group(0))
        except:
            return np.nan
    @staticmethod
    def car_digits_no_dot(val):
        try:
            return float(re.search(r'[0-9]+', val).group(0))
        except:
            return np.nan
    @staticmethod
    def car_prod(val):
        try:
            prod_list = re.findall(r'[0-9]+', val)
            if len(prod_list) == 1:
                prod_list.append(datetime.now().year)
        except:
            prod_list =[np.nan, np.nan]
        return prod_list

if not os.path.isfile('car_list_csv.csv'):
    if not os.path.isfile('final_data26486.pickle'):
        print(f'Please download final_data26486.pickle to current python folder: {os.getcwd()}')
    else:
        car_dataset_list = pd.read_pickle('final_data26486.pickle')
        car_list = []
        for car_item in car_dataset_list:
            temp_dict = {}
            temp_dict['car_id'] = car_item['car_id']
            temp_dict['link'] = car_item['link']
            temp_dict.update(car_item['car_primary'])
            for el in range(len(car_item['transmission'])):
                temp_dict_copy = copy.deepcopy(temp_dict)
                temp_dict_copy.update(car_item['transmission'][el])
                car_list.append(temp_dict_copy)
                
        df = pd.DataFrame(car_list)

        for el in ['diameter', 'radius', 'acceleration', 'fuel_ave', 'fuel_road', 'fuel_city']:
            df[el] = df[el].apply(my_regex_fun_Class.car_digits_with_dot)

        for el in ['car_length', 'car_width', 'car_width_mirrors', 'car_height', 'car_height_plus_railings',
                   'car_height_plus_back_doors', 'car_axes_length', 'car_wheels_front_width','car_wheels_back_width',
                   'car_clearance', 'car_trunk_max', 'car_trunk_min', 'car_engine_v', 'V_max', 'V_fuel',
                   'range_ave', 'range_road', 'range_city', 'co2', 'weight_min', 'weight_max']:
            df[el] = df[el].apply(my_regex_fun_Class.car_digits_no_dot)
            
        df['start_prod'] = df['car_engine_produced'].apply(lambda x : my_regex_fun_Class.car_prod(x)[0])
        df['end_prod'] = df['car_engine_produced'].apply(lambda x : my_regex_fun_Class.car_prod(x)[1])
        
        move_col = df.pop('start_prod')
        df.insert(df.columns.get_loc("car_engine_produced") + 1, 'start_prod', move_col)
        move_col = df.pop('end_prod')
        df.insert(df.columns.get_loc("car_engine_produced") + 2, 'end_prod', move_col)
        move_col = df.pop('link')
        df.insert(len(df.columns), 'link', move_col)
        
        df.to_csv('car_list_csv.csv', sep = ';', encoding="utf-8-sig", index = False)
            

df = pd.read_csv('car_list_csv.csv', sep = ';', encoding="utf-8-sig", index_col = False)
print(df.info())
print(df.head())





'''
Let`s see how CO2, power, fuel consumption, ... changed in last ~30 years.
We can compare one chosen producer or group of producers.
Comparing we have to slice data, separate premium / sport cars from cars for "people" :)
lets take: 
'''

'''
easier would be using pandas but, let`s try use list of dictionaries placed in 'final_data26486.pickle'
we will try write our own functions, group and aggregate them, simple python code no pandas library
'''

import pickle
import sys
import os
import re
from collections import Counter

    # Spyder Ide used, clearing console
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
except:
    pass  

from inspect import currentframe
def code_line_number(line_no):
    print('\nLast executed Code line:', line_no - 1,'\n')
    print('_' * 40 ,'\n')


if not os.path.isfile('final_data26486.pickle'):
    print('No file : final_data26486.pickle')
    sys.exit()
if not os.path.isfile('slice_data.pickle'):    
    with open('final_data26486.pickle', 'rb') as file:
        full_car_list = pickle.load(file)
        file.close()
    # Huge size of file used 225104 . For working on this module better to filter needed data and load to another, smaller pickle   
    # create new list, but firstly let`s choose producers, we need models 4 "people" not supercars or exclusive
    # also we need producers with many different car models and models produced in years, but different generation
# print(sys.getsizeof(full_car_list))
producer_list = []
for item in full_car_list:
    producer_list.append(item['car_id'].split(' ')[0])
my_counter = Counter(producer_list)

popular_list, not_popular_list = [], []

for index, item in enumerate(my_counter):
    if my_counter[item] >= 400:
        popular_list.append([item, my_counter[item]])
    else:
        not_popular_list.append([item, my_counter[item]])

# print(not_popular_list)
# print(popular_list)      
    # how to buuble sort array in array? not needed in this case but fun to try
def array_sort(my_arr):
    arr_len = len(my_arr)
    for i_l1 in range(0, arr_len):
        for i_l2 in range(arr_len - i_l1 -1):
            if my_arr[i_l2][1] > my_arr[i_l2 + 1][1]:
                my_arr[i_l2], my_arr[i_l2 + 1] = my_arr[i_l2  + 1], my_arr[i_l2] # switch places higher with lower
    return my_arr

print(f'Unsorted popular_list\n{popular_list}\n')
popular_list = array_sort(popular_list)
print(f'Sorted popular_list\n{popular_list}\n')
# how about descending sort? we could change our function code or just simple use built-in reverse sorted array function
popular_list.reverse()
print(f'Reversed sorted popular_list\n{popular_list}\n')
code_line_number(currentframe().f_lineno)
    # make new smaller pickle
my_list = []
# for item in full_car_list:
    # here just example of using python`s nested list comprehension, 
new_list = [item for item in full_car_list if item['car_id'].split(' ')[0] in [x[0] for x in popular_list]]
    # after filtering our list we get 79,3% of item`s
print('Filtered to full data share')
print('{0:.3f}'.format(len(new_list) / len(full_car_list)))
code_line_number(currentframe().f_lineno)
    # we try to do all without filtered data to new pickle, but working on full size data, at the end see time of execution
    # now the most important apart, find engines and their properties, few models can have the same engine, 
    # the same engine may be in manual or automatic transmission
    # let`s build new list with car_id, angine properties and date of introduction to market
    # just to smaller our list, after finishing code we always could go back and nest some code: less lines but also less readability
engine_list = []    

for item in new_list:
    item_primary_data = []
    temp_item_dict = {}
        # standard informationa about car, merging string:item['car_id'] and list comprehension to one
    item_primary_data = [item['car_id']] + [
        item['car_primary'][el] for el in ['car_engine_produced', 'car_engine_v', 'car_engine_type',
                                           'car_engine_power', 'car_engine_torque', 'car_engine_cylinders']]
        # beacuse we do not work with pandas and columns names we can use list of dictionaries
    temp_item_dict_keys = ['car_id', 'car_engine_produced', 'car_engine_v', 'car_engine_type',
                           'car_engine_power','car_engine_torque', 'car_engine_cylinders'] 
    for index, item_pd in enumerate(temp_item_dict_keys):
        temp_item_dict[item_pd] = item_primary_data[index]
        # now it is a little bit tricky -> co2, fuel consumption... are list values for key: 'transmission'
        # there are one or more transmissions but we need average -> it is the same engine,
        # but results may be a little bit different because of for example FWD vs 4D, 4D consumes ~more than FWD
        # also data are in string type
    gearbox_data = item['transmission']
    fuel_ave = 0
    fuel_road = 0
    fuel_city = 0
    co2 = 0
    i_counter = 0
        # above data are crucial, without them we do not need car data
    for gearbox in gearbox_data:
        try:
            fuel_ave += float(re.search(r'[0-9]+.[0-9]+', gearbox['fuel_ave']).group(0))
            fuel_road += float(re.search(r'[0-9]+.[0-9]+', gearbox['fuel_road']).group(0))
            fuel_city += float(re.search(r'[0-9]+.[0-9]+', gearbox['fuel_city']).group(0))
            i_counter += 1
        except:
            fuel_ave = 'none'
            fuel_road = 'none'
            fuel_city = 'none'
        try:
            co2 += int(re.search(r'[0-9]+', gearbox['co2']).group(0))
        except:
            co2 = ''
        # before appending regex year of engine introduced to market for example: od 2009 do 2013 roku we take 2009
        # if date cannot convert to int it means something wrong
    try:
        temp_item_dict['car_engine_v'] = int(re.search(r'[0-9]{3,4}', item['car_primary']['car_engine_v']).group(0))
        temp_item_dict['car_engine_produced'] = int(re.search(r'[0-9]{4}', item['car_primary']['car_engine_produced']).group(0))
    except:
        continue
            # if date is not valid we set i_counter to 0, we do not need bada data
            # also we do not need very old cars like 1972, let`s analyze <1980, >
    if  temp_item_dict['car_engine_produced'] < 1980:
        continue
    try:
        temp_item_dict['fuel_road'] = round(fuel_road / i_counter, 1)
        temp_item_dict['fuel_ave'] = round(fuel_ave / i_counter, 1)
        temp_item_dict['fuel_city'] = round(fuel_city / i_counter, 1)
    except:
        temp_item_dict['fuel_road'] = 'none'
        temp_item_dict['fuel_ave'] = 'none'
        temp_item_dict['fuel_city'] = 'none'
        
    try:
        temp_item_dict['co2'] = round(co2 / i_counter, 0)
    except:
        temp_item_dict['co2'] = 'none'
        #  takes last euro type > the same engine construction
    temp_item_dict['euro_type'] = gearbox['euro_type']
    engine_list.append(temp_item_dict)

print(f'We have {len(engine_list)} different engines to study in list \'engine_list\'')
print('\nWhy so messy try-except code\n')
print('the problem is that on autocentrum.pl, before 2010 many cars have no CO2 information\n\
For example even car from 2011 has no information : Opel Insignia\n\
https://www.autocentrum.pl/dane-techniczne/opel/insignia/i/sedan/silnik-diesla-2.0-cdti-ecotec-startstop-160km-2011-2013/\n\
Analysis is as better as good are input values')
code_line_number(currentframe().f_lineno)
    # how many full data items in engine_list we have?
print('How incomplete data are on autocentrum.pl?')
incomplete_list = [item for item in engine_list if item['fuel_road'] == 'none']
print(f'\nFor example no data in fuel_road are in {len(incomplete_list)} engines/car models\n\
which is {round(100 * len(incomplete_list) / len(engine_list), 0)}% all data from our initial list')
incomplete_list = [item for item in engine_list if item['co2'] == 'none']
print(f'\nNo Co2 information in {round(100 * len(incomplete_list) / len(engine_list), 0)}% all data from our initial list')
incomplete_list = [item for item in engine_list if
                   item['co2'] == 'none' or
                   item['fuel_road'] == 'none' or
                   item['fuel_ave'] == 'none' or
                   item['fuel_city'] == 'none']

print(f'\nWhen we put it together and look for only full data items we get {round(100 * (1 -len(incomplete_list) / len(engine_list)), 0)}')
print('It seems that if Co2 data is included then all other fuel consumption informations also are in data')
code_line_number(currentframe().f_lineno)
print('How many cars in each year has got full data?')

my_years = list(range(1980, 2021))
    # we make list of list year and counter, counter initial = 0 
for index, el in enumerate(my_years):
    my_years[index] = [el, 0]
for year in my_years:
    for item in engine_list:
        if year[0] == item['car_engine_produced'] and item['co2'] != 'none':
            year[1] += 1
for year in my_years:
    print(year)
print('As we can see before 1996 there is lack of Co2 informations')
code_line_number(currentframe().f_lineno)

print('Even with incomplete Co2 data, we can do something.\nWe can find out what was average sized engine introduced to market in each year')
print('[Year, average cm3, engines count]')
    # Like before but we add to year and counter engine size
my_years = list(range(1980, 2021))
for index, el in enumerate(my_years):
    my_years[index] = [el, 0, 0]
for year in my_years:
    for item in engine_list:
        if year[0] == item['car_engine_produced']:
            year[1] += item['car_engine_v']
            year[2] += 1
    year[1] /= year[2]
    year[1] = int(year[1])
    
for year in my_years:
    print(year)  

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("darkgrid")
plt.plot([item[0] for item in my_years], [item[1] for item in my_years])
plt.show()
print('\nNew engine models in popular cars got back to 1980 year')

print('\nWhy in 2020 we have average near 1900 cm3 even though producers are pressed to reduce Co2?')
print('Because autocentrum database does not show most sold cars engine type, but models of engines.')
print('But still we are much below 2006 year.\n\n')

print('Percentage of engines type produced:')
from collections import Counter
my_list_2020 = [item['car_engine_type'] for item in engine_list if item['car_engine_produced'] == 2020]
my_list_2006 = [item['car_engine_type'] for item in engine_list if item['car_engine_produced'] == 2006]
my_dict_2020 = dict(Counter(my_list_2020))
my_dict_2006 = dict(Counter(my_list_2006))

    # 'diesel' vs hybrydowy' vs 'benzynowy'
for my_y, my_dict, my_list in [[2006, my_dict_2006, my_list_2006], [2020, my_dict_2020, my_list_2020]]:
    print('\nIn year:', my_y)
    for engine_type in ['diesel', 'benzynowy', 'hybrydowy', 'hybrydowy plug-in']:
        engine_val = my_dict.get(engine_type)
        if engine_val == None:
            engine_val = 0
        print(engine_type, int(100 * engine_val / len(my_list)), '%') 

print('\nIn 2020 we have almost {hybrid:.2f} % of hybrid engines'.format(
    hybrid = 100 * (my_dict_2020.get('hybrydowy') + my_dict_2020.get('hybrydowy plug-in')) / len(my_list_2020)))

my_list_2020_hybrid = [item for item in engine_list if item['car_engine_produced'] == 2020 if item['car_engine_type'] in ['hybrydowy', 'hybrydowy plug-in']]
my_list_2020_hybrid_engine = [item['car_engine_v'] for item in my_list_2020_hybrid]
import numpy as np
print('\nWhat size of hybrid engines we have?:')
print(int(np.mean(my_list_2020_hybrid_engine)), 'cm3')
print('So average hybrid`s engines are pretty close to our overall average, and do not diminish much average size of engine')
code_line_number(currentframe().f_lineno)


print('Funny thing is that we have huge raise in engines models, it is even 200% more than 20 year`s ago')
print('Let`s check how many unique engines we have, different: \
car_engine_produced, car_engine_v, car_engine_type, car_engine_power, car_engine_torque, car_engine_cylinders')
print('There is chance -> 0 that 2 different engines would have the same above values')
print('We can assume that it is result of merging and cooperating producers\n')
    # car_engine_produced, car_engine_v, car_engine_type, car_engine_power, car_engine_torque, car_engine_cylinders
my_years_0 = list(range(1980, 2021))
unique_list = []    
for year in my_years_0:
    for item in engine_list:
        if year == item['car_engine_produced']:
            unique_list.append([item['car_engine_produced'], item['car_engine_v'], 
                               item['car_engine_type'], item['car_engine_power'],
                               item['car_engine_torque'], item['car_engine_cylinders']])
    # we take every element and check if it exists in result list, if no we add item to result list
    # in python we can compare lists like [1,2,3] == [1,2,3]
result_list = []
print('May take up to 1 minute, please wait.\n')
 
for unique_list_item in unique_list:
    flag = True
    if len(result_list) == 0:
            result_list.append(unique_list_item)
    for result_list_item in result_list:
        if result_list_item == unique_list_item:
            flag = False
            break
    if flag == True:
        result_list.append(unique_list_item)

print(f'We had {len(unique_list)} engines in our list, but after comparing and filtering for unique\n\
we have really unique {len(result_list)} engines, which is {int(100 * len(result_list) / len(unique_list))}% of all.')

print('Now let`s check average engine size\n')
    # we could wrap some code bellow in one function and reuse it, but for excercise purposes let`s think
    # that every calculation is separate excercise
my_years_1 = list(range(1980, 2021))
for index, el in enumerate(my_years_1):
    my_years_1[index] = [el, 0, 0]
for year in my_years_1:
    for item in result_list:
        if year[0] == item[0]:
            year[1] += item[1]
            year[2] += 1
    year[1] /= year[2]
    year[1] = int(year[1])
    
print('[Year, average cm3, engines count]')    
for year in my_years_1:
    print(year)  

print('As we can see average of unique angines size is bigger than all engines constantly from ~2008')
plt.plot([item[0] for item in my_years], [item[1] for item in my_years], label = 'All engines')
plt.plot([item[0] for item in my_years_1], [item[1] for item in my_years_1], label = 'Unique engines')
plt.legend(loc = 2)
plt.show()
print('\nWhy? maybe because nowadays we have a lot of small engines in very different cars')
print('In the past producers made bigger engines for bigger cars and smaller engines to smaller cars,\n\
engines where designed for cars. Now producers design engine and put in every posiible car\n')
print('1. In the past we had bigger variety of engines')
print('2. Now we have more different car models with small engine than with big engines,\
in other words we put small engine to all cars and big engines only to big cars')
print('\n\nVariety of engines?\n')           
print('Year, all, unique, %')

variety_to_pot_x_y = []
for ind in range(len(my_years)):
    variety_to_pot_x_y.append([my_years[ind][0], int(100 * my_years_1[ind][2] / my_years[ind][2])])
    print(my_years[ind][0], my_years[ind][2], my_years_1[ind][2], int(100 * my_years_1[ind][2] / my_years[ind][2]), '%')  

plt.plot([item[0] for item in variety_to_pot_x_y], [item[1] for item in variety_to_pot_x_y])
plt.title('Engines variety %')
plt.show()
code_line_number(currentframe().f_lineno)
#-----------------------------------------------------------------------------------------------------

print('Let`s go back to cmplite data, co2 and fuel consumption')
complete_list = [item for item in engine_list if
                   item['co2'] != 'none' and
                   item['fuel_road'] != 'none' and
                   item['fuel_ave'] != 'none' and
                   item['fuel_city'] != 'none']
print('Now we know that many engines are duplicated in many models we coul use calculated result_list,\n\
but there is one problem. The same engine in different cars gives different Co2 production,\n\
so get unique engine list appending one more factor : Co2')

my_years_2 = list(range(1999, 2021))
unique_list = []    
for year in my_years_2:
    for item in complete_list:
        if year == item['car_engine_produced']:
            unique_list.append([item['car_engine_produced'], item['car_engine_v'], 
                               item['car_engine_type'], item['car_engine_power'],
                               item['car_engine_torque'], item['car_engine_cylinders'], item['co2']])
result_list = []
print('\nMay take up to 1 minute, please wait.\n')
 
for unique_list_item in unique_list:
    flag = True
    if len(result_list) == 0:
            result_list.append(unique_list_item)
    for result_list_item in result_list:
        if result_list_item == unique_list_item:
            flag = False
            break
    if flag == True:
        result_list.append(unique_list_item)

print(f'Unique engine list counts: {len(result_list)} engines, but some engines are the same just \
in different car model.')

    # we need production year, engine cm3 sum, co2 sum, counter
    # we can do the same as previous tasks, but list/array is good for not many variables in it, or when we mix types
    # so maybe try dictionary
    # !!! remember we calculate data only with CO2 nformation
    
with open('result_pickle.pickle', 'wb') as file:
    pickle.dump(result_list, file, protocol=pickle.HIGHEST_PROTOCOL)
    file.close()

    



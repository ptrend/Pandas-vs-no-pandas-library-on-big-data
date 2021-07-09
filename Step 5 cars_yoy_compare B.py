
'''
We continue check how CO2, power, fuel consumption, ... changed in last ~30 years.
We can compare one chosen producer or group of producers.
Comparing we have to slice data, separate premium / sport cars from cars for "people" :)
lets take: 
'''

'''
easier would be using pandas but, let`s try use list of dictionaries placed in 'result_pickle.pickle' exported in "Step 4 cars_yoy_compare A.py"
we will try write our own functions, group and aggregate them, simple python code no pandas library
'''


    # Spyder Ide used, clearing console
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
except:
    pass  

import sys
import pickle
with open('result_pickle.pickle', 'rb') as file:
    result_list = pickle.load(file)
    file.close()
   
def co2():
    global co2_engine_b_y
    global co2_engine_d_y
    global v_engine_b_list
    global v_engine_d_list
    v_engine_b_list = []
    v_engine_d_list = []
    co2_engine_b_y, co2_engine_d_y = [], []
    x_data, y_ben, y_diesel = [], [], []
    my_co2_dict = {} # or my_co2_dict = dict()
    my_years_2 = list(range(1999, 2021))
    for year in my_years_2:
        # year, co2, counter
        temp_list_b_1, temp_list_b_2, temp_list_b_3 = [year,0,0], [year,0,0], [year,0,0]
        temp_list_d_1, temp_list_d_2, temp_list_d_3 = [year,0,0], [year,0,0], [year,0,0]
        my_co2_dict[year] = {}
        for item in result_list:
            if year == item[0]:
                if item[2] == 'benzynowy':
                    if 951 <= item[1] < 1450:
                        temp_list_b_1[1] += item[6]
                        temp_list_b_1[2] += 1
                    elif 1451 <= item[1] < 1950:
                        temp_list_b_2[1] += item[6]
                        temp_list_b_2[2] += 1
                    elif 1951 <= item[1] < 1999:
                        temp_list_b_3[1] += item[6]
                        temp_list_b_3[2] += 1
                    else:
                        pass
                elif item[2] == 'diesel':
                    if 951 <= item[1] < 1450:
                        temp_list_d_1[1] += item[6]
                        temp_list_d_1[2] += 1
                    elif 1451 <= item[1] < 1950:
                        temp_list_d_2[1] += item[6]
                        temp_list_d_2[2] += 1
                    elif 1951 <= item[1] < 1999:
                        temp_list_d_3[1] += item[6]
                        temp_list_d_3[2] += 1
                    else:
                        pass
                else:
                    pass
                # print(temp_list_b_3)
                if not my_co2_dict[year].get(item[2]):
                    my_co2_dict[year][item[2]] = {}
                    my_co2_dict[year][item[2]]['engine_v_sum'] = 0
                    my_co2_dict[year][item[2]]['engine_co2_sum'] = 0
                    my_co2_dict[year][item[2]]['engine_count'] = 0
                my_co2_dict[year][item[2]]['engine_v_sum'] += item[1]
                my_co2_dict[year][item[2]]['engine_co2_sum'] += item[-1]
                my_co2_dict[year][item[2]]['engine_count'] += 1
        v_engine_b_list.append([temp_list_b_1, temp_list_b_2, temp_list_b_3])
        v_engine_d_list.append([temp_list_d_1, temp_list_d_2, temp_list_d_3])
    for key1, item1 in my_co2_dict.items():
        x_data.append(key1) #year
        
        for key2, item2 in my_co2_dict[key1].items():
            co2_1000 = 1000 * my_co2_dict[key1][key2]['engine_co2_sum']
            co2_1000 /= my_co2_dict[key1][key2]['engine_v_sum']
            co2_1000 = int(co2_1000)
            co2_engine = my_co2_dict[key1][key2]['engine_co2_sum']
            co2_engine /= my_co2_dict[key1][key2]['engine_count']
            co2_engine = int(co2_engine)
            if key2 == 'benzynowy':
                y_ben.append(co2_1000)
                co2_engine_b_y.append(co2_engine)
            elif key2 == 'diesel':
                y_diesel.append(co2_1000)
                co2_engine_d_y.append(co2_engine)
            else:
                pass
    return x_data, y_ben, y_diesel 
    # return multiple 
    # global example for co2_engine_b_y, co2_engine_d_y
    # or we could define co2_engine_b_y = [], co2_engine_d_y = [] 
    # before function and it would be default global, but only if we ran function    
    

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
x_d, y_b, y_d = co2()

fig, ax = plt.subplots(figsize = (10, 5))
ax.plot(x_d, y_b, label = 'PB')
ax.plot(x_d, y_d, label = 'ON')
min_tick = int(min(min(y_b), min(y_d)) / 10) * 10
max_tick = int(max(max(y_b), max(y_d)) / 10) * 12
ax.set_yticks([x for x in range(min_tick, max_tick, 10)])
ax.xaxis.set_ticks(range(1999, 2022, 2))
ax.legend(loc = 1)
plt.title('g co2 on 100 km from 1 dm3 engine')
plt.show()
print('\nThere is some decrease in emissions co2 per 1 dm3 engine on distance 100km\
but is nt huge as we suspected\n')
print('Why? Let`s see on emisions co2 per engine full size in years\n')

fig, ax = plt.subplots(figsize = (10, 5))
ax.plot(x_d, co2_engine_b_y, label = 'PB')
ax.plot(x_d, co2_engine_d_y, label = 'ON')
ax.xaxis.set_ticks(range(1999, 2022, 2))
ax.legend(loc = 1)
plt.title('Introduced engine to market co2 g/100km ')
plt.show()

print('\n!!!!!!!!!!!!!!!!!!!!!\n')
print('You may think why data are different to data in internet?\n')
print('In internet there is data from registered cars.\n\
We have engines in cars introduced to market in each year also smaller engines are\
sold more often than bigger ones')
print('\n\nLet`s see how engine co2 depends on its volume?\n')
print('Compare dm3 <1 - 1.5) , <1.5 - 2) and most popular in big engines 2.0 dm3')
    # v_engine_b_list, v_engine_d_list. These are lists of lists for every year 
    # plot benzin
    # zero engine in year problem in diesel engines
    # we can put for example 1, but then we would have one year jump or make linear interpolation
    # in 2018 and 2019 we did not have small diesel engines introduced to market
    # [[2018, 0, 0], [2018, 8114.0, 72], [2018, 6638.0, 50]]
    # [[2019, 0, 0], [2019, 4368.0, 33], [2019, 8269.0, 56]]
    # we can manually change or write something for fun

help_label_dict = {
    0 : '<1 - 1.5)',
    1 : '<1.5 - 2)',
    2 : '2'
    }
help_title_list = ['Co2 PB g/100 km per engine size', 'Co2 ON g/100 km per engine size']    
help_ticks = [[x for x in range(100, 220, 10)], [x for x in range(90, 180, 10)]]
for ind, item in enumerate(v_engine_d_list):
    for ind_2, item_2 in enumerate(item):
        if item_2[2] == 0:
            item_2[2] = (v_engine_d_list[ind - 1][ind_2][2] + v_engine_d_list[ind + 1][ind_2][2]) / 2
            item_2[1] = (v_engine_d_list[ind - 1][ind_2][1] + v_engine_d_list[ind + 1][ind_2][1]) / 2

for ind_help, s_engine in enumerate([v_engine_b_list, v_engine_d_list]):
    fig, ax = plt.subplots(figsize = (10, 5))
    for ind in [0,1,2]:
        ax.plot([item[0][0] for item in v_engine_b_list],
            [int(item[ind][1] / item[ind][2]) for item in s_engine], 
            label = help_label_dict[ind])
    ax.set_yticks(help_ticks[ind_help])
    ax.xaxis.set_ticks(range(1999, 2022, 2))
    plt.title(help_title_list[ind_help])    
    plt.legend(loc = 1) 
    plt.show()
    
print('\n\nWhat happened in 2020 with new diesel engines?\n\
Go to csv file or use pandas and find out. Calculations are properly done.\n\
If You compare this results with something You found out on the web, remember do not comprare apples to oranges\
Details in dataset are pretty important :)')

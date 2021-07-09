
from inspect import currentframe

def code_line_number(line_no):
    print('\nLast executed Code line:', line_no - 1,'\n')
    print('_' * 40 ,'\n')

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

    # Spyder Ide used, clearing console
try:
    from IPython import get_ipython
    get_ipython().magic('clear')
except:
    pass  

if not os.path.isfile('car_list_csv_updated.csv'):
    print('UPDATE electric car list first by running csv_update_online.py')
    sys.exit() # sys.exit() instead of else statement

my_cols_1 = ['car_id', 'car_engine_type', 'range_city', 'battery_kwh', 'start_prod', 'end_prod', 'link']
df = pd.read_csv('car_list_csv_updated.csv', sep =';', usecols = my_cols_1)

# print(df[['car_id']][df['car_id'].str.contains(r'BMW')])
# print(df.info(memory_usage="deep"))
    # for this plot we need only 'car_id','car_engine_type' , 'range_city', 'range_road', 'battery_kwh'
    # reasigning df to only electric gives us much less memory used
df = df[df['car_engine_type'] == 'elektryczny']
    # also delete data where battery is 0
    # describe shows that minimum is 0, we do know there are no null data
# print(df.describe())
df = df[df['battery_kwh'] > 0]    
# print(df.describe())
    # 119 rows instead 143
plot_steps = {}
plot_steps['step_1'] = [df[['range_city', 'battery_kwh']], 'r', 'Deleted data']
    # we can see that one data is odd battery kwh ~ 20 and range ~ 600
    # + one has range and battery near 0
    # + one has battery near 0 and range ~ 100
    # let`s find that rows
# print(df[(df['range_city'] > 400) & (df['battery_kwh'] < 40)])
    # we have two rows, for Fiat it seams it is correct but for Chevrolet Volt it is an obvious error
    # cut Chevrolet Volt from our df
list_of_odd = (df[(df['range_city'] > 400) & (df['battery_kwh'] < 40)]['car_id']).values.tolist()
df = df[df['car_id'] != list_of_odd[0]]
# print(df[(df['range_city'] < 120) & (df['battery_kwh'] < 20)])
    # It is Renault Twizy Electric so it is ok
    # Second is BMW i8 Coupe Facelifting Elektryczny, it not pure electric
df_list_of_odd = df[(df['range_city'] < 120) & (df['battery_kwh'] < 20)]
BMW_i8_car_id = df_list_of_odd.values.tolist()[0][0]
    # use regex to find out how many BMW we have
# print(df[df['car_id'].str.contains(r'BMW')])
    # *****************************************************
    # we can drop BMW_i8 on few ways
    # -----------------------------------------------------
    # 1. just return new df without this car
# df = df[df['car_id'] != BMW_i8_car_id]
    # -----------------------------------------------------
    # 2. use drop() / especially good for small numbers of rows
    # we need have index to use drop
# df.set_index('car_id', inplace = True)
# df = df.drop(labels = BMW_i8_car_id, axis = 0, inplace = True)
# df.reset_index(inplace = True)
    # -----------------------------------------------------
    # 3. Delete rows based on row number
    # reindex our sliced df from 0 to n -1 rows
df.reset_index(drop = True, inplace = True)
BMW_index = df.index[df['car_id'] == BMW_i8_car_id][0]
df = df.drop(df.index[BMW_index], axis = 0)
    # *****************************************************
    # finally reset index one more time to have numbers 0 to n - 1 rows
df.reset_index(drop = True, inplace = True)
plot_steps['step_2'] = [df[['range_city', 'battery_kwh']], 'b', 'Step_2']
    # plot in one to find differences, if points overlap, color -> last card rule
    # if df has many rows, deleted rows added to df_deleted and draw df and df_deleted
for frame in [plot_steps['step_1'], plot_steps['step_2']]:
    my_step_1_vs_2 = plt.scatter(frame[0]['range_city'], frame[0]['battery_kwh'], color = frame[1], label = frame[2])
plt.title("Chart 1. Step_1 vs Step_2 / red -> deleted data")
plt.legend(loc = 2)
plt.show()
code_line_number(currentframe().f_lineno)

# Last executed Code line
    # comparing cars must include year of release model
    # for this we do not need link and car_engine_type columns
df.drop(['car_engine_type', 'link'], axis = 1, inplace = True)
    # how about set multiindex?
df.set_index(['start_prod', 'car_id'], inplace = True)
df.sort_index( inplace = True)
    # dump data to csv to quick see in excel
df.to_csv('sth_1.csv', sep = ';', encoding="utf-8-sig", index = True)

# *******************************************************************
    # how many models had each producer?
df.reset_index(inplace = True)

def group_split_func(car, n):
    return ' '.join(car.split(' ')[0:n])

cars_brand_year = df.groupby(['start_prod', df['car_id'].apply(lambda x: group_split_func(x, 1))])['car_id'].count()
# print(cars_brand_year)    
    # it seems to many models?
cars_brand_year = df.groupby(['start_prod', df['car_id'].apply(lambda x: group_split_func(x, 2))])['car_id'].count()    
# print(cars_brand_year)
    # we can see ex: in 2020 Peugeot had 19 models, 
    # but there are only two models and theirs multiple versions : Peugeot Expert 9, Peugeot Traveller 10
    # so every year there was only one new model introduced by manufacturer
cars_brand_year = cars_brand_year.groupby(['start_prod','car_id']).count()
# print(cars_brand_year)
# print(cars_brand_year)
# *******************************************************************
    # let`s go back to our df 
# we have chart battery vs range for all years of models introduced to market
# let`s divide to each years of production 
# <2011, 2013), <2013, 2015), <2015, 2017), <2017, 2019),<2019, 2021)
for frame in [df[(df['start_prod'] >= year ) & (df['start_prod'] < (year + 2))] for year in range(2011,2021,2)]:
    plt.scatter(frame['range_city'], frame['battery_kwh'], label = f'{frame.start_prod.min()} - {frame.start_prod.min() + 1}')
plt.legend(loc = 2)
plt.title('Chart 2. battery_kwh vs range_city')
plt.show()
code_line_number(currentframe().f_lineno)
     # as we see most of new models were introduced in 2019 - 2020
# *******************************************************************
     # another approach, this time with bar and sum models by data range 
     # using Categorical data
df_new = pd.DataFrame({"value": df['start_prod'].values})
df_new["group"] = pd.cut(df_new.value, range(2011, 2022, 2), right=False)
grouped_data = df_new.groupby(by = 'group')['value'].count()

ax = grouped_data.plot.bar(rot = 45, xlabel = '')
ax.set_xlabel('')
ax.set_title('Chart 3a. All car models - Categorical data method')
    # using Categorical data we have labels [2011, 2013), it does not look nice
ax.set_xticklabels([x.get_text().replace('[', '').replace('(', '')
                    .replace(',', ' -').replace(')', '')
                    for x in ax.get_xticklabels()])
ax.set_xticklabels([f'{x.get_text()[0:4]} - {str(int(x.get_text()[-4:]) - 1)}'
                    for x in ax.get_xticklabels()])
plt.show()
code_line_number(currentframe().f_lineno)

    # how about the same (3a) but with counter
    # for practice purposes, useless but can show that result`s of everything 
    # may be done as ~good as python`s built-in functions
from collections import Counter
from collections import OrderedDict

def plot_bar_counter(df1, chart_no, title_change):
    my_counter = Counter(df1['start_prod'].values)
    my_counter = OrderedDict(sorted(my_counter.items()))
    my_years_range = [*range(2011, 2022, 2)]
    
    my_years_range_pair = []
        # sys.exit() stops entire module, but if we need all code to executed it 
        # gives 1 less else conditional due to importance of Python`s indentation  
    if len(my_years_range) % 2 != 0:
        print('odd len(my_years_range), check it and modify my_years_range, ex: one range 1 year+')
        sys.exit()
        
    left_side = my_years_range.pop(0)
    while len(my_years_range) > 0:
        right_side = my_years_range.pop(0) - 1
        my_years_range_pair.append([left_side, right_side, 0])
        left_side = right_side + 1 
    
        # iterating through counter keys
    for _ in my_counter.keys():
        for year_range in my_years_range_pair:
            if ((_ == year_range[0]) or (_ == year_range[1])):
                year_range[2] += my_counter[_]
                
    my_bar = plt.bar([f'{str(x[0])} - {str(x[1])}' for x in my_years_range_pair],
            [x[2] for x in my_years_range_pair], width = 0.5)
    plt.title(f'Chart {chart_no}. {title_change}')
    plt.xticks(rotation = 45) 
        # this time add values on top and greed, and also change bar color of max bar
    for rect in my_bar:
        rect_height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2, 0.5 * rect_height,
                    '%d' % int(rect_height), ha='center', va='bottom',
                    color = 'black', fontsize = 'x-large')
        if rect_height == max([rect.get_height() for rect in my_bar]):
            rect.set_color('r')
    plt.grid(axis = 'y', color = 'red', linestyle = '--', linewidth = 0.5)
    plt.show()
    
plot_bar_counter(df, '3b', 'All car models - Counter method')
code_line_number(currentframe().f_lineno)
# *******************************************************************
    # we know that many points battery vs range are overlaping
    # let`s find out how many unique for each producers there are 
    # different models with battery and range 
    # car_id column values modyfied, 2 first words to identify car: brand + model

df['car_id'] = df['car_id'].apply(lambda x: group_split_func(x, 2))
    # get rid off some overlaping rows values, all columns except end of production, 
    # models are introduced in the same year, some models production may be ended sooner
    # beacuse of lack of interest

df.drop_duplicates(subset = ['start_prod', 'car_id', 'range_city', 'battery_kwh'], inplace = True)
plot_bar_counter(df, '3c', 'Car models limited to unique - Counter method')
code_line_number(currentframe().f_lineno)
# *******************************************************************
    # how about add some extra data to our plot? 
    # for example km per battery kwh from "unique" data rounded to integers
df['km_per_kwh'] = (df['range_city'] / df['battery_kwh']).apply(lambda x: round(x, 1))

def mean_rounded(x):
    return round(x.mean(), 1)

df_grouped_km_kwh = df[['start_prod', 'km_per_kwh']].groupby(by = 'start_prod').agg(
    Cars_count = ('km_per_kwh', 'count'), Minimum = ('km_per_kwh', 'min'),
    Average = ('km_per_kwh', mean_rounded), Maximum = ('km_per_kwh', 'max'))

print('\n\nRange km per 1 kwh of battery')
print(df_grouped_km_kwh)  
code_line_number(currentframe().f_lineno)

    # in this case pivot_table gives more elasticity in caclulations on multiple columns
    # without merging two grouped df we can make calculations on columns: 'km_per_kwh' and 'battery_kwh'
df_pivot_table = pd.pivot_table(df, values = ['km_per_kwh', 'battery_kwh'], index = ['start_prod'],
                   aggfunc={
                       'km_per_kwh': [np.count_nonzero, min, np.mean, max,],
                       'battery_kwh': [min, np.mean, max,]}).reset_index()
    #getting access to pivot_table may be a little tricky, beacuse of MuliIndex 
print('\nMultiIndex of pivot_table\n\n', df_pivot_table.columns, '\n\n')
code_line_number(currentframe().f_lineno)
    # EX: get all rows sraet_prod > 2015
print('start_prod > 2015\n', df_pivot_table[df_pivot_table[('start_prod', '')] > 2015])
code_line_number(currentframe().f_lineno)

    # how about rename MultiIndex? Having MultiIndex may be a little bit anoying
    # we can join levels of MultiIndex
import copy
df_pivot_table_copied = copy.deepcopy(df_pivot_table)

print('Multiindex levels joined with defined map function\n')
    # with defined map function join_multi_index(n)
def join_multi_index(n):
    if n[1] == '':
        return n[0]
    return n[0] + '_' + n[1]
df_pivot_table.columns = list(map(join_multi_index, df_pivot_table.columns))
print(df_pivot_table.columns)
code_line_number(currentframe().f_lineno)
    # or with simple string function join but with no handling exceptions like
    # empty index name ex. ('start_prod', '')
# df_pivot_table.columns = list(map("_".join, df_pivot_table.columns))
#     # we see that one column is 'start_prod_' beacuse of MultiIndex ('start_prod', '')
#     # we can manually rename
# df_pivot_table.rename({'start_prod_' : 'start_prod'}, axis = 1, inplace = True)    

    # how about more visualisation of simple plots?
    # range plot min/max or range km
print('Looks ugly, doesn\'t it???')
grouped_df = df.groupby(by = 'start_prod').agg(km_min = ('range_city', 'min'), km_max = ('range_city', 'max'))
year_x = grouped_df.index.values.tolist()
def between_plot(grouped_df = grouped_df, year_x = year_x):
    fig, ax = plt.subplots()
    km_min_y = grouped_df['km_min'].values.tolist()
    km_max_y = grouped_df['km_max'].values.tolist()
    ax.fill_between(year_x, km_min_y, km_max_y)
    return ax
between_plot()
plt.show()
code_line_number(currentframe().f_lineno)
    # We do not have all x_labels and with so few data chart will manage that
my_ax = between_plot()
my_ax.xaxis.set_ticks(year_x)
plt.show()
print('\nWe have all x labels on chart but we see that empty space for 2012 -> no\
data to make even spaced x labels we have to do some trick')
code_line_number(currentframe().f_lineno)
print('\nWe plot as a function of x values for "natural nombers" variables \
and then replace by names from oryginal ticks and then replace by names from oryginal ticks\
ticks array`s size one and other must be the same')
year_x_natural = list(range(1, len(year_x) + 1))
my_ax = between_plot(year_x = year_x_natural)
plt.show()
code_line_number(currentframe().f_lineno)
print('\nNow we replace with our true xlabels\nAnd finally:')
year_x_natural = list(range(1, len(year_x) + 1))
my_ax = between_plot(year_x = year_x_natural)
year_x.insert(0, year_x[0] - 1)
year_x.append(year_x[-1] + 1)
    # We do not need warning comment about FixedFormatter should only be used together with FixedLocator
import matplotlib.ticker as mticker
ticks_loc = my_ax.get_xticks().tolist()
my_ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
my_ax.xaxis.set_ticklabels(year_x)
plt.show()
code_line_number(currentframe().f_lineno)

# *******************************************************************
print('Crazy idea between_plot may not look nice for a few data\nWe will try plot between line to \"between bar\"')

grouped_df = df.groupby(by = 'start_prod').agg(km_min = ('range_city', 'min'), km_max = ('range_city', 'max'))
grouped_df.reset_index(inplace = True)
full_data = grouped_df.values.tolist()
    # Nested List Comprehensions
full_data = [[int(item) for item in item2] for item2 in full_data]
bar_year, bar_min, bar_max = [item[0] for item in full_data], [item[1] for item in full_data], [item[2] for item in full_data]

fig, ax = plt.subplots(figsize = (10, 5))
ax.plot(0,0)
    # add xscale 1, 2, 3, 4...., and yscale max
max_scale_y = int((round(grouped_df['km_max'].max() / 100, 0) + 1) * 100)
ax.set_ylim(0, max_scale_y)
ax.set_xlim(0, len(bar_year) + 1)
    # add rectangles
start_x = 0.75

for _ in range(0, len(bar_min)):
    rec_1 = plt.Rectangle((start_x + _, bar_min[_]), 0.5, bar_max[_] - bar_min[_])
    ax.add_patch(rec_1)
    ax.text(start_x + _, bar_min[_] - 25, bar_min[_]) 
    ax.text(start_x + _, bar_max[_] + 10, bar_max[_])
    
bar_year.insert(0, bar_year[0] - 1)
bar_year.append(bar_year[-1] + 1)  
bar_year = [str(_) for _ in bar_year]
ticks_loc = my_ax.get_xticks().tolist()
ax.xaxis.set_major_locator(mticker.FixedLocator(ticks_loc))
ax.xaxis.set_ticklabels(bar_year)
ax.title.set_text('Range min / max in introduced cars to the market')
plt.show()
code_line_number(currentframe().f_lineno)
# *******************************************************************
# 
print('Why range does not increase YOY ?\n')
print('1. Electric engines have reached theirs is today\'s efficiency long time ago')
print('2. YOY electric cars were design to be more and more complicated in in their construction')
print('3. 2. -> causes increase in weight\n')
print('\n\nCalculations 2010 = 100\n\n')
df = pd.read_csv('car_list_csv_updated.csv', sep =';')
df = df[df['car_engine_type'] == 'elektryczny']
df_grouped = df.groupby('start_prod').agg(avg_weight_min = ('weight_min', 'mean'), avg_weight_max = ('weight_max', 'mean'))
    # we calculate year/2010 to see how weight changed in 10 years, calculating YOY may not say much
# df_grouped['avg_min_YOY'] = df_grouped['avg_weight_min'].rolling(window = 2).apply(lambda df_tem: df_tem.iloc[1] / df_tem.iloc[0] - 1)
# df_grouped['avg_max_YO2Y'] = df_grouped['avg_weight_max'].rolling(window = 2).apply(lambda df_tem: df_tem.iloc[1] / df_tem.iloc[0] - 1)
    
    # if we had multiindex we would use groupby.first to create new column with first current group value
    # with one indexed we can just take first value of avg_weight_min and avg_weight_max
    #  to have actual changejust minus 1
df_grouped['avg_min_YO2010'] = df_grouped['avg_weight_min'] / df_grouped['avg_weight_min'].iloc[0] # - 1
df_grouped['avg_max_YO2010'] = df_grouped['avg_weight_max'] / df_grouped['avg_weight_max'].iloc[0] # - 1
    
for col in df_grouped.columns[0:2]:
    df_grouped[col] = df_grouped[col].apply(lambda x: round(x, 0))
for col in df_grouped.columns[-2:]:
    df_grouped[col] = df_grouped[col].apply(lambda x: round(x, 2))

code_line_number(currentframe().f_lineno)

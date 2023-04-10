#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 09:29:08 2023

@author: teodornicola-antoniu
"""
import os

import pandas as pd
import itertools
import wordcloud as wc
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

###############################################################################
# Data Pre-Processing
###############################################################################

'''
Step 1:
    
To begin with, we will read the provided csv files into dataframes in pandas.

'''

current_file_path = os.path.dirname(os.path.abspath('__file__'))

main_table = pd.read_csv(current_file_path + '/Central_American_Survey_Original/main_table.csv')
hh_roster = pd.read_csv(current_file_path + '/Central_American_Survey_Original/hh_roster.csv')
mig_ext_roster = pd.read_csv(current_file_path + '/Central_American_Survey_Original/mig_ext_roster.csv')
mig_int_roster = pd.read_csv(current_file_path + '/Central_American_Survey_Original/mig_int_roster.csv')
mig_pend_roster = pd.read_csv(current_file_path + '/Central_American_Survey_Original/mig_pend_roster.csv')
answer_lookup = pd.read_excel(current_file_path + '/Central_American_Survey_Original/look-up table.xlsx', sheet_name= 'answer_lookup')

'''
Step 2:
    
Then, we are going to see how many rown and columns we have in each of the files.
I am planning to plot this to show visually the quantity of information in each file

'''
print(len(main_table))                  #4998
print(len(main_table.columns))          #456

print(len(hh_roster))                   #22369
print(len(hh_roster.columns))           #61


print(len(mig_ext_roster))              #1624
print(len(mig_ext_roster.columns))      #116


print(len(mig_int_roster))              #721
print(len(mig_int_roster.columns))      #90


print(len(mig_pend_roster))             #384
print(len(mig_pend_roster.columns))     #52


#Table size (row * column)
print(main_table.size)
print(hh_roster.size)
print(mig_ext_roster.size)
print(mig_int_roster.size)
print(mig_pend_roster.size)


'''
Step 3:
    
We will now look at the number of unique respondents.

'''
print(main_table['_uuid'].nunique())
print(hh_roster['_submission__uuid'].nunique())
print(mig_ext_roster['_submission__uuid'].nunique())
print(mig_int_roster['_submission__uuid'].nunique())
print(mig_pend_roster['_submission__uuid'].nunique())


print(main_table['_id'].nunique())
print(hh_roster['_submission__id'].nunique())
print(mig_ext_roster['_submission__id'].nunique())
print(mig_int_roster['_submission__id'].nunique())
print(mig_pend_roster['_submission__id'].nunique())

'''
Step 4:
    
We should also understand what percentage of the data is null

'''

print(main_table.isna().sum().sum()/main_table.size)
print(hh_roster.isna().sum().sum()/hh_roster.size)
print(mig_ext_roster.isna().sum().sum()/mig_ext_roster.size)
print(mig_int_roster.isna().sum().sum()/mig_int_roster.size)
print(mig_pend_roster.isna().sum().sum()/mig_pend_roster.size)


print(main_table.isna().sum().sum())
print(hh_roster.isna().sum().sum())
print(mig_ext_roster.isna().sum().sum())
print(mig_int_roster.isna().sum().sum())
print(mig_pend_roster.isna().sum().sum())

'''
Step 4:
    
Establish unique id key found across all datasets. Note, this is not a primary key.

'''

main_table       = main_table.rename(columns={'_id': 'UNIQUE_ID'})
hh_roster        = hh_roster.rename(columns={'_submission__id': 'UNIQUE_ID'})
mig_ext_roster   = mig_ext_roster.rename(columns={'_submission__id': 'UNIQUE_ID'})
mig_int_roster   = mig_int_roster.rename(columns={'_submission__id': 'UNIQUE_ID'})
mig_pend_roster  = mig_pend_roster.rename(columns={'_submission__id': 'UNIQUE_ID'})



'''
Step 5:
    

'''
answer_lookup = answer_lookup.dropna(how='all')
answer_lookup_dict = pd.Series(answer_lookup['text_content'].values,index=answer_lookup['name_mco']).to_dict()

###############################################################################
# Merge HH Education Level with Main Table on [Id, Age, Sex]
###############################################################################

main_table       = main_table.rename(columns={'_id': 'UNIQUE_ID',
                                              'rsp_sex' : 'SEX',
                                              'rsp_age' : 'AGE'})

hh_roster       = hh_roster.rename(columns={'_submission__id': 'UNIQUE_ID',
                                            'hh_sex' : 'SEX',
                                            'hh_age' : 'AGE'})





extended_main = main_table.merge(hh_roster[['UNIQUE_ID',
                                            'SEX',
                                            'AGE',
                                            'country',
                                            'escolaridad',
                                            'mig_ocupacion', 
                                            'orig_ocupacion']], 
                                 on=['UNIQUE_ID',
                                     'AGE',
                                     'SEX',
                                     'country'],
                                 how='left')


escolaridad_dict = {1:"Without education",
                    2:"Preschool",
                    3:"Primary",
                    4:"High school",
                    5:"General baccalaureate",
                    6:"Technical Baccalaureate",
                    7:"Higher or university education technician",
                    8:"University undergraduate (bachelor's degree, engineering)",
                    9:"University postgraduate (master's, doctorate or specialization)",
                    99:"NS / NR"}


occupation_dict = {1:"Salaried employment",
                   2:"Informal work",
                   3:"Own business",
                   4:"Agricultural production or labor",
                   5:"Unemployed",
                   6:"Retired",
                   7:"Domestic work",
                   8:"Unpaid home care",
                   9:"Student (may or may not attend classes regularly)",
                   10:"Other",
                   88:"Does not apply",
                   99:"NS / NR"}

remesa_occupation_dict = {1:'Permanent employment'                 ,
                          2:'Temporary or seasonal employment'     ,
                          3:'Own business'                         ,
                          4:'Informal work'                        ,
                          5:'Agricultural production'              ,
                          6:'Agricultural day'                     ,
                          7:'Unemployed'                           ,
                          8:'Retired'                              ,
                          9:'Domestic work'                        ,
                          10:'Student'                             ,
                          11:'Other'                               ,
                          99:'NS / NR'
                          }


income_sufficiency_dict = {1:'Enough'                   ,
                           2:'Almost enough'            ,   
                           3:'Sometimes enough'         ,
                           4:'Rarely enough'            ,
                           5:'Insufficient'             ,
                           99:'NS / NR'                 ,
                          }



extended_main = extended_main.replace({"escolaridad": escolaridad_dict})
extended_main = extended_main.replace({"mig_ocupacion": occupation_dict})
extended_main = extended_main.replace({"orig_ocupacion": occupation_dict})
extended_main = extended_main.replace({"remesa_remit_ocupacion": remesa_occupation_dict})
extended_main = extended_main.replace({"income_sufficiency_6m": income_sufficiency_dict})


lempira_to_USD_Fx = 0.0415
quetzals_to_USDFx = 0.1292 


def fxExchangetoUSD(row):
    if row['avg_income_currency'] == 0:
        return 0
    if row['avg_income_currency'] == 1:
        return row['avg_income_amount']
    if row['avg_income_currency'] == 2:
        return row['avg_income_amount']*lempira_to_USD_Fx
    if row['avg_income_currency'] == 3:
        return row['avg_income_amount']*quetzals_to_USDFx
    

extended_main['avg_income_amount_usd'] = extended_main.apply(fxExchangetoUSD,axis=1)


# extended_main.to_excel(current_file_path + '/extended_main.xlsx')


###############################################################################
# 
###############################################################################

find_Oscar_cols = ['UNIQUE_ID'                  ,
                   'SEX'                        ,
                   'AGE'                        ,
                   'country'                    ,
                   'escolaridad'                ,
                   'mig_ocupacion'              , 
                   'orig_ocupacion'             ,
                   'remesa_remit_ocupacion'     ,
                   'avg_income_amount_usd'      ,
                   'income_sufficiency_6m'      ,
                   ]

find_Oscar_df = extended_main[find_Oscar_cols]






###############################################################################
#Pre-processing of mig_ext_roster
###############################################################################

mig_ext_country_dict = {1:'United States of America',
                        2:'Canada',
                        3:'Australia',
                        4:'Spain',
                        5:'Italy',
                        6:'Mexico',
                        7:'Guatemala',
                        8:'Costa Rica',
                        9:'Honduras',
                        10:'The Savior',
                        11:'Nicaragua',
                        12:'Belize',
                        13:'France',
                        14:'Panama',
                        15:'Colombia',
                        16:'Ecuador',
                        17:'Peru',
                        18:'UK',
                        19:'chili',
                        20:'Brazil',
                        21:'Other',
                        99:'NS / NR',
                        }



extended_mig_ext_roster = mig_ext_roster.replace({"mig_ext_country": mig_ext_country_dict})
extended_mig_ext_roster.to_excel(current_file_path + '/extended_mig_ext_roster.xlsx')







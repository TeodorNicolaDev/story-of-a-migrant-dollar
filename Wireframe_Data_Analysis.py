#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 09:29:08 2023

@author: teodornicola-antoniu
"""

import pandas as pd
import itertools
import wordcloud as wc
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio


'''
Step 1:
    
To begin with, we will read the provided csv files into dataframes in pandas.

'''

main_table = pd.read_csv('/Users/teodornicola-antoniu/Desktop/Desktop - Teodor’s MacBook Pro (2)/Spring2023/Classes/6.C85 Data Visualizations/WFB Data/dataset-1_central-american-survey/main_table.csv')
hh_roster = pd.read_csv('/Users/teodornicola-antoniu/Desktop/Desktop - Teodor’s MacBook Pro (2)/Spring2023/Classes/6.C85 Data Visualizations/WFB Data/dataset-1_central-american-survey/hh_roster.csv')
mig_ext_roster = pd.read_csv('/Users/teodornicola-antoniu/Desktop/Desktop - Teodor’s MacBook Pro (2)/Spring2023/Classes/6.C85 Data Visualizations/WFB Data/dataset-1_central-american-survey/mig_ext_roster.csv')
mig_int_roster = pd.read_csv('/Users/teodornicola-antoniu/Desktop/Desktop - Teodor’s MacBook Pro (2)/Spring2023/Classes/6.C85 Data Visualizations/WFB Data/dataset-1_central-american-survey/mig_int_roster.csv')
mig_pend_roster = pd.read_csv('/Users/teodornicola-antoniu/Desktop/Desktop - Teodor’s MacBook Pro (2)/Spring2023/Classes/6.C85 Data Visualizations/WFB Data/dataset-1_central-american-survey/mig_pend_roster.csv')
answer_lookup = pd.read_excel('/Users/teodornicola-antoniu/Desktop/Desktop - Teodor’s MacBook Pro (2)/Spring2023/Classes/6.C85 Data Visualizations/WFB Data/Central American Survey Processed/look-up table.xlsx', sheet_name= 'answer_lookup')


"""Generates CSV file with array info.
Adding: 'left', 'right'
"""


import os
import pandas as pd
import numpy as np
import proplot as pplt
import sys

polygons = {'left_1': ['2019P184', '2019P127', '2019P182', '2019P128'],
            'left_2': ['2019P184', '2019P124', '2019O6', '2019P127'],
            'left_3': ['2019O1', '2019P127','2019O6'],
            'left': ['2019P184', '2019P127', '2019P182', '2019P128'],
            'DN_1': ['2019P124', '2019P125', '2019P102', '2019P198'],
            'DN_2': ['2019P90', '2019P91', '2019P193', '2019P196'],
            'DN_3': ['2019P188', '2019P187', '2019P92', '2019P103'],
            'DN_4': ['2019P191', '2019P148', '2019P200', '2019P195'],
            'DN_5': ['2019O6', '2019P203', '2019T69', '2019P105'],
            'l_sites': [ '2019T65', '2019T67', '2019S94'],
            'DN_full': ['2019O5', '2019P91', '2019P187', '2019O1',
                        '2019O6', '2019P124'],
            'north': ['2019P22', '2019P91', '2019P187'],
            'right_1': ['2019P123', '2019P112', '2019P187'],
            'right_2': ['2019P114', '2019P113', '2019P155'],
            'right_3': ['2019P113', '2019P92', '2019P137', '2019P119'],
            'right': ['2019P114', '2019P123', '2019P113', '2019P155'],
            'distant': ['2019P123', '2019P157', '2019P156', '2019P155'],
            'large': ['2019P22', '2019P123', '2019P157', '2019P156',
                                 '2019P155', '2019P182', '2019P128', '2019P184',
                                 '2019P124']}
colors = {'left_1': 'lilac',
          'left_2': 'purple',
          'left_3': 'maroon',
          'left': 'lilac',
          'DN_1': 'k',
          'DN_2': 'k',
          'DN_3': 'k',
          'DN_4': 'k',
          'DN_5': 'k',
          'l_sites': 'tab:orange',
          'DN_full': 'k',
          'north': 'green',
          'right_1': 'tan',
          'right_2': 'gold',
          'right_3': 'yellow',
          'right': 'gold',
          'distant': 'orange',
          'large': 'forest green'}

lstyles = {'left_1': '-',
           'left_2': '--',
           'left_3': '-.',
           'left': '-',
           'right_1': '-',
           'right_2': '--',
           'right_3': '-.',
           'right': '-',
            'DN_1': '-',
           'DN_2': '--',
           'DN_3': '-.',
           'DN_4': ':',
           'DN_5': '(1, (4, 1, 1, 1, 1, 1))'} # Weird one - need to be able to parse this / remake it

lwidths = {'DN_1': 1,
           'DN_2': 1,
           'DN_3': 1,
           'DN_4': 1,
           'DN_5': 1,
           'left': 2, 
           'right': 2,
           'DN_full': 2}


# Make dataframe with buoy name, array name, color, line style, and line width
data = []
for array in polygons:
    color = colors[array]
    if array in lstyles:
        ls = lstyles[array]
    else:
        ls = '-'
        
    if array in lwidths:
        lw = lwidths[array]
    else:
        lw = 1
        
    for idx, buoy in enumerate(polygons[array]):
        
        data.append([buoy, array, color, ls, lw, idx])
array_ref = pd.DataFrame(data, columns=['buoyID', 'array_name', 'color', 'line_style', 'line_width', 'array_position'])
array_ref.to_csv('../data/array_info.csv')
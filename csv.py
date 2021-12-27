#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author      : Chen Wei
@date        : 2021-12-27
@file        : csv.py
@description : csv utils
@version     : 1.0
"""

import csv

def write_csv(file_path):
    """write csv file

    Args:
        file_path ([str]): file path
        
    NOTE: just code snippet for further modification
    
    https://geek-docs.com/python/python-tutorial/python-csv.html

    """
    csv_file = open(file_path, 'w', newline='')

    csv_writer = csv.DictWriter(csv_file, ['a', 'b', 'c', 'd'])

    csv_writer.writeheader()

    csv_writer.writerow({'a':1, 
                         'b':2, 
                         'c':3, 
                         'd':4})

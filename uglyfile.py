"""There are some ugly files such as MSCI raw data that looks like a '|' delimered csv
files but the head is listed as a column vector in the beginning of the file. I don't 
know the name of this format (please advice if you know it.)

This module reads the uglyfile and parse it into dataframe

Author: Giovanni (Xiaochuan) Ge
Created: 2017/04/21
Updated: 2017/04/21
"""
import re, csv, pandas as pd

def read(uglyfile):
    with open(uglyfile, 'r') as file_handle:
        ncol = find_ncol(file_handle)
        head = read_head(file_handle, ncol)
        assert ncol == len(head), 'Wrong number of columns'
        csv.register_dialect('piper', delimiter='|', quoting=csv.QUOTE_NONE)
        body = csv.reader(file_handle, dialect = 'piper')
        body = [row[1:] for row in body if len(row) > 1]
        body = [[s.strip() for s in nested] for nested in body]

    return pd.DataFrame(body, columns = head)

def find_ncol(file_handle, ncol = None):
    while ncol is None: 
        line = file_handle.readline()
        ncol = re.search('(?<=#\s)[0-9]+', line)
    return int(ncol.group(0))

def read_head(file_handle, ncol):
    head = []
    for i in range(ncol):    
        line = file_handle.readline()
        head.append(line.split()[-4])

    head = [s.strip() for s in head]
    return head
import pandas as pd
from scipy.optimize import root_scalar
import numpy as np
from datetime import datetime as dt

def simple_read(path):
    '''
    Reads .ict files to a Pandas DataFrame
    :param path: path to the .ict data
    :return: Pandas DataFrame with .ict data
    '''
    with open(path) as f:
        # find the value in the file which tells you how many lines to skip to get to the table
        first_line = f.readline()
        header_line = int(first_line[0:-2].split(",")[0])-1
    data = pd.read_csv(path, sep=',', skiprows=header_line)

    # finds the location in the path containing the date
    acc = 0
    boo = False
    for letter in path:
        if letter == '2':
            boo = True
        elif boo and letter == '0':
            acc -= 1
            break
        acc += 1
        
    # creates datetime object with the date the data was collected
    day = dt(int(path[acc:acc+4]), int(path[acc+4:acc+6]), int(path[acc+6:acc+8])) 
    
    for column in data.keys():
        if 'Time' in column:
            # converts seconds after midnight columns to datetime
            data[column] = day + pd.to_timedelta(data[column], unit='seconds')
    data.columns = data.columns.str.replace(' ', '')
    return data.replace(-9999, np.nan) # Converts -9999 values to NaN

def gf_kappa(k, D_d, gf, RH):
    A = 4*0.072*0.0180153/(8.3144598*(273.15+17)*1000)
    return (gf**3 - 1) / (gf**3 - (1 - k)) - RH / np.exp(A/(D_d*gf))

def get_root(D_d, gf, RH):
    return root_scalar(gf_kappa, args=(D_d, gf, RH), bracket=[0, 2], method='brentq').root

d = simple_read('./inputs/ARCSIX-DASH_P3B_20240610_R1.ict')

d['kappa'] = np.nan
for i in range(0,len(d)):
    row = d.loc[i]
    if np.isfinite(d.loc[i, 'GF']) & np.isfinite(d.loc[i, 'RH']):
        d.loc[i, 'kappa'] = get_root(row.Dp, row.GF, row.RH/100)

d.to_csv('./outputs/RF08_kappa.csv', index=False)
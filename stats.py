#%%
import pandas as pd

d = pd.read_csv('./outputs/RF08_kappa.csv', parse_dates=['Time_Start', 'Time_Stop'])

def window(d, start, end):
    s = pd.to_datetime(start)
    e = pd.to_datetime(end)

    return d[(d.Time_Start >= s) & (d.Time_Start < e)]

def get_stats(d):
    return d.describe()[['RH', 'Dp', 'RI', 'GF', 'kappa']]

stats = pd.DataFrame()

w1 = get_stats(window(d, '2024-06-10 11:50:00', '2024-06-10 12:14:00'))
w2 = get_stats(window(d, '2024-06-10 13:51:00', '2024-06-10 14:12:00'))
w3 = get_stats(window(d, '2024-06-10 14:54:00', '2024-06-10 15:23:00'))

ws = [w1,w2,w3]

for i in range(0,len(ws)):
    ws[i].to_excel(f'./outputs/w{i+1}.xlsx')
    ws[i].to_csv(f'./outputs/w{i+1}.csv')
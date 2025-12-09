from funcs import *
from scipy.optimize import root_scalar

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
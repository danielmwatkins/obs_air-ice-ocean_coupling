import pandas as pd
import numpy as np
import proplot as pplt
import os
import sys
sys.path.append('../obs_air-ice-ocean_coupling/scripts/')
import drifter
import xarray as xr

l_co_sites = {'L1': '2019T67', # L1 / T67 / asfs 40
           'L2': '2019T65', # L2 / T65 / asfs 30
           'L3': '2019S94', # L3 / S94 / asfs 50
           'Met City': '2019T66'}

dataloc = '../obs_air-ice-ocean_coupling/data/interpolated_tracks/'
files = os.listdir(dataloc)
files = [f for f in files if f != '.DS_Store']
buoy_data = {}
for f in files:
    buoy_data[f.split('.')[0].split('_')[-1]] = pd.read_csv(dataloc + f, parse_dates = True, index_col=0)

df_l2 = pd.read_csv('../data/met_data/asfs30.csv', index_col=0, parse_dates=True)
df_l1 = pd.read_csv('../data/met_data/asfs40.csv', index_col=0, parse_dates=True)
df_l3 = pd.read_csv('../data/met_data/asfs50.csv', index_col=0, parse_dates=True)
df_co = pd.read_csv('../data/met_data/metcity.csv', index_col=0, parse_dates=True)
df_co = df_co.loc[~df_co.index.duplicated()]



ts = slice('2020-01-30 00:00', '2020-02-02 00:00')
l_co_data = {'L1': df_l1.resample('30min').asfreq(),
             'L2': df_l2.resample('30min').asfreq(),
             'L3': df_l3.resample('30min').asfreq(),
             'Met City': df_co.resample('30min').asfreq()}

l_co_data['Met City'].rename(
            {'wspd_u_mean_10m': 'u_wind',
             'wspd_v_mean_10m': 'v_wind'}, axis=1, inplace=True)
for site in ['L1', 'L2', 'L3']:
    l_co_data[site].rename({'wspd_u_mean': 'u_wind',
                            'wspd_v_mean': 'v_wind'}, axis=1, inplace=True)


for buoy in buoy_data:
    buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude']]
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True, xvar='x_stere', yvar='y_stere')
    buoy_data[buoy]['u'] = buoy_df['u']
    buoy_data[buoy]['v'] = buoy_df['v']
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=False, method='centered', date_index=True)
    buoy_data[buoy]['u_stere'] = buoy_df['u']
    buoy_data[buoy]['v_stere'] = buoy_df['v']


for site in l_co_data:
    l_co_data[site] = l_co_data[site].where(np.abs(l_co_data[site].u_wind) < 50).loc[ts]
    buoy = l_co_sites[site]
    df = buoy_data[buoy].copy()
    
    df = df.merge(l_co_data[site].loc[:, ['u_wind', 'v_wind']], left_index=True, right_index=True)
    u = df['u_wind']
    v = df['v_wind']
    lon = df['longitude'] - 90
    df['u_stere_wind'] =  u * np.cos(np.deg2rad(lon)) -  v * np.sin(np.deg2rad(lon))
    df['v_stere_wind'] =  u * np.sin(np.deg2rad(lon)) +  v * np.cos(np.deg2rad(lon))
    df['wind_speed'] = np.sqrt(u**2 + v**2)
    l_co_data[site] = df.copy()
# Import data from ASFS and MetCity 
import xarray as xr
import pandas as pd
import numpy as np
import os

# Downloaded ADC data (cox et al. 2023)
dataloc = '/Users/dwatkin2/Documents/research/data/mosaic_met_data/'
saveloc = '../data/met_data/'
for source in ['metcity']: #['asfs40', 'asfs50', 'asfs30', 'metcity']:
    files = os.listdir(dataloc + source + '/data/')
    files = [f for f in files if f != '.DS_Store']

    files = [f for f in files if (int(f.split('.')[-3]) > 20200114) & (int(f.split('.')[-3]) < 20200301)]
    files.sort()
    
    dfs = []
    for file in files:
        with xr.open_dataset(dataloc + source + '/data/' + file) as ds:
#             if file == files[0]:
#                 print([v for v in ds.variables])
            if source == 'metcity':
                variables = ['lat_tower', 'lon_tower', 'tower_heading', 'atmos_pressure_2m',
                             'temp_2m', 'temp_6m', 'temp_10m',
                             'rh_2m', 'rh_6m', 'rh_10m',
                             'wspd_u_mean_2m', 'wspd_u_mean_6m', 'wspd_u_mean_10m',
                             'wspd_v_mean_2m', 'wspd_v_mean_6m', 'wspd_v_mean_10m']                
            else:
                variables = ['lat', 'lon', 'heading', 'atmos_pressure', 'temp', 'rh', 'wspd_u_mean', 'wspd_v_mean']
            if variables[0] + '_qc' in ds.variables:
                df = ds[variables + [v + '_qc' for v in variables]].to_dataframe()
                for v in variables:
                    df.loc[df[v + '_qc'] != 0, v] = np.nan
            else:                
                df = ds[variables].to_dataframe()
            if source == 'metcity':
                df.rename({'lat_tower': 'latitude', 'lon_tower': 'longitude'}, axis=1, inplace=True)
            else:
                df.rename({'lat': 'latitude', 'lon': 'longitude'}, axis=1, inplace=True)
            dfs.append(df.loc[:, [v for v in df.columns if v[-2:] != 'qc']])
    pd.concat(dfs).to_csv('../data/met_data/' + source + '.csv')
    readme = []
    for attr in ds.attrs:
        readme.append(attr + ': ' + ds.attrs[attr])
    with open(saveloc + source + '_readme.csv', 'w') as f:
        f.write('\n'.join(readme))
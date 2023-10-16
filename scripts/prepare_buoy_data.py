"""Data processing for the MOSAiC drifting buoys. Code was tested using drift tracks downloaded on March 23, 2023.

Before running the script, 
1. Download data from https://arcticdata.io/catalog/view/urn%3Auuid%3A56ffc86a-ddea-4379-a27a-09c992e65f16
2. Set 'dataloc' to point to the directory where you have saved the data
3. Set 'saveloc' to point to where you want the interpolated tracks to be saved
4. Make sure the file drifter.py is in the same directory as this script
"""
import numpy as np
import os
import pandas as pd
from drifter import standard_qc, interpolate_buoy_track, compute_velocity

#### Parameters #####
dataloc = '../data/adc_dn_tracks/'
saveloc = '../data/interpolated_tracks/'
begin = '2020-01-25 00:00'
end = '2020-02-05 00:00'
max_interval = '3H'
interp_freq = '30min'
min_coverage = 0.8 # Fraction of data required

# List of reference buoys for L and M sites
reference_buoys = {'2019O1': 'M1', 
                   '2019V2': 'M2', 
                   '2019O3': 'M3', 
                   '2019O4': 'M4',
                   '2019O5': 'M5',
                   '2019O6': 'M6', 
                   '2019T69': 'M8',
                   '2019T67': 'L1',
                   '2019T65': 'L2',
                   '2019S94': 'L3',
                   '2019T66': 'CO1'}

#### Setup ####
begin = pd.to_datetime(begin)
end = pd.to_datetime(end)
max_interval = pd.to_timedelta(max_interval)


CO_list = pd.read_csv(dataloc + 'CO_site_buoy_summary.csv').set_index('Sensor ID')
L_list = pd.read_csv(dataloc + 'L_site_buoy_summary.csv').set_index('Sensor ID')
M_list = pd.read_csv(dataloc + 'M_site_buoy_summary.csv').set_index('Sensor ID')
P_list = pd.read_csv(dataloc + 'P_site_buoy_summary.csv').set_index('Sensor ID')
metadata = pd.concat([CO_list, L_list, M_list, P_list], axis=0)

metadata['Deployment Date'] = pd.to_datetime(metadata['Deployment Date'].values)
metadata['Sampling Frequency (hh:mm)'] = [x + ':00' for x in metadata['Sampling Frequency (hh:mm)']]
metadata['Sampling Frequency (hh:mm)'] = pd.to_timedelta(metadata['Sampling Frequency (hh:mm)'])

p_buoys = list(P_list.index)
ref_buoys = [x for x in reference_buoys]

#### Read data #####
files = [f for f in os.listdir(dataloc) if f[0] not in ['.', 'D', 'm']]
files = [f for f in files if f.split('_')[1] != 'site']
files.sort()

buoy_data = {}
filenames = {}
n_pbuoys_with_data = 0
n_pbuoys_with_sufficient_data = 0
for f in files:
    dn_id, imei, sensor_id = f.split('.')[0].split('_')
    filenames[sensor_id] = f
    if sensor_id in p_buoys + ref_buoys:
        df = pd.read_csv(dataloc + f, parse_dates=True, index_col='datetime')

        if 'V' in sensor_id:
            df.index -= pd.to_timedelta('8H') # V buoys are in Beijing time, adjust to UTC


        t_idx = (df.index >= begin) & (df.index <= end)
        if len(df.loc[t_idx] >  0):
            if sensor_id in p_buoys:
                n_pbuoys_with_data += 1
            actual_freq = pd.to_timedelta(np.median(np.diff(df.loc[t_idx].index)))
            expected = int((end - begin) / actual_freq)            

            if len(df.loc[t_idx]) > min_coverage*expected:
                if sensor_id in p_buoys:
                    n_pbuoys_with_sufficient_data += 1
                buoy_data[sensor_id] = df.loc[t_idx]
print('P-buoys with at least one observation', n_pbuoys_with_data)
print('P-buoys exceeding minimum coverage', n_pbuoys_with_sufficient_data)
#### Clean and interpolate data ####
for sensor_id in buoy_data:
    df_qc = standard_qc(buoy_data[sensor_id],
                        min_size=50, # min size actually handled already by the min_coverage * expected part
                        gap_threshold='6H',        
                        segment_length=24,
                        lon_range=(-180, 180),
                        lat_range=(65, 90),
                        max_speed=1.5,
                        speed_window='3D',
                        verbose=False)   
    # Interpolate to hourly
    if df_qc is not None:
        df_interp = interpolate_buoy_track(df_qc.where(~df_qc.flag).dropna(), freq='30min', maxgap_minutes=240)
        df_interp = compute_velocity(df_interp, rotate_uv = False, date_index=True, method='c')
        df_interp.to_csv(saveloc + filenames[sensor_id])

"""Visualizing storm systems with regridded ERA5 data
Module to be added: rudimentary storm track identification.
Uses 10m wind for the wind arrays, and contours to show the 950 hPa wind speed.
Plots propagation of storm from MSL.
Updated version shows contours for wind speed.

First figure: 3x4 showing SLP

Requirements: 
- Interpolated buoy data
- drifter file 
- interpolated buoy data
- era5 data

TBD: Move the section that calculates distance to the CO to a separate section so that all plots refer to the same list of DN buoys
TBD: Add colors to the buoy locations
TBD: Adjust sizes
TBD: Add metadata file
"""

import xarray as xr
import os
import numpy as np
import proplot as pplt
import pandas as pd
import metpy.calc as mcalc
from metpy.units import units
import sys
import drifter
import warnings
import cartopy.crs as ccrs

warnings.simplefilter('ignore')
pplt.rc.reso='med'
pplt.rc['cartopy.circular'] = False
crs = ccrs.NorthPolarStereo(central_longitude=90, true_scale_latitude=70)

era5_dataloc = '../data/era5_regridded/'
buoy_dataloc = '../data/interpolated_tracks/'
sic_dataloc = '../data/'

##### Load buoy data #####
buoy_data = {}
metadataloc = '../data/adc_dn_tracks/'
metadata = pd.read_csv(metadataloc + 'DN_buoy_list_v2.csv')
metadata['filename'] = ['_'.join([x, str(y), z]) for 
                        x, y, z in zip(metadata['DN Station ID'],
                                       metadata['IMEI'],
                                       metadata['Sensor ID'])]
metadata.set_index('Sensor ID', inplace=True)

files = os.listdir(buoy_dataloc)
files = [f for f in files if f[0] not in ['.', 'm']]
buoy_data = {f.split('_')[-1].replace('.csv', ''): pd.read_csv(buoy_dataloc + f,
            index_col=0, parse_dates=True) for f in files}

full_time_series = [b for b in buoy_data if len(buoy_data[b].dropna())/len(buoy_data[b]) > 0.9]
station_id = metadata.loc[:, 'DN Station ID']
stations_already = []
truncated_list = []
for buoy in full_time_series:
    if station_id[buoy] not in stations_already:
        stations_already.append(station_id[buoy])
        truncated_list.append(buoy)

lat = pd.Series({buoy: buoy_data[buoy]['latitude'].median() for buoy in truncated_list})
lon = pd.Series({buoy: buoy_data[buoy]['longitude'].median() for buoy in truncated_list})
distant_buoys = lat[(lat < 87) | (lon < 80)].index.tolist()
near_buoys = [b for b in truncated_list if b not in distant_buoys]

# for buoy in buoy_data:
#     buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude']]
#     buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True)
#     buoy_data[buoy]['u'] = buoy_df['u']
#     buoy_data[buoy]['v'] = buoy_df['v']
    
#     buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude']].rolling('12H', center=True).mean()
#     buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True)
#     buoy_data[buoy]['smoothed_u'] = buoy_df['u']
#     buoy_data[buoy]['smoothed_v'] = buoy_df['v']
#     buoy_data[buoy]['smoothed_speed'] = buoy_df['speed']
    
# storm_track = pd.read_csv('../data/storm_track.csv', index_col=0, parse_dates=True).iloc[4:].dropna()    

##### Load ERA5 data #####
savename = '2020-01-25_2020-02-05'
era5_data = xr.open_dataset(era5_dataloc + 'era5_msl_regridded_' + savename + '.nc')

###### Defining the buoy groups ###########
# Intend to put this in a separate file so all figure plots can access it
# Change colors and size for this figure
left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P119']
distant = ['2019P156', '2019P157']
north = ['2019P22']
l_sites = ['2019T67', '2019T65', '2019S94']
l_colors = {'2019T67': 'tab:blue',
            '2019T65': 'powder blue',
            '2019S94': 'tab:green'}


#### Import sea ice concentration
ds_sic = xr.open_dataset(sic_dataloc + 'amsr_sea_ice_concentration.nc')

### Set up figure
pplt.rc['title.bbox'] = True
pplt.rc['title.bboxalpha'] = 1
pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0
pplt.rc.reso='med'
pplt.rc['cartopy.circular'] = False

crs = ccrs.NorthPolarStereo(central_longitude=90, true_scale_latitude=70)
crs_nsidc = ccrs.NorthPolarStereo(central_longitude=-45, true_scale_latitude=70)

df_x = pd.DataFrame({buoy: buoy_data[buoy]['x_stere'].resample('1H').asfreq() for buoy in buoy_data})
df_y = pd.DataFrame({buoy: buoy_data[buoy]['y_stere'].resample('1H').asfreq() for buoy in buoy_data})

warnings.simplefilter('ignore')
dates = pd.date_range('2020-01-30 00:00', '2020-02-02 00:00', freq='6H')
fig, axs = pplt.subplots(proj='npstere', proj_kw={'lon_0': 90}, ncols=4, nrows=3, width=8.5)
axs.format(land=True, boundinglat=75, latmax=90, lonlocator=np.arange(0, 361, 45), landzorder=1)
for ax, date in zip(axs, dates):
    ax.plot(df_x.loc[date,:], df_y.loc[date,:], transform=crs, marker='o', lw=0, ms=3, color='w', edgecolor='k', ew=0.5)
    ax.plot(df_x.loc[date, '2019T66'], df_y.loc[date,'2019T66'], transform=crs, marker='*', ms=12, color='firebrick', edgecolor='k', ew=0.5)
    c = ax.contourf(era5_data.x_stere,
                    era5_data.y_stere, era5_data.sel(time=date)['msl']/100, transform=crs,
                zorder=0, cmap='coldhot', levels=np.arange(972, 1030, 4), extend='both')
    ax.contour(ds_sic['x_stere'], ds_sic['y_stere'],
                   ds_sic.sel(time=date.strftime('%Y-%m-%d'))['sea_ice_concentration'], transform=crs_nsidc,
                           color=['purple'], ls='-',
               levels=[15], zorder=2, labels=False)
    
    ax.format(title=date.strftime('%Y-%m-%d %H:%M'), titlesize=10)
axs.format(abc=True)
fig.colorbar(c, label='Sea level pressure (hPa)', loc='r', shrink=0.75)
fig.save('../figures/fig02_slp_storms_overview.jpg', dpi=300)
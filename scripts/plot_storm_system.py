"""Visualizing storm systems with regridded ERA5 data
Module to be added: rudimentary storm track identification.

Requirements: 
- Interpolated buoy data
- drifter file 
- interpolated buoy data
- era5 data
"""
"""Visualizing storm systems with regridded ERA5 data
Module to be added: rudimentary storm track identification.

Requirements: 
- Interpolated buoy data
- drifter file 
- interpolated buoy data
- era5 data
"""

import xarray as xr
import os
import numpy as np
import proplot as pplt
import pandas as pd
import metpy.calc as mcalc
from metpy.units import units
import sys
#sys.path.append('../scripts/')
import drifter

era5_dataloc = '../data/era5/'
buoy_dataloc = '../data/interpolated_tracks//'

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

# Check: how can lat be empty at this point?
lat = pd.Series({buoy: buoy_data[buoy]['latitude'].median() for buoy in truncated_list})
lon = pd.Series({buoy: buoy_data[buoy]['longitude'].median() for buoy in truncated_list})
distant_buoys = lat[(lat < 87) | (lon < 80)].index.tolist()
near_buoys = [b for b in truncated_list if b not in distant_buoys]

for buoy in buoy_data:
    buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude']]
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True)
    buoy_data[buoy]['u'] = buoy_df['u']
    buoy_data[buoy]['v'] = buoy_df['v']
    
    buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude']].rolling('12H', center=True).mean()
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True)
    buoy_data[buoy]['smoothed_u'] = buoy_df['u']
    buoy_data[buoy]['smoothed_v'] = buoy_df['v']
    buoy_data[buoy]['smoothed_speed'] = buoy_df['speed']
    
storm_track = pd.read_csv('../../../data/storm_track.csv', index_col=0, parse_dates=True).iloc[4:].dropna()    

##### Load ERA5 data #####
variables = ['msl', 'u_950', 'v_950', 'q_925', 't_925']
savename = '2020-01-25_2020-02-05'
era5_data = {var: xr.open_dataset(era5_dataloc + 'era5_' + var + '_regridded_' + savename + '.nc') for var in variables}


dwp = mcalc.dewpoint_from_specific_humidity(pressure = 925*units('hPa'),
                                            temperature = era5_data['t_925']['t_925'].data * units('K'),
                                            specific_humidity = era5_data['q_925']['q_925'].data * units('kg/kg'))

theta_e = mcalc.equivalent_potential_temperature(pressure = 925 * units('hPa'),
                                       temperature = era5_data['t_925']['t_925'].data * units('K'),
                                       dewpoint = dwp)

ds_dwp = xr.Dataset({'td': (('time', 'xc', 'yc'), dwp.magnitude)},
                    coords=era5_data['t_925']['t_925'].coords)

ds_theta = xr.Dataset({'theta_e': (('time', 'xc', 'yc'), theta_e.magnitude)},
                    coords=era5_data['t_925']['t_925'].coords)

era5_data['theta_925'] = ds_theta

# Rotate U and V (could move this into the regridding section)
u = era5_data['u_950']['u_950']
v = era5_data['v_950']['v_950']
lon = u['longitude'] + 45 # NSIDC xstere is rotated
lat = v['latitude']
ustere = u * np.cos(np.deg2rad(lon)) - v * np.sin(np.deg2rad(lon))    
vstere = u * np.sin(np.deg2rad(lon)) + v * np.cos(np.deg2rad(lon))
era5_data['u_stere'] = xr.Dataset({'u_stere': ustere})
era5_data['v_stere'] = xr.Dataset({'v_stere': vstere})
era5_data['wind_speed'] = xr.Dataset({'wind_speed': 
                            np.sqrt(ustere**2 + vstere**2)})

# 2x4 plot with wind speed
left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
distant = ['2019P156', '2019P157']
ahead = ['2019P22']
l_sites = ['2019T67', '2019T65', '2019S94']
l_colors = {'2019T67': 'tab:blue',
            '2019T65': 'powder blue',
            '2019S94': 'tab:green'}

pplt.rc['title.bbox'] = True
pplt.rc['title.bboxalpha'] = 1
pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0



plot_scale = 0.8e3
fig, axs = pplt.subplots(width=10, nrows=2, ncols=4, share=True, span=False)
idx_skip = 2

plot_dates = ['2020-01-31 04:00', '2020-01-31 16:00', '2020-02-01 02:00', '2020-02-02 00:00']
plot_dates = [pd.to_datetime(x) for x in plot_dates]

for date, ax1, ax2 in zip(plot_dates, axs[0,:], axs[1,:]):
    x0 = storm_track.loc[date, 'x_stere'] # replace with storm track
    y0 = storm_track.loc[date, 'y_stere']
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    local_xu = ((X - x0)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y0)[::idx_skip, ::idx_skip])*1e-3

    local_x = (X - x0)*1e-3
    local_y = (Y - y0)*1e-3
    
    cbar1 = ax1.contourf(local_x, local_y, era5_data['theta_925'].sel(time=date)['theta_e'],
                        levels=np.arange(235, 285, 5), cmap='coolwarm', extend='both',
                        alpha=0.75, cmap_kw={'cut': 0.1})
    ax1.contour(local_x, local_y, era5_data['msl'].sel(time=date)['msl']/100, color='k',
                levels=np.arange(972, 1020, 4), labels=True, zorder=2)
    
    ax1.quiver(local_xu, local_yv,
              era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
              era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip], scale=400)

    ax1.format(title=date, ylabel='Y (km)', xlabel='X (km)',
         xlim=(-plot_scale, plot_scale), ylim=(-plot_scale, plot_scale),
          xticks=np.arange(-0.75e3, 0.8e3, 250), xtickminor=False, xrotation=90,
         yticks=np.arange(-0.75e3, 0.8e3, 250), ytickminor=False)
    
    
    for buoy in buoy_data:
        z = 4
        c = 'w'
        m = 'o'
        if buoy in left:
            c = 'lilac'
            m = 'o'
        elif buoy in right:
            c = 'gold'
            m = 'o'
        elif buoy in distant:
            c = 'orange'
            m = 'o'
        elif buoy in ahead:
            c = 'gray'
            m = 'o'
        elif buoy in l_sites:
            c = l_colors[buoy]
            z = 5
            m = 'o'

        if date in buoy_data[buoy].index:
            ax1.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x0/1e3,
                    buoy_data[buoy].loc[date, 'y_stere']/1e3 - y0/1e3, zorder=z,
                    edgecolor='k', edgewidth=0.5, marker=m, facecolor=c)

    ax1.plot(storm_track['x_stere']/1e3 - storm_track.loc[date, 'x_stere']/1e3,
            storm_track['y_stere']/1e3 - storm_track.loc[date, 'y_stere']/1e3,
            color='w', lw=2, zorder=3)


    x0 = storm_track.loc[date, 'x_stere'] # replace with storm track
    y0 = storm_track.loc[date, 'y_stere']
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    local_xu = ((X - x0)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y0)[::idx_skip, ::idx_skip])*1e-3

    local_x = (X - x0)*1e-3
    local_y = (Y - y0)*1e-3
    
    cbar2 = ax2.contourf(local_x, local_y, era5_data['wind_speed'].sel(time=date)['wind_speed'],
                       cmap='greens', extend='both', alpha=0.75, cmap_kw={'cut': 0.1}, vmin=0, vmax=20)
    
    ax2.contour(local_x, local_y, era5_data['msl'].sel(time=date)['msl']/100,
                color='k', levels=np.arange(972, 1020, 4),
                   labels=True, zorder=2)
    
    ax2.quiver(local_xu, local_yv,
              era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
              era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip], scale=400)

    ax1.format(title=date, ylabel='Y (km)', xlabel='X (km)',
         xlim=(-plot_scale, plot_scale), ylim=(-plot_scale, plot_scale),
          xticks=np.arange(-0.75e3, 0.8e3, 250), xtickminor=False, xrotation=90,
         yticks=np.arange(-0.75e3, 0.8e3, 250), ytickminor=False)
    
    for buoy in buoy_data:
        z = 4
        c = 'w'
        m = 'o'
        if buoy in west_buoys:
            c = 'lilac'
            m = 'o'
        elif buoy in se_buoys:
            c = 'gold'
            m = 'o'
        elif buoy in far_se_buoys:
            c = 'orange'
            m = 'o'
        elif buoy in l_sites:
            c = l_colors[buoy]
            z = 5
            m = 'o'

        if date in buoy_data[buoy].index:
            ax2.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x0/1e3,
                    buoy_data[buoy].loc[date, 'y_stere']/1e3 - y0/1e3, zorder=z,
                    edgecolor='k', edgewidth=0.5, marker=m, facecolor=c)

    ax2.plot(storm_track['x_stere']/1e3 - storm_track.loc[date, 'x_stere']/1e3,
            storm_track['y_stere']/1e3 - storm_track.loc[date, 'y_stere']/1e3,
            color='w', lw=2, zorder=3)
    ax2.format(title=date, ylabel='Y (km)', xlabel='X (km)',
         lltitle='$P_{min}$: ' + str(int(np.round(storm_track.loc[date, 'center_mslp']/100,0))) + ' hPa',
         xlim=(-plot_scale, plot_scale), ylim=(-plot_scale, plot_scale),
          xticks=np.arange(-0.75e3, 0.8e3, 250), xtickminor=False, xrotation=90,
         yticks=np.arange(-0.75e3, 0.8e3, 250), ytickminor=False)
    
axs[0,-1].colorbar(cbar1, label='$\\Theta_e$ (K)', loc='r', length=0.5)
axs[1,-1].colorbar(cbar2, label='$\\Theta_e$ (K)', loc='r', length=0.5)
# ax.colorbar(cbar, label='$U_{10}$ (m/s)', loc='r', length=0.5)       
fig.format(abc=True, leftlabels=['Equiv. pot. temperature',  'Surface wind speed'])
fig.save('../figures/janfeb_storm_2x4_theta_wind.png', dpi=300)
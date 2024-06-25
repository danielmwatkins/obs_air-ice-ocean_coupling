"""Visualizing storm systems with regridded ERA5 data
Module to be added: rudimentary storm track identification.
Uses 10m wind for the wind arrays, and contours to show the 950 hPa wind speed.
Plots propagation of storm from MSL.
Updated version shows contours for wind speed.

First figure: 3x4 showing SLP

Requirements: 
- Interpolated buoy data
- interpolated buoy data
- era5 data
"""
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import metpy.calc as mcalc
from metpy.units import units
import numpy as np
import os
import proplot as pplt
import pandas as pd
import sys
import warnings
import xarray as xr
from metpy.plots import ColdFront, WarmFront
warnings.simplefilter('ignore')

# Plot settings
pplt.rc['reso'] = 'med'
pplt.rc['cartopy.circular'] = False
pplt.rc['title.bbox'] = True
pplt.rc['title.bboxalpha'] = 1
pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0

# Data locations
era5_dataloc = '../data/era5_regridded/'
buoy_dataloc = '../data/interpolated_tracks/'

# Storm track generated in a different script
storm_track = pd.read_csv('../data/storm_track.csv', index_col=0, parse_dates=True).dropna()    

# Manual front identification
# Units are km from storm center
df = pd.read_csv('../data/fronts_relative_to_storm_track.csv', parse_dates=True)
fronts = {ftype: data for ftype, data in df.groupby('front_type')}
for ftype in fronts:
    fronts[ftype] = {date: data[['x', 'y']].rolling(3, center=True, min_periods=0).mean() for date, data in fronts[ftype].groupby('datetime')}

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

###### Defining the buoy groups ###########
# Intend to put this in a separate file so all figure plots can access it
left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P119']
distant = ['2019P156', '2019P157']
north = ['2019P22']
l_sites = ['2019T67', '2019T65', '2019S94']
l_colors = {'2019T67': 'tab:blue',
            '2019T65': 'powder blue',
            '2019S94': 'tab:green'}


##### Load ERA5 data #####
# I use the metpy library here to calculate the equivalent potential temperature
# Could replace with virtual potential temperature for consistency with Figure 5
variables = ['msl', 'u10', 'v10', 'u_950', 'v_950', 'q_925', 't_925']
savename = '2020-01-25_2020-02-05'
era5_data = {var: xr.open_dataset(era5_dataloc + 'era5_' + var + '_regridded_' + savename + '.nc') for var in variables}


dwp = mcalc.dewpoint_from_specific_humidity(pressure = 925*units('hPa'),
                                            temperature = era5_data['t_925']['t_925'].data * units('K'),
                                            specific_humidity = era5_data['q_925']['q_925'].data * units('kg/kg'))

theta_e = mcalc.equivalent_potential_temperature(pressure = 925 * units('hPa'),
                                       temperature = era5_data['t_925']['t_925'].data * units('K'),
                                       dewpoint = dwp)

ds_theta = xr.Dataset({'theta_e': (('time', 'xc', 'yc'), theta_e.magnitude)},
                    coords=era5_data['t_925']['t_925'].coords)

era5_data['theta_925'] = ds_theta

# Rotate U and V (could move this into the regridding section)
u = era5_data['u10']['u10']
v = era5_data['v10']['v10']
lon = np.deg2rad(u['longitude'] - 90) # Projected with central_longitude = 90, so this centers it
ustere = u * np.cos(lon) - v * np.sin(lon)    
vstere = u * np.sin(lon) + v * np.cos(lon)
era5_data['u_stere'] = xr.Dataset({'u_stere': ustere})
era5_data['v_stere'] = xr.Dataset({'v_stere': vstere})
era5_data['950_wind_speed'] = xr.Dataset({'wind_speed': 
                            np.sqrt(era5_data['u_950']['u_950']**2 + era5_data['v_950']['v_950']**2)})


plot_scale = 0.8e3 # Defines the figure size; units are kilometers
fig, axs = pplt.subplots(width=6, nrows=2, ncols=2, share=True, span=False)

idx_skip = 4
plot_dates = ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
plot_dates = [pd.to_datetime(x) for x in plot_dates]

for date, ax in zip(plot_dates, axs):
    # Current position of the storm track is the centered data
    x0 = storm_track.loc[date, 'x_stere'] 
    y0 = storm_track.loc[date, 'y_stere'] 
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    local_xu = ((X - x0)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y0)[::idx_skip, ::idx_skip])*1e-3
    U = era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip]
    V = era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip]
    

    local_x = (X - x0)*1e-3
    local_y = (Y - y0)*1e-3
    
    cbar1 = ax.contourf(local_x, local_y,
                        era5_data['theta_925'].sel(time=date)['theta_e'],
                        levels=np.arange(235, 285, 5),
                        cmap='BR', extend='both',
                        alpha=0.35, cmap_kw={'cut': -0.1}, zorder=0, vmin=225, vmax=295)
    ax.contour(local_x, local_y, era5_data['msl'].sel(time=date)['msl']/100, color='k',
                levels=np.arange(972, 1020, 4), lw=1, labels=True, zorder=2)
    
    ax.quiver(local_xu, local_yv, U, V, scale=250, width=1/500, headwidth=8)

    ax.format(title=date, ylabel='Y (km)', xlabel='X (km)', titlesize=12,
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
        elif buoy in north:
            c = 'gray'
            m = 'o'
        elif buoy in l_sites:
            c = l_colors[buoy]
            z = 5
            m = 's'

        if date in buoy_data[buoy].index:
            ax.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x0/1e3,
                    buoy_data[buoy].loc[date, 'y_stere']/1e3 - y0/1e3, zorder=z,
                    edgecolor='k', edgewidth=0.5, marker=m, ms=4, facecolor=c)
            
    # I use buoy 2019T66 as the location of the CO
    ax.plot(buoy_data['2019T66'].loc[date, 'x_stere']/1e3 - x0/1e3, 
            buoy_data['2019T66'].loc[date, 'y_stere']/1e3 - y0/1e3,
            zorder=6,
            marker='*', ms=10, color='firebrick', edgecolor='k', ew=0.5)

    ax.plot(storm_track['x_stere']/1e3 - storm_track.loc[date, 'x_stere']/1e3,
            storm_track['y_stere']/1e3 - storm_track.loc[date, 'y_stere']/1e3,
            facecolor='gray1', lw=1, zorder=3, m='^', ms=2, edgecolor='gray8', c='gray8', ew=0.5)

    wind_color = 'indigo'
    ax.contour(local_x, local_y, era5_data['950_wind_speed'].sel(time=date)['wind_speed'],
                       color=[wind_color], ls='--', levels=[16], zorder=4, labels=False, lw=2)
    ax.contour(local_x, local_y, era5_data['950_wind_speed'].sel(time=date)['wind_speed'],
                       color=[wind_color], levels=[20], zorder=4, labels=False, lw=2)
    
    ax.format(title=date, ylabel='Y (km)', xlabel='X (km)',
              xlim=(-plot_scale, plot_scale), ylim=(-plot_scale, plot_scale),
              xticks=np.arange(-0.75e3, 0.8e3, 250), xtickminor=False, xrotation=90,
              yticks=np.arange(-0.75e3, 0.8e3, 250), ytickminor=False)
    ax.text(-25, -25, 'L', fontsize=15, weight='bold', zorder=10)
# Add fronts

for color, ls, front in zip(['b', 'b', 'r'], ['-', '--', '-'],
                        [fronts['sfc_cold_front'], fronts['ele_cold_front'], fronts['sfc_warm_front']]):
    for ax, date in zip(axs, front):
        if len(front[date]['x']) == len(front[date]['y']):
            if color=='b':
                ax.plot(front[date]['x'].values,
                    front[date]['y'].values, color=color,
                    ls=ls, marker='', path_effects=[ColdFront(size=3, spacing=4, flip=False)], zorder=10)                      
            else:
                ax.plot(front[date]['x'].values,
                    front[date]['y'].values, color=color,
                    ls=ls, path_effects=[WarmFront(size=3, spacing=4, flip=False)], zorder=10)

        ax.format(xreverse=False, yreverse=False)

# Vector legend
# Need to manually set the location
ax.quiver(120,
          -640,
          20,
          0,
          scale=300, headwidth=4, c = 'tab:blue', zorder=6, width=1/250)
ax.text(250, -670, '20 m/s wind', c='tab:blue', zorder=6)
rec = Rectangle((80, -750), 700, 220) 
pc = PatchCollection([rec], facecolor='w', alpha=1,
                         edgecolor='k', zorder=5)
ax.add_collection(pc)

# Generate legend manually for finer control
h, l = [], []
for c, ls, label in zip(['k', wind_color, wind_color, 'gray8'],
                    ['-', '--', '-', '-'],
                    ['SLP (hPa)', '16 m/s wind', '20 m/s wind', 'Storm track']):
    if label == 'SLP (hPa)':
        lw = 1
    else:
        lw = 2
    if label == 'Storm track':
        h.append(ax.plot([],[], color=c, facecolor='gray1', edgecolor=c, ew=0.5, m='^', ls=ls, lw=1))    
    else:
        h.append(ax.plot([],[],color=c,  ls=ls, lw=lw))
    l.append(label)
axs[0].legend(h, l, loc='ul', alpha=1, ncols=1, fontsize=9) 
    
fig.colorbar(cbar1, label='$\\Theta_e$ (K)', loc='r', length=0.75)
fig.format(abc=True) # Adds abc labels
fig.save('../figures/fig03_storm_centered.jpg', dpi=300)
fig.save('../figures/fig03_storm_centered.pdf', dpi=300)

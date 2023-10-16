import pandas as pd
import proplot as pplt
import pyproj
import numpy as np
import os

dataloc = '../data/interpolated_tracks/'
zoom_plot_dates = ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
zoom_plot_dates = [pd.to_datetime(x) for x in zoom_plot_dates]

buoy_data = {}
for f in os.listdir(dataloc):
    if f[0] != '.':
        dn_id, imei, sensor_id = f.split('.')[0].split('_')
        buoy_data[sensor_id] = pd.read_csv(dataloc + f, parse_dates=True, index_col='datetime')

left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
distant = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
co = ['2019T66']
site_specs = {'2019T67': ('tab:blue', 's', 7),
               '2019T65': ('powder blue', 's', 7),
               '2019S94': ('tab:green', 's', 7),
               '2019T66': ('tab:red', '*', 15)}

##### Velocity time series plots ########
ts = slice('2020-01-30 20:00', '2020-02-02 02:00')
fig, axs = pplt.subplots(width=5, height=6, nrows=3, sharey=False)
for var, ax in zip(['u', 'v', 'speed'], axs):
    for b in buoy_data:

        z = 2
        lw = 0.7
        ls = '-'
        if b in left:
            c = 'lilac'
        elif b in right:
            c = 'gold'
        elif b in distant:
            c = 'orange'

        elif b in site_specs:
            c = site_specs[b][0]
            lw = 2
            z = 5
        else:
            c = 'k'
            z = 0
        if b == '2019P22':
            c = 'gray'
            
        ax.plot(buoy_data[b].loc[ts, var].resample('1H').asfreq(),
                c=c, zorder=z, marker='', lw=lw, ls=ls)

    ax.format(ylabel=var + ' (m/s)', xlabel='', xrotation=45, 
              xminorlocator=1/12, xgridminor=True)
    


for abc, date in zip(['d', 'e', 'f', 'g'], zoom_plot_dates):
    for ax in axs:
        ax.axvline(date, color='tab:blue', lw=0.5, zorder=0)

    axs[0].text(date + pd.to_timedelta('30min'), 0.5, abc, color='tab:blue', zorder=4)
    axs[1].text(date + pd.to_timedelta('30min'), 0.5, abc, color='tab:blue', zorder=4)
    axs[2].text(date + pd.to_timedelta('30min'), 0.525, abc, color='tab:blue', zorder=4)

axs[0].format(ylim=(-0.4, 0.6))
axs[1].format(ylim=(-0.4, 0.6))
axs[2].format(ylim=(-0.05, 0.6))
for ax in axs:
    ax.axhline(0, color='gray', lw=1, alpha=0.5, zorder=0)
h = []
l = []
for color, label in zip(
    ['lilac',  'gold', 'orange', 'gray', 'k', #'tab:red',
     'tab:blue', 'powder blue', 'tab:green'],
    ['Left', 'Right', 'Distant', 'Ahead', 'DN',  #'CO',
     'L1', 'L2', 'L3']):
    if label in ['CO', 'L1', 'L2', 'L3']:
        lw = 3
    else:
        lw = 3
    if label == 'CO':
        ls = '--'
    else:
        ls = '-'

    h.append(ax.plot([],[], lw=lw, color=color, ls=ls))
    l.append(label)
ax.legend(h, l, ncols=2, loc='ul', alpha=1, order='F')
for ax, label in zip(axs, ['a','b','c']):
    ax.format(ltitle=label)

fig.save('../figures/fig06a_velocity_timeseries_ice_stereographic_uv.jpg', dpi=300)
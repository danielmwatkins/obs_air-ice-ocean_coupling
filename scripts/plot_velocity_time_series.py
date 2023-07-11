import pandas as pd
import proplot as pplt
import pyproj
import numpy as np
import os

dataloc = '../data/interpolated_tracks/'

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
               '2019T65': ('gold', 's', 7),
               '2019S94': ('tab:green', 's', 7),
               '2019T66': ('tab:red', '*', 15)}

###### Maps ########
pol_stere_proj = 'epsg:3413'
npstere_crs = pyproj.CRS(pol_stere_proj)
source_crs = pyproj.CRS("epsg:4326") # Global lat-lon coordinate system
latlon_to_polar = pyproj.Transformer.from_crs(source_crs, npstere_crs, always_xy=True)
for buoy in buoy_data:
    x, y = latlon_to_polar.transform(buoy_data[buoy].longitude, buoy_data[buoy].latitude)
    buoy_data[buoy]['x_stere'] = x
    buoy_data[buoy]['y_stere'] = y

fig, ax0 = pplt.subplots(ncols=1, width=4, share=False)
date = '2020-02-01 00:00'
all_buoys = [b for b in buoy_data if date in buoy_data[b].index]

df_x = pd.DataFrame({buoy: buoy_data[buoy].loc[date, 'x_stere'] for buoy in all_buoys}, index=all_buoys)/1e3
df_y = pd.DataFrame({buoy: buoy_data[buoy].loc[date, 'y_stere'] for buoy in all_buoys}, index=all_buoys)/1e3
x0 = df_x['2019T66']
y0 = df_y['2019T66']
df_x -= x0
df_y -= y0

dn_buoys = [b for b in all_buoys if b not in left + right + distant]


ax1 = ax0.inset(
    [-530, -530, 450, 450], transform='data', zoom=True,
    zoom_kw={'ec': 'gray', 'ls': '-', 'lw': 1}
)


ax0.plot(df_x, df_y, marker='o', c='w', edgecolor='k', ms=3, edgewidth=0.5)
ax1.plot(df_x[dn_buoys], df_y[dn_buoys], marker='o', c='w', edgecolor='k', ms=4, edgewidth=0.5)

for group, color in zip([left, right, distant], ['lilac', 'powder blue', 'orange']):
    ax0.plot(df_x[group], df_y[group], marker='o', c=color, edgecolor='k', ms=5, edgewidth=0.5)

for buoy in site_specs:
    color, shape, size = site_specs[buoy]
    if buoy == '2019T66':
        ax0.plot(df_x[buoy], df_y[buoy], color=color, marker=shape, ms=size, edgecolor='k', edgewidth=0.5)
    ax1.plot(df_x[buoy], df_y[buoy], color=color, marker=shape, ms=size, edgecolor='k', edgewidth=0.5)

ax0.format(xlim=(-550, 450), ylim=(-550, 450),
           xlocator=np.arange(-400, 401, 200), xtickminor=False,
           ylocator=np.arange(-400, 401, 200), ytickminor=False,
           ylabel='Y (km)', xlabel='X (km)')
ax1.format(xlim=(-55,45), ylim=(-55,45),
           xticks=[], yticks=[], xlabel='', ylabel='')

h = []
l = []
for color, label, m in zip(
    ['tab:red', 'tab:blue', 'gold', 'tab:green', 'w'],
    ['CO', 'L1', 'L2', 'L3', 'P'],
    ['*', 's', 's', 's', 'o']):
    if label=='CO':
        s = 10
    else:
        s = 5
    h.append(ax0.plot([],[], m=m, ms=s, lw=0, color=color, edgecolor='k'))
    l.append(label)
ax0.legend(h, l, loc='lr', ncols=1, pad=0.5)
fig.format(title='MOSAiC Distributed Network', fontsize=12)
fig.save('../figures/distributed_network_map.png', dpi=300)


##### Velocity time series plots ########
ts = slice('2020-01-30 20:00', '2020-02-02 02:00')
fig, axs = pplt.subplots(width=8, height=6, nrows=3, sharey=False)
for var, ax in zip(['u', 'v', 'speed'], axs):
    for b in buoy_data:

        z = 2
        lw = 0.7
        ls = '-'
        if b in left:
            c = 'lilac'
        elif b in right:
            c = 'powder blue'
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
        if b == '2019T66':
            z += 1
            ls = '--'
            
        ax.plot(buoy_data[b].loc[ts, var].resample('1H').asfreq(),
                c=c, zorder=z, marker='', lw=lw, ls=ls)

    ax.format(ylabel=var + ' (m/s)', xlabel='', xrotation=45, xformatter='%b %d %HZ',
             xlocator=1/2,
              xminorlocator=1/6, xgridminor=True, suptitle='Drift velocity')
    
zoom_plot_dates = ['2020-01-31 16:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
zoom_plot_dates = [pd.to_datetime(x) for x in zoom_plot_dates]


for abc, date in zip(['a', 'b', 'c', 'd'], zoom_plot_dates):
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
    ['lilac',  'powder blue', 'orange', 'gray', 'k', 'tab:red', 'tab:blue', 'gold', 'tab:green'],
    ['Left', 'Right', 'Distant', 'Ahead', 'DN',  'CO', 'L1', 'L2', 'L3']):
    if label in ['CO', 'L1', 'L2', 'L3']:
        lw = 2
    else:
        lw = 1
    if label == 'CO':
        ls = '--'
    else:
        ls = '-'

    h.append(ax.plot([],[], lw=lw, color=color, ls=ls))
    l.append(label)
ax.legend(h, l, ncols=2, loc='ul', alpha=1, order='F')
    
fig.save('../figures/velocity_timeseries_ice_stereographic_uv.jpg', dpi=300)
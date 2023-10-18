import cartopy.crs as ccrs
import pandas as pd
import proplot as pplt
import pyproj
import numpy as np
import os
import warnings
warnings.simplefilter('ignore')
dataloc = '../data/interpolated_tracks/'

buoy_data = {}
for f in os.listdir(dataloc):
    if f[0] != '.':
        dn_id, imei, sensor_id = f.split('.')[0].split('_')
        buoy_data[sensor_id] = pd.read_csv(dataloc + f, parse_dates=True, index_col='datetime')

left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
distant = ['2019P156', '2019P157']
ahead = ['2019P22']
l_sites = ['2019T67', '2019T65', '2019S94']
co = ['2019T66']
site_specs = {'2019T67': ('tab:blue', 's', 8, 1),
               '2019T65': ('powder blue', 's', 8, 2),
               '2019S94': ('tab:green', 's', 8, 3),
               '2019T66': ('tab:red', '*', 15, 0)}
date = '2020-02-01 00:00'
all_buoys = [b for b in buoy_data if date in buoy_data[b].index]
dn_buoys = [b for b in all_buoys if b not in left + right + distant]



pplt.rc.reso='med'
pplt.rc['cartopy.circular'] = False

crs = ccrs.NorthPolarStereo(central_longitude=90, true_scale_latitude=70)
fig, axs = pplt.subplots(proj='npstere', proj_kw={'lon_0': 90, 'true_scale_latitude': 80}, ncols=2, width=6)
axs.format(land=True, latgrid=True, longrid=True, latmax=90, latlocator=1, lonlocator=10, latlabels=True, lonlabels=True)
offset = 300e3
x0 = 23255
y0 = -276124 - offset
dx = 500e3
ax = axs[0]
ax.set_extent([x0-dx, x0+dx, y0-dx, y0+dx], crs=crs)

df_x = pd.Series({buoy: buoy_data[buoy].loc[date, 'x_stere'] for buoy in all_buoys})
df_y = pd.Series({buoy: buoy_data[buoy].loc[date, 'y_stere'] for buoy in all_buoys})

for group, color in zip([left, right, distant, ahead, co], ['lilac', 'gold', 'orange', 'gray', 'firebrick']):
    if color == 'firebrick':
        m = '*'
        ms = 15
    else:
        m = 'o'
        ms = 5
    ax.plot(df_x[group], df_y[group], marker=m, c=color, lw=0, edgecolor='k', ms=ms, edgewidth=0.5, transform=crs)

x0 -= 50e3
ax.plot([x0 +250e3, x0 + 450e3], [y0 - 0.75*dx, y0 - 0.75 * dx], color='k', transform=crs, lw=5)
ax.plot([x0 +350e3, x0 + 445e3], [y0 - 0.75*dx, y0 - 0.75 * dx], color='w', transform=crs, lw=4)
ax.text(x0 +230e3, y0 - 0.7*dx, 0)
ax.text(x0 +310e3, y0 - 0.7*dx, '100')
ax.text(x0 +420e3, y0 - 0.7*dx, '200')
ax.text(x0 + 320e3, y0-0.9*dx, 'km')

ax = axs[1]
dx = 60e3
x0 = 23255
y0 = -276124 + 20e3
ax.set_extent([x0-dx, x0+dx, y0-dx, y0+dx], crs=crs)
axs[0].plot([x0-dx, x0-dx, x0+dx, x0+dx, x0-dx], [y0-dx, y0+dx, y0+dx, y0-dx, y0-dx], color='b', lw=0.5, transform=crs)

ax.plot(df_x[dn_buoys], df_y[dn_buoys], marker='o', c='w', lw=0, edgecolor='k', ms=4, edgewidth=0.5, transform=crs)

for buoy in site_specs:
    color, shape, size, num = site_specs[buoy]
    if buoy == '2019T66':
        ax.plot(df_x[buoy], df_y[buoy], color=color, marker=shape, ms=size, lw=0, edgecolor='k', edgewidth=0.5, transform=crs)
    else:
        ax.plot(df_x[buoy], df_y[buoy], color=color, marker=shape, ms=10, lw=0, edgecolor='k', edgewidth=0.5, transform=crs)
        ax.text(df_x[buoy]-1.2e3, df_y[buoy]-1.4e3, num, transform=crs, color='w', fontsize=8)

h = []
l = []
for color, label, m in zip(
    ['tab:red', 'tab:blue', 'powder blue', 'tab:green', 'w', 'lilac', 'gold', 'orange', 'gray'],
    ['CO', 'L1', 'L2', 'L3', 'P', 'left', 'right', 'distant', 'ahead'],
    ['*', 's', 's', 's', 'o', 'o', 'o', 'o', 'o']):
    if label=='CO':
        s = 10
    else:
        s = 5
    h.append(ax.plot([],[], m=m, ms=s, lw=0, color=color, edgecolor='k'))
    l.append(label)
ax.legend(h[0:5], l[0:5], ncols=1, loc='ll')
axs[0].legend([h[0]] + h[5:], [l[0]] + l[5:], ncols=1, loc='ll')
axs[0].format(title='Extended DN')
axs[1].format(title='Distributed Network')

fig.save('../figures/fig01_distributed_network_map.png', dpi=300)
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
ahead = ['2019P22']
l_sites = ['2019T67', '2019T65', '2019S94']
co = ['2019T66']
site_specs = {'2019T67': ('tab:blue', 's', 7),
               '2019T65': ('powder blue', 's', 7),
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


#### Lat/lon lines ####
from scipy.interpolate import interp1d

crs0 = pyproj.CRS('WGS84')
crs1 = pyproj.CRS('epsg:3413')
transformer_ll = pyproj.Transformer.from_crs(crs0, crs_to=crs1, always_xy=True)
transformer_xy = pyproj.Transformer.from_crs(crs1, crs_to=crs0, always_xy=True)

lats = np.arange(75, 91, 2.5)
lons = np.arange(-180, 181, 10)
lons, lats = np.meshgrid(lons, lats)
xylon, xylat = transformer_ll.transform(lons, lats)
xylon = xylon * 1e-3
xylat = xylat * 1e-3

# x0 = 0.4e6
# y0 = -1.1e6
lat_labels = []
lat_y = []
lon_labels = []
lon_x = []

for idx in range(0, xylon.shape[0]):
    if np.any(xylon[idx,:] < x0['2019T66']) & np.any(xylon[idx,:] > x0['2019T66']):
        y = interp1d(xylon[idx,:], xylat[idx,:])(x0['2019T66'])
        lat_y.append(y)
        lat_labels.append(lats[idx,0])
for idx in range(0, xylon.shape[1]):
    if np.any(xylat[:,idx] < y0['2019T66']) & np.any(xylat[:,idx] > y0['2019T66']):
        if np.any(xylon[:,idx] < x0['2019T66']) & np.any(xylon[:,idx] > x0['2019T66']):            
            x = interp1d(xylat[:,idx], xylon[:,idx])(y0['2019T66'])
            lon_x.append(x)
            lon_labels.append(lons[0,idx])
            
lat_y = list(np.array(lat_y))
lat_labels = [str(x) + '$^\circ$' for x in lat_labels]
lon_labels = [str(x) + '$^\circ$' for x in lon_labels]
lon_x = list(np.array(lon_x))
####

dn_buoys = [b for b in all_buoys if b not in left + right + distant]
for idx in range(xylon.shape[1]):
    ax0.plot(xylon[:,idx] - x0['2019T66'], xylat[:,idx] - y0['2019T66'], color='k', alpha=0.5, lw=0.5)
for idx in range(xylon.shape[0]):
    
    ax0.plot(xylon[idx,:] - x0['2019T66'], xylat[idx,:] - y0['2019T66'], color='k', alpha=0.5, lw=0.5)

ax1 = ax0.inset(
    [-530, -530, 450, 450], transform='data', zoom=True, # Check if zoom lets you choose the corners
    zoom_kw={'ec': 'gray', 'ls': '-', 'linewidths': 0.5}
)


ax0.plot(df_x, df_y, marker='o', c='w', edgecolor='k', ms=3, edgewidth=0.5)
ax1.plot(df_x[dn_buoys], df_y[dn_buoys], marker='o', c='w', edgecolor='k', ms=4, edgewidth=0.5)

for group, color in zip([left, right, distant, ahead], ['lilac', 'gold', 'orange', 'gray']):
    ax0.plot(df_x[group], df_y[group], marker='o', c=color, edgecolor='k', ms=5, edgewidth=0.5)

for buoy in site_specs:
    color, shape, size = site_specs[buoy]
    if buoy == '2019T66':
        ax0.plot(df_x[buoy], df_y[buoy], color=color, marker=shape, ms=size, edgecolor='k', edgewidth=0.5)
    ax1.plot(df_x[buoy], df_y[buoy], color=color, marker=shape, ms=size, edgecolor='k', edgewidth=0.5)

ax1.plot([20, 40], [-50, -50], lw=2, color='k')
ax1.text(20, -45, '20 km')
ax0.format(xlim=(-550, 450), ylim=(-550, 450),
           xlocator=np.arange(-400, 401, 200), xtickminor=False,
           ylocator=np.arange(-400, 401, 200), ytickminor=False,
           ylabel='Y (km)', xlabel='X (km)')
ax1.format(xlim=(-55,45), ylim=(-55,45),
           xticks=[], yticks=[], xlabel='', ylabel='')

h = []
l = []
for color, label, m in zip(
    ['tab:red', 'tab:blue', 'powder blue', 'tab:green', 'w', 'lilac', 'gold', 'orange', 'gray'],
    ['CO', 'L1', 'L2', 'L3', 'DN', 'left', 'right', 'distant', 'ahead'],
    ['*', 's', 's', 's', 'o', 'o', 'o', 'o', 'o']):
    if label=='CO':
        s = 10
    else:
        s = 5
    h.append(ax0.plot([],[], m=m, ms=s, lw=0, color=color, edgecolor='k'))
    l.append(label)
ax0.legend(h, l, loc='lr', ncols=2, order='F', pad=0.5, alpha=1)
fig.format(title='MOSAiC Distributed Network', fontsize=12)
fig.save('../figures/fig01_distributed_network_map.png', dpi=300)


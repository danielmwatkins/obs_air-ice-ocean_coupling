import sys
sys.path.append('../scripts')
import drifter
import pandas as pd
import proplot as pplt
import numpy as np
import os
import pyproj

dataloc = '../data/interpolated_tracks/'

left = ['2019P128', '2019P184', '2019P182', '2019P127']
right = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
distant = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
ahead = ['2019P22']
co = ['2019T66']
site_specs = {'2019T67': ('tab:blue', 's', 7),
               '2019T65': ('powder blue', 's', 7),
               '2019S94': ('tab:green', 's', 7),
               '2019T66': ('tab:red', '*', 15)}

buoy_data = {}
for f in os.listdir(dataloc):
    if f[0] != '.':
        dn_id, imei, sensor_id = f.split('.')[0].split('_')
        buoy_data[sensor_id] = pd.read_csv(dataloc + f, parse_dates=True, index_col='datetime')

s_track = pd.read_csv('../data/storm_track.csv', index_col=0, parse_dates=True)
s_track = s_track.loc[slice('2020-01-31 12:00', '2020-02-02 00:00')]
    
polygons = {'Left 1': ['2019P184', '2019P127', '2019P182', '2019P128'],
            'Left 2': ['2019P184', '2019P124', '2019O6', '2019P127'],
            'Left 3': ['2019O1', '2019P127','2019O6'],
            'DN_set_1': ['2019P124', '2019P125', '2019P102', '2019P198'],
            'DN_set_2': ['2019P90', '2019P91', '2019P193', '2019P196'],
            'DN_set_3': ['2019P136', '2019P187', '2019P92', '2019P103'],
            'DN_set_4': ['2019P191', '2019P148', '2019P139', '2019P195'],
            'DN_set_5': ['2019P143', '2019P203', '2019T69', '2019P105'],
            'l_sites': [ '2019T65', '2019T67', '2019S94'],
            'Full DN': ['2019O5', '2019P91', '2019P187', '2019P191',
                        '2019P148', '2019P124'],
            'North group': ['2019P22', '2019P91', '2019P187'],
            'Right group 1': ['2019P123', '2019P112', '2019P187'],
            'Right group 2': ['2019P114', '2019P113', '2019P155'],
            'Right group 3': ['2019P113', '2019P92', '2019P137', '2019P119'],
            'Distant group': ['2019P123', '2019P157', '2019P156', '2019P155'],
            'Very large group': ['2019P22', '2019P123', '2019P157', '2019P156',
                                 '2019P155', '2019P182', '2019P128', '2019P184',
                                 '2019P124']}

colors = {'Left 1': 'lilac',
          'Left 2': 'purple',
          'Left 3': 'maroon',
          'DN_set_1': 'k',
          'DN_set_2': 'k',
          'DN_set_3': 'k',
          'DN_set_4': 'k',
          'DN_set_5': 'k',
          'l_sites': 'tab:orange',
          'Full DN': 'tab:blue',
          'North group': 'green',
          'Right group 1': 'goldenrod',
          'Right group 2': 'gold',
          'Right group 3': 'yellow',
          'Distant group': 'orange',
          'Very large group': 'forest green'}

lstyles = {'DN_set_1': '-',
           'DN_set_2': '--',
           'DN_set_3': '-.',
           'DN_set_4': ':',
           'DN_set_5': '-'}    

strain_rates = {}
for set_name in polygons:
    strain_rates[set_name] = drifter.compute_strain_rate_components(polygons[set_name][::-1], buoy_data)


    
###### Maps ########
pol_stere_proj = 'epsg:3413'
npstere_crs = pyproj.CRS(pol_stere_proj)
source_crs = pyproj.CRS("epsg:4326") # Global lat-lon coordinate system
latlon_to_polar = pyproj.Transformer.from_crs(source_crs, npstere_crs, always_xy=True)
for buoy in buoy_data:
    x, y = latlon_to_polar.transform(buoy_data[buoy].longitude, buoy_data[buoy].latitude)
    buoy_data[buoy]['x_stere'] = x
    buoy_data[buoy]['y_stere'] = y

fig, ax0 = pplt.subplots(ncols=1, height=4, share=False)
date = '2020-02-01 00:00'
all_buoys = [b for b in buoy_data if date in buoy_data[b].index]

df_x = pd.DataFrame({buoy: buoy_data[buoy].loc[:, 'x_stere'] for buoy in all_buoys})/1e3
df_y = pd.DataFrame({buoy: buoy_data[buoy].loc[:, 'y_stere'] for buoy in all_buoys})/1e3
x0 = df_x.loc[date, '2019T66']
y0 = df_y.loc[date, '2019T66']
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
    if np.any(xylon[idx,:] < x0) & np.any(xylon[idx,:] > x0):
        y = interp1d(xylon[idx,:], xylat[idx,:])(x0)
        lat_y.append(y)
        lat_labels.append(lats[idx,0])
for idx in range(0, xylon.shape[1]):
    if np.any(xylat[:,idx] < y0) & np.any(xylat[:,idx] > y0):
        if np.any(xylon[:,idx] < x0) & np.any(xylon[:,idx] > x0):            
            x = interp1d(xylat[:,idx], xylon[:,idx])(y0)
            lon_x.append(x)
            lon_labels.append(lons[0,idx])
            
lat_y = list(np.array(lat_y))
lat_labels = [str(x) + '$^\circ$' for x in lat_labels]
lon_labels = [str(x) + '$^\circ$' for x in lon_labels]
lon_x = list(np.array(lon_x))
####

dn_buoys = [b for b in all_buoys if b not in left + right + distant]
for idx in range(xylon.shape[1]):
    ax0.plot(xylon[:,idx] - x0, xylat[:,idx] - y0, color='k', alpha=0.5, lw=0.5)
for idx in range(xylon.shape[0]):
    
    ax0.plot(xylon[idx,:] - x0, xylat[idx,:] - y0, color='k', alpha=0.5, lw=0.5)

ax1 = ax0.inset(
    [-530, -530, 450, 450], transform='data', zoom=True, # Check if zoom lets you choose the corners
    zoom_kw={'ec': 'gray', 'ls': '-', 'linewidths': 0.5}
)


ax0.plot(df_x.loc[date,:], df_y.loc[date,:], marker='o', c='w', lw=0,
         edgecolor='k', ms=3, edgewidth=0.5, zorder=1)
ax1.plot(df_x.loc[date, dn_buoys], df_y.loc[date, dn_buoys], lw=0,
         marker='o', c='w', edgecolor='k', ms=4, edgewidth=0.5, zorder=4)

for group, color in zip([left, right, distant, ahead], ['lilac', 'gold', 'orange', 'gray']):
    ax0.plot(df_x.loc[date, group], df_y.loc[date, group], lw=0,
             marker='.', c=color, edgecolor='k', ms=5, edgewidth=0.5, zorder=4)

for buoy in site_specs:
    color, shape, size = site_specs[buoy]
    if buoy == '2019T66':
        ax0.plot(df_x.loc[date, buoy], df_y.loc[date, buoy], color=color,
                 marker=shape, ms=12, edgecolor='k', edgewidth=0.5, zorder=5)
        ax1.plot(df_x.loc[date, buoy], df_y.loc[date, buoy], color=color,
                 marker=shape, ms=size, edgecolor='k', edgewidth=0.5, zorder=5)
    else:
        ax1.plot(df_x.loc[date, buoy],
             df_y.loc[date, buoy], color=color, lw=0, zorder=5,
             marker=shape, ms=5, edgecolor='k', edgewidth=0.5)

# Plot storm track
ax0.plot(s_track['x_stere']/1e3 - x0, s_track['y_stere']/1e3 - y0, lw=0.5,
         color='gray', ls='--', m='', zorder=0)


# Overlay polygons
l = []
h = []
for set_name in ['Full DN', 'Left 1', 'Left 2', 'Left 3', 'North group']:
    buoy_set = polygons[set_name]
    zorder=6
    lw=1

    h.append(ax0.plot(df_x.loc[date, buoy_set + [buoy_set[0]]],
            df_y.loc[date, buoy_set + [buoy_set[0]]],
                label=set_name, marker='', lw=lw, zorder=zorder, color=colors[set_name]))
    l.append(set_name)

for set_name in ['Full DN', 'DN_set_1', 'DN_set_2', 'DN_set_3',
                 'DN_set_4', 'DN_set_5', 'l_sites']:
    buoy_set = polygons[set_name]
    ls = '-'
    if set_name[0] == 'D':
        ls = lstyles[set_name]
    if set_name in ['Full DN', 'l_sites']:
        zorder = 2
        lw = 2
    elif set_name == 'DN_set_5':
        zorder = 2
        lw = 1.5
    else:
        zorder = 3
        lw = 1
    if set_name != 'Full DN':
        h.append(ax1.plot(df_x.loc[date, buoy_set + [buoy_set[0]]],
            df_y.loc[date, buoy_set + [buoy_set[0]]],
                label='', marker='', lw=lw, zorder=zorder,
             color=colors[set_name], ls=ls))
        l.append(set_name)
    else:
        ax1.plot(df_x.loc[date, buoy_set + [buoy_set[0]]],
            df_y.loc[date, buoy_set + [buoy_set[0]]],
                label='', marker='', lw=lw, zorder=zorder,
             color=colors[set_name], ls=ls)


ax0.legend(h, l, loc='r', ncols=1)


    
ax0.format(xlim=(-550, 450), ylim=(-550, 450),
           xlocator=np.arange(-400, 401, 200), xtickminor=False,
           ylocator=np.arange(-400, 401, 200), ytickminor=False,
           ylabel='Y (km)', xlabel='X (km)')
ax1.format(xlim=(-55,45), ylim=(-55,45),
           xticks=[], yticks=[], xlabel='', ylabel='')

h = []
l = []
for color, label, m in zip(
    ['tab:red', 'tab:blue', 'powder blue', 'tab:green', 'w'],
    ['CO', 'L1', 'L2', 'L3', 'P'],
    ['*', 's', 's', 's', 'o']):
    if label=='CO':
        s = 10
    else:
        s = 5
    h.append(ax0.plot([],[], m=m, ms=s, lw=0, color=color, edgecolor='k'))
    l.append(label)
# ax0.legend(h, l, loc='lr', ncols=1, pad=0.5, alpha=1)
fig.format(title='', fontsize=12)
fig.save('../figures/deformation_polygons_map.png', dpi=300)

### Deformation plot next    
    
    
    

ts = slice('2020-01-30 20:00', '2020-02-02 02:00')
fig, ax = pplt.subplots(width=5, height=6, nrows=3, sharey=False)

for set_name in ['Full DN', 'l_sites', 'DN_set_1', 'DN_set_2', 'DN_set_3', 'DN_set_4', 'DN_set_5']:
    if set_name[0] == 'D':
        ls = lstyles[set_name]
        lw = 1
        label = set_name
    else:
        ls = '-'
        lw = 1
        label = set_name
    if set_name in ['Full DN', 'l_sites', 'DN_set_5']:
        lw = 1.5

        
    print(set_name, np.round(strain_rates[set_name].area.loc[ts].mean()**0.5/1e3), 'km')
    ax[0].plot(strain_rates[set_name].divergence.loc[ts], color=colors[set_name], ls=ls, lw=lw, label=label)
    ax[1].plot(strain_rates[set_name].maximum_shear_strain_rate.loc[ts], ls=ls, color=colors[set_name], lw=lw, label=label)    
    ax[2].plot(strain_rates[set_name].vorticity.loc[ts], color=colors[set_name], ls=ls, lw=lw, label=label)        
    ax[0].axhline(0, color='k', lw=0.5) 
    ax[2].axhline(0, color='k', lw=0.5)
    ax[0].format(ultitle='divergence', ylabel='$\\nabla \cdot \vec u$ (s$^{-1}$)')
    ax[1].format(ultitle='maximum shear strain rate', ylabel='$\epsilon_{II}$ (s$^{-1}$)')
    ax[2].format(ultitle='vorticity', ylim=(-7.5e-6, 5.5e-6),
                 ylabel='$\\nabla \\times \vec u$ (s$^{-1}$)')
ax[2].legend(loc='ll', ncols=2)
ax.format(xrotation=45, xlabel='')
fig.save('../figures/strain_rates_DN.jpg', dpi=300)
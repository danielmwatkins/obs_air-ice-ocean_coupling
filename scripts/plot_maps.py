import cartopy.crs as ccrs
import pandas as pd
import proplot as pplt
import pyproj
import numpy as np
import os
import warnings
warnings.simplefilter('ignore')
dataloc = '../data/interpolated_tracks/'


def scalebar(ax, x0, y0, length, az=90, yoffset=1e3, xoffset=-1e3):
    """Plot a scale bar on axis ax given an origin in 
    polar stereographic coordinates with lat_0=90 and true scale latitude 70
    """
    
    g = pyproj.Geod(ellps='WGS84')
    proj_LL = 'epsg:4326' # WGS 84 Ellipsoid
    proj_XY = '+proj=stere +lat_0=90 +lat_ts=70 +lon_0=90 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs'
    crs = ccrs.NorthPolarStereo(central_longitude=90, true_scale_latitude=70)

    transform_to_ll = pyproj.Transformer.from_crs(proj_XY, proj_LL, always_xy=True)
    transform_to_ps = pyproj.Transformer.from_crs(proj_LL, proj_XY, always_xy=True)
    lon0, lat0 = transform_to_ll.transform(x0, y0)
    lon1, lat1, ba = g.fwd(lons=lon0, lats=lat0, az=az, dist=length*1e3)
    x1, y1 = transform_to_ps.transform(lon1, lat1)

    ax.text((x0 + x1)/2 + xoffset, (y0 + y1)/2 + yoffset, str(length) + ' km')
    ax.plot([x0, x1], [y0, y1], c='k', lw=3, transform=crs)

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
# x0 = 23255
# y0 = -276124 - offset
x0 = 28887
y0 = -268774 - offset
dx = 500e3
ax = axs[0]
ax.set_extent([x0-dx, x0+dx, y0-dx, y0+dx], crs=crs)

df_x = pd.Series({buoy: buoy_data[buoy].loc[date, 'x_stere'] for buoy in all_buoys})
df_y = pd.Series({buoy: buoy_data[buoy].loc[date, 'y_stere'] for buoy in all_buoys})
# print(df_x['2019T66'], df_y['2019T66'])
for group, color in zip([left, right, distant, ahead, co], ['lilac', 'gold', 'orange', 'gray', 'firebrick']):
    if color == 'firebrick':
        m = '*'
        ms = 15
    else:
        m = 'o'
        ms = 5
    ax.plot(df_x[group], df_y[group], marker=m, c=color, lw=0, edgecolor='k', ms=ms, edgewidth=0.5, transform=crs)

scalebar(ax, x0 - 0.9*dx, y0 + 0.7*dx, az=27.5, length=200, yoffset=20e3, xoffset=-90e3)

ax = axs[1]
dx = 50e3
x0 = 28887 - 15e3 # Offset center of image so that buoys aren't under legend
y0 = -268774 + 5e3
ax.set_extent([x0-dx, x0+dx, y0-dx, y0+dx], crs=crs)

scalebar(ax, x0 - 0.9*dx, y0 + 0.7*dx, az=82.5, length=20, yoffset=-2.7e3, xoffset=-7.5e3)

# Draw square on panel 1
axs[0].plot([x0-dx, x0-dx, x0+dx, x0+dx, x0-dx], [y0-dx, y0+dx, y0+dx, y0-dx, y0-dx], color='b', lw=0.5, transform=crs)

ax.plot(df_x[dn_buoys], df_y[dn_buoys], marker='o', c='w', lw=0, edgecolor='k', ms=4, edgewidth=0.5, transform=crs)
ax.format(lonlocator=5, latlocator=0.5)

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
# axs[0].format(title='Extended DN')
# axs[1].format(title='Distributed Network')
axs.format(abc=True)
fig.save('../figures/fig01_distributed_network_map.png', dpi=300)
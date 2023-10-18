"""Plots the zoomed in picutre with sea ice drift speed, wind speed, and MSL
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

zoom_plot_dates = ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
zoom_plot_dates = [pd.to_datetime(x) for x in zoom_plot_dates]

cusp_plot_dates = ['2020-01-31 22:00', '2020-01-31 23:00', '2020-02-01 0:00', '2020-02-01 01:00']
cusp_plot_dates = [pd.to_datetime(x) for x in cusp_plot_dates]


era5_dataloc = '../data/era5_regridded/'
buoy_dataloc = '../data/interpolated_tracks/'

# TBD add params: four dates to plot in a separate file, so that multiple figures can reference it

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

for buoy in buoy_data:
    buoy_df = buoy_data[buoy].loc[:, ['latitude', 'longitude', 'x_stere', 'y_stere']]
    buoy_df['x'] = buoy_df['x_stere']
    buoy_df['y'] = buoy_df['y_stere']
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=True, method='centered', date_index=True)
    buoy_data[buoy]['u'] = buoy_df['u']
    buoy_data[buoy]['v'] = buoy_df['v']
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=False, method='centered', date_index=True)
    buoy_data[buoy]['u_stere'] = buoy_df['u']
    buoy_data[buoy]['v_stere'] = buoy_df['v']
    
co_buoy = '2019T66'
df_lon = pd.DataFrame({buoy: buoy_data[buoy]['longitude'] for buoy in buoy_data})
df_lat = pd.DataFrame({buoy: buoy_data[buoy]['latitude'] for buoy in buoy_data})
df_x = pd.DataFrame({buoy: buoy_data[buoy]['x_stere'] for buoy in buoy_data})
df_y = pd.DataFrame({buoy: buoy_data[buoy]['y_stere'] for buoy in buoy_data})
df_u = pd.DataFrame({buoy: buoy_data[buoy]['u_stere'] for buoy in buoy_data})
df_v = pd.DataFrame({buoy: buoy_data[buoy]['v_stere'] for buoy in buoy_data})
date = '2020-02-01 00:00'
dist = np.sqrt((df_x.loc[date] - df_x.loc[date, co_buoy])**2 + 
               (df_y.loc[date] - df_y.loc[date, co_buoy])**2)
dn_buoys = list(dist[dist <= 60e3].index)

storm_track = pd.read_csv('../data/storm_track.csv', index_col=0, parse_dates=True).iloc[4:].dropna()    

##### Load ERA5 data #####
variables = ['msl', 'u10', 'v10']
savename = '2020-01-25_2020-02-05'

era5_data = {var: xr.open_dataset(era5_dataloc + 'era5_' + var + '_regridded_' + savename + '.nc') for var in variables}


# Rotate U and V (could move this into the regridding section)
u = era5_data['u10']['u10']
v = era5_data['v10']['v10']
lon = u['longitude'] - 90 # NSIDC xstere is rotated
lat = v['latitude']
ustere = u * np.cos(np.deg2rad(lon)) - v * np.sin(np.deg2rad(lon))    
vstere = u * np.sin(np.deg2rad(lon)) + v * np.cos(np.deg2rad(lon))
era5_data['u_stere'] = xr.Dataset({'u_stere': ustere})
era5_data['v_stere'] = xr.Dataset({'v_stere': vstere})
era5_data['wind_speed'] = xr.Dataset({'wind_speed': 
                            np.sqrt(ustere**2 + vstere**2)})

# Colors for buoy groups
west_buoys = ['2019P128', '2019P184', '2019P182', '2019P127']
se_buoys = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
far_se_buoys = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
l_colors = {'2019T67': 'tab:blue',
            '2019T65': 'powder blue',
            '2019S94': 'tab:green'}

# pplt.rc['title.bbox'] = True
# pplt.rc['title.bboxalpha'] = 1
pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0

fig, axs = pplt.subplots(height=6, nrows=2, ncols=2, share=True, spany=False, spanx=False)
for date, ax in zip(zoom_plot_dates, axs):
    x_dn = df_x.loc[date, co_buoy]
    y_dn = df_y.loc[date, co_buoy]
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    idx_skip = 2
    local_xu = ((X - x_dn)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y_dn)[::idx_skip, ::idx_skip])*1e-3

    local_x = (X - x_dn)*1e-3
    local_y = (Y - y_dn)*1e-3
    x_dn = x_dn*1e-3
    y_dn = y_dn*1e-3

    ax.contour(local_x, local_y, era5_data['msl'].sel(time=date)['msl']/100, color='k',
                levels=np.arange(972, 1020, 4), lw=1, labels=True, zorder=2, labels_kw = {'inline_spacing': -5})
    
    ax.quiver(local_xu, local_yv,
              era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
              era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip],
              scale=300, width=1/400, headwidth=4, color='dark gray')

    ax.format(title=date, ylabel='Y (km)', xlabel='X (km)',
          #lltitle='$P_{min}$: ' + str(int(np.round(storm_track.loc[date, 'center_mslp']/100,0))) + ' hPa',
         ylim=(-0.25e3, 0.25e3), xlim=(-0.25e3, 0.25e3),
          xticks=np.arange(-0.25e3, 0.26e3, 250), xtickminor=False, xrotation=90,
         yticks=np.arange(-0.25e3, 0.26e3, 250), ytickminor=False)
    for buoy in buoy_data:
        if date in buoy_data[buoy].index:
            z = 4
            m = 'o'
            if buoy in west_buoys:
                c = 'lilac'
            elif buoy in se_buoys:
                c = 'gold'
            elif buoy in far_se_buoys:
                c = 'orange'
            elif buoy in l_sites:
                c = l_colors[buoy]
                z = 5
                m = 'o'
            else:
                c='w'
            if buoy == '2019P22':
                c = 'gray'
            ax.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x_dn,
                    buoy_data[buoy].loc[date, 'y_stere']/1e3 - y_dn,
                    edgecolor='k', edgewidth=0.5, marker=m, facecolor=c, zorder=z)
    for color, buoy_set in zip(['lilac', 'gold', 'orange',
                                'tab:blue', 'tab:red', 'tab:green', 'gray'],
                               [west_buoys, se_buoys, far_se_buoys,
                                ['2019T67'], ['2019T65'], ['2019S94'], ['2019P22']]):
        ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
                  df_y.loc[date, buoy_set]/1e3 - y_dn,
                  df_u.loc[date, buoy_set]*100,
                  df_v.loc[date, buoy_set]*100,
                  scale=300, headwidth=4, c = 'k', # c = color if you want it to match the buoy position dots
                  zorder=6, width=1/250)
    
    ax.plot(storm_track['x_stere']/1e3 - x_dn,
            storm_track['y_stere']/1e3 - y_dn,
            color='gray', lw=1, zorder=0)

# Idea: separate color for ice drift speed, wind speed
# Possibly add the centered hourly average wind speed
ax.quiver(150,
          -180,
          20,
          0,
          scale=300, headwidth=4, c = 'b', zorder=6, width=1/250)
ax.text(75, -220, '20 m/s wind\n 20 cm/s ice', c='b')

axs.format(xreverse=False, yreverse=False, xlocator=[-250, -125, 0, 125, 250],
          ylocator=[-250, -125, 0, 125, 250])#['d', 'e','f','g'])
for ax, label in zip(axs, ['d','e','f','g']):
    ax.format(ltitle=label)

fig.save('../figures/fig06b_snapshot_drift_and_wind.jpg', dpi=300)

### Drift speed anomalies
plot_winds = False
plot_anomalies = True
    
fig, axs = pplt.subplots(height=6, nrows=2, ncols=2, share=True, spany=False, spanx=False)
for date, ax in zip(zoom_plot_dates, axs):
    x_dn = df_x.loc[date, co_buoy]
    y_dn = df_y.loc[date, co_buoy]
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    idx_skip = 2
    local_xu = ((X - x_dn)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y_dn)[::idx_skip, ::idx_skip])*1e-3

    local_x = (X - x_dn)*1e-3
    local_y = (Y - y_dn)*1e-3
    x_dn = x_dn*1e-3
    y_dn = y_dn*1e-3
    
    if plot_winds:
        ax.quiver(local_xu, local_yv,
                  era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
                  era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip],
                  scale=300, width=1/400, headwidth=4, color='dark gray')

    ax.format(title=date, ylabel='Y (km)', xlabel='X (km)',
          #lltitle='$P_{min}$: ' + str(int(np.round(storm_track.loc[date, 'center_mslp']/100,0))) + ' hPa',
         ylim=(-55, 55), xlim=(-55, 45),
          xticks=np.arange(-40, 41, 20), xtickminor=False, xrotation=90,
         yticks=np.arange(-40, 41, 20), ytickminor=False)
    for buoy in buoy_data:
        if date in buoy_data[buoy].index:
            z = 4
            m = 'o'
            if buoy in west_buoys:
                c = 'lilac'
            elif buoy in se_buoys:
                c = 'gold'
            elif buoy in far_se_buoys:
                c = 'orange'
            elif buoy in l_sites:
                c = l_colors[buoy]
                z = 5
                m = 'o'
            else:
                c='w'
            if buoy == '2019P22':
                c = 'gray'
            ax.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x_dn,
                    buoy_data[buoy].loc[date, 'y_stere']/1e3 - y_dn,
                    edgecolor='k', edgewidth=0.5, marker=m, facecolor=c, zorder=z)

    buoy_set = [buoy for buoy in buoy_data]
    if plot_anomalies:
        df_ua = df_u.loc[date, buoy_set] - df_u.loc[date, co_buoy]
        df_va = df_v.loc[date, buoy_set] - df_v.loc[date, co_buoy]
        df_u_mean = df_u.loc[date, dn_buoys].mean()
        df_v_mean = df_v.loc[date, dn_buoys].mean()
        ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
              df_y.loc[date, buoy_set]/1e3 - y_dn,
              df_ua*100,
              df_va*100,
              scale=100, headwidth=4, c = 'k', zorder=6, width=1/250)
        
    else:
        ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
              df_y.loc[date, buoy_set]/1e3 - y_dn,
              df_u.loc[date, buoy_set]*100,
              df_v.loc[date, buoy_set]*100,
              scale=200, headwidth=4, c = 'k', zorder=6, width=1/250)
    
    if plot_anomalies:
        ax.quiver(0, 0,
                  df_u_mean*100, df_v_mean*100, scale=100, headwidth=4, c='tab:red', zorder=6, width=1/150)
        v = np.sqrt(df_u_mean**2 + df_v_mean**2)*100
        ax.text(10, -50, '$\overline{U_{ice}}$: ' + str(np.round(v, 1)) + ' cm/s', c='tab:red')

for ax, label in zip(axs, ['d','e','f','g']):
    ax.format(ltitle=label)
    
if plot_winds:
    ax.quiver(74,
              -55,
              20,
              0,
              scale=400, headwidth=4, c = 'b', zorder=6, width=1/250)
    ax.text(30, -60, '20 m/s wind\n 20 cm/s ice', c='b')
    

fig.format(xreverse=False, yreverse=False)
fig.save('../figures/fig08b_snapshot_velocity_anomaly_dn.jpg', dpi=300)

# Drift speed anomalies for times near low passage
plot_winds=True
fig, axs = pplt.subplots(height=6, nrows=2, ncols=2, share=True, spany=False, spanx=False)
for date, ax in zip(cusp_plot_dates, axs):
    x_dn = df_x.loc[date, co_buoy]
    y_dn = df_y.loc[date, co_buoy]
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    idx_skip = 1
    local_xu = ((X - x_dn)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y_dn)[::idx_skip, ::idx_skip])*1e-3

    local_x = (X - x_dn)*1e-3
    local_y = (Y - y_dn)*1e-3
    x_dn = x_dn*1e-3
    y_dn = y_dn*1e-3
    
    if plot_winds:
        ax.quiver(local_xu, local_yv,
                  era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
                  era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip],
                  scale=300, width=1/400, headwidth=4, color='dark gray')

    ax.format(title=date, ylabel='Y (km)', xlabel='X (km)',
          #lltitle='$P_{min}$: ' + str(int(np.round(storm_track.loc[date, 'center_mslp']/100,0))) + ' hPa',
         ylim=(-105, 105), xlim=(-115, 95),
          xticks=np.arange(-40, 41, 20), xtickminor=False, xrotation=90,
         yticks=np.arange(-40, 41, 20), ytickminor=False)
    for buoy in buoy_data:
        if date in buoy_data[buoy].index:
            z = 4
            m = 'o'
            if buoy in west_buoys:
                c = 'lilac'
            elif buoy in se_buoys:
                c = 'gold'
            elif buoy in far_se_buoys:
                c = 'orange'
            elif buoy in l_sites:
                c = l_colors[buoy]
                z = 5
                m = 'o'
            else:
                c='w'
            if buoy == '2019P22':
                c = 'gray'
            ax.plot(buoy_data[buoy].loc[date, 'x_stere']/1e3 - x_dn,
                    buoy_data[buoy].loc[date, 'y_stere']/1e3 - y_dn,
                    edgecolor='k', edgewidth=0.5, marker=m, facecolor=c, zorder=z)

    buoy_set = [buoy for buoy in buoy_data]
    if plot_anomalies:
        df_ua = df_u.loc[date, buoy_set] - df_u.loc[date, co_buoy]
        df_va = df_v.loc[date, buoy_set] - df_v.loc[date, co_buoy]
        df_u_mean = df_u.loc[date, dn_buoys].mean()
        df_v_mean = df_v.loc[date, dn_buoys].mean()
        ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
              df_y.loc[date, buoy_set]/1e3 - y_dn,
              df_ua*100,
              df_va*100,
              scale=100, headwidth=4, c = 'k', zorder=6, width=1/250)
        
    else:
        ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
              df_y.loc[date, buoy_set]/1e3 - y_dn,
              df_u.loc[date, buoy_set]*100,
              df_v.loc[date, buoy_set]*100,
              scale=200, headwidth=4, c = 'k', zorder=6, width=1/250)
    
    if plot_anomalies:
        ax.quiver(0, 0,
                  df_u_mean*100, df_v_mean*100, scale=100, headwidth=4, c='tab:red', zorder=6, width=1/150)
        v = np.sqrt(df_u_mean**2 + df_v_mean**2)*100
        ax.text(10, -50, '$\overline{U_{ice}}$: ' + str(np.round(v, 1)) + ' cm/s', c='tab:red')

for ax, label in zip(axs, ['d','e','f','g']):
    ax.format(ltitle=label)
    
if plot_winds:
    ax.quiver(74,
              -55,
              20,
              0,
              scale=400, headwidth=4, c = 'b', zorder=6, width=1/250)
    ax.text(30, -60, '20 m/s wind\n 20 cm/s ice', c='b')
    

fig.format(xreverse=False, yreverse=False)
fig.save('../figures/fig0XX_snapshot_velocity_anomaly_dn.jpg', dpi=300)
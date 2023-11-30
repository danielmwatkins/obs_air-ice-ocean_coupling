"""Plots for analyzing the sudden changes in direction. Should split into parts that produce a dataframe and parts that do the plotting."""
import pandas as pd
import numpy as np
import proplot as pplt
import os
import sys
sys.path.append('../scripts/')
import drifter
import xarray as xr

l_co_sites = {'L1': '2019T67', # L1 / T67 / asfs 40
           'L2': '2019T65', # L2 / T65 / asfs 30
           'L3': '2019S94', # L3 / S94 / asfs 50
           'Met City': '2019T66'}
ts = slice('2020-01-30 00:00', '2020-02-02 00:00')
dataloc = '../data/interpolated_tracks/'



files = os.listdir(dataloc)
files = [f for f in files if f != '.DS_Store']


#### MOSAIC buoys #####
buoy_data = {}
for f in files:
    buoy = f.split('.')[0].split('_')[-1]
    buoy_data[buoy] = pd.read_csv(dataloc + f, parse_dates = True, index_col=0)
    buoy_data[buoy] = buoy_data[buoy].loc[:, ['latitude', 'longitude', 'x_stere', 'y_stere', 'u', 'v']]
    lon = buoy_data[buoy]['longitude'] - 90 # Rotated stereographic
    lat = buoy_data[buoy]['latitude']
    u = buoy_data[buoy]['u']
    v = buoy_data[buoy]['v']
    buoy_data[buoy]['u_stere'] = u * np.cos(np.deg2rad(lon)) - v * np.sin(np.deg2rad(lon))    
    buoy_data[buoy]['v_stere'] = u * np.sin(np.deg2rad(lon)) + v * np.cos(np.deg2rad(lon))
DN = []
date0 = pd.to_datetime('2020-02-01 00:00')
x0 = buoy_data['2019T66'].loc[date0, 'x_stere']
y0 = buoy_data['2019T66'].loc[date0, 'y_stere']

for buoy in buoy_data:
    if date0 in buoy_data[buoy].index:
        xs = np.round(buoy_data[buoy].loc[date0, 'x_stere']  - x0, -2)/1e3
        ys = np.round(buoy_data[buoy].loc[date0, 'y_stere']  - y0, -2)/1e3
        if np.sqrt(xs**2 + ys**2) < 65:
            DN.append(buoy)
#### Met station data #####
df_l2 = pd.read_csv('../../data/met_data/asfs30.csv', index_col=0, parse_dates=True)
df_l1 = pd.read_csv('../../data/met_data/asfs40.csv', index_col=0, parse_dates=True)
df_l3 = pd.read_csv('../../data/met_data/asfs50.csv', index_col=0, parse_dates=True)
df_co = pd.read_csv('../../data/met_data/metcity.csv', index_col=0, parse_dates=True)
df_co = df_co.loc[~df_co.index.duplicated()]


l_co_data = {'L1': df_l1.resample('30min').asfreq(),
             'L2': df_l2.resample('30min').asfreq(),
             'L3': df_l3.resample('30min').asfreq(),
             'Met City': df_co.resample('30min').asfreq()}

l_co_data['Met City'].rename(
            {'wspd_u_mean_10m': 'u_wind',
             'wspd_v_mean_10m': 'v_wind'}, axis=1, inplace=True)

for site in ['L1', 'L2', 'L3']:
    l_co_data[site].rename({'wspd_u_mean': 'u_wind',
                            'wspd_v_mean': 'v_wind'}, axis=1, inplace=True)

#### ERA5 data ######
ds_u10 = xr.open_dataset('../data/era5_regridded/era5_u10_regridded_2020-01-25_2020-02-05.nc')
ds_v10 = xr.open_dataset('../data/era5_regridded/era5_v10_regridded_2020-01-25_2020-02-05.nc')
ds_slp = xr.open_dataset('../data/era5_regridded/era5_msl_regridded_2020-01-25_2020-02-05.nc')
u = ds_u10['u10']
v = ds_v10['v10']
lon = u['longitude'] - 90 # Rotated stereographic
lat = v['latitude']
ustere = u * np.cos(np.deg2rad(lon)) - v * np.sin(np.deg2rad(lon))    
vstere = u * np.sin(np.deg2rad(lon)) + v * np.cos(np.deg2rad(lon))
xgrid = ds_u10.x_stere[0,:].data
ygrid = ds_u10.y_stere[:,0].data
ds_u10_stere = xr.Dataset({'u_stere': (('time', 'y', 'x'), ustere.data)},
                         coords={'x': (('x',), xgrid),
                                'y': (('y',), ygrid),
                                'time': ustere.time.data})
ds_v10_stere = xr.Dataset({'v_stere': (('time', 'y', 'x'), vstere.data)},
                         coords={'x': (('x',), xgrid),
                                'y': (('y',), ygrid),
                                'time': vstere.time.data})

df_x = pd.DataFrame({buoy: buoy_data[buoy]['x_stere'].resample('1H').asfreq() for buoy in buoy_data})
df_y = pd.DataFrame({buoy: buoy_data[buoy]['y_stere'].resample('1H').asfreq() for buoy in buoy_data})
df_u = pd.DataFrame(np.nan, columns=df_x.columns, index=df_x.index)
df_v = pd.DataFrame(np.nan, columns=df_x.columns, index=df_x.index)
for date in df_u.index:
    
    x = xr.DataArray(df_x.loc[date,:], dims="z")
    y = xr.DataArray(df_y.loc[date, :], dims="z")
    u = ds_u10_stere.sel(time=date)['u_stere'].interp(
        {'x': x,
         'y': y}, method='linear').data
    v = ds_v10_stere.sel(time=date)['v_stere'].interp(
        {'x': x,
         'y': y}, method='linear').data
    df_u.loc[date,:] = u
    df_v.loc[date,:] = v

for buoy in buoy_data:
    buoy_data[buoy]['u_stere_era5'] = df_u[buoy]
    buoy_data[buoy]['v_stere_era5'] = df_v[buoy]    
    buoy_data[buoy]['era5_windspeed'] = np.sqrt(buoy_data[buoy]['u_stere_era5']**2  + buoy_data[buoy]['v_stere_era5']**2)
    buoy_data[buoy]['speed'] = np.sqrt( buoy_data[buoy]['u']**2 +  buoy_data[buoy]['v']**2)

for site in l_co_data:
    l_co_data[site] = l_co_data[site].where(np.abs(l_co_data[site].u_wind) < 50).loc[ts]
    buoy = l_co_sites[site]
    df = buoy_data[buoy].copy()
    
    df = df.merge(l_co_data[site].loc[:, ['u_wind', 'v_wind']], left_index=True, right_index=True)
    u = df['u_wind']
    v = df['v_wind']
    lon = df['longitude'] - 90
    df['u_stere_wind'] =  u * np.cos(np.deg2rad(lon)) -  v * np.sin(np.deg2rad(lon))
    df['v_stere_wind'] =  u * np.sin(np.deg2rad(lon)) +  v * np.cos(np.deg2rad(lon))
    df['wind_speed'] = np.sqrt(u**2 + v**2)
    l_co_data[site] = df.copy()


check_A = slice('2020-01-30 12:00', '2020-01-31 12:00')
check_B = slice('2020-01-31 12:00', '2020-02-01 12:00')

speed_min_a = {}
speed_min_b = {}
xa = {}
ya = {}
xb = {}
yb = {}
for buoy in DN:
    speed_min_a[buoy] = buoy_data[buoy].loc[check_A].speed.idxmin()
    xa[buoy] = buoy_data[buoy].loc[speed_min_a[buoy], 'x_stere']
    ya[buoy] = buoy_data[buoy].loc[speed_min_a[buoy], 'y_stere']
    speed_min_b[buoy] = buoy_data[buoy].loc[check_B].speed.idxmin()
    xb[buoy] = buoy_data[buoy].loc[speed_min_b[buoy], 'x_stere']
    yb[buoy] = buoy_data[buoy].loc[speed_min_b[buoy], 'y_stere']

speed_min = pd.DataFrame({'time_a': speed_min_a,
                          'x_stere_a': xa,
                          'y_stere_a': ya,
                          'offset_a': (pd.Series(speed_min_a) - pd.to_datetime('2020-01-31 00:00')).dt.total_seconds()/3600,
                          'time_b': speed_min_b,
                          'x_stere_b': xb,
                          'y_stere_b': yb,
                          'offset_b': (pd.Series(speed_min_b) - pd.to_datetime('2020-02-01 00:00')).dt.total_seconds()/3600})


ts = slice('2020-01-30 12:00', '2020-02-01 12:00')
fig, axs = pplt.subplots(ncols=4, nrows=1, share=False, aspect=1, width=10)
for ax, site in zip(axs, l_co_data):

    df = l_co_data[site].copy().resample('1H').asfreq()
    df['x_stere'] /= 1e3
    df['y_stere'] /= 1e3
    
    xmin = df['x_stere'].min()
    xmax = df['x_stere'].max()
    ymin = df['y_stere'].min()
    ymax = df['y_stere'].max()
    dy = 10.5
    dx = 3.5
    y0 = 0.5*(ymax + ymin)
    x0 = 0.5*(xmax + xmin)
    
    ax.quiver(df.x_stere, df.y_stere, df.u_stere, df.v_stere, scale=2, label='Ice Drift', zorder=3)
    ax.quiver(df.x_stere, df.y_stere, df.u_stere_era5*0.02, df.v_stere_era5*0.02, scale=2, color='steelblue', label='ERA5 Wind')
    ax.quiver(df.x_stere, df.y_stere, df.u_stere_wind*0.02, df.v_stere_wind*0.02, scale=2, color='light blue', label='Observed Wind', )

    date1 = speed_min.loc[l_co_sites[site],'time_a']
    date2 = speed_min.loc[l_co_sites[site],'time_b']
    for date, label in zip([date1, date2],['A', 'B']):
        x = l_co_data[site].loc[date, 'x_stere'] / 1e3
        y = l_co_data[site].loc[date, 'y_stere']/1e3
        ax.plot(x,  y, color='r', marker='.')
        ax.text(x + 0.25,  y, label, color='r')

   
    ax.format(yreverse=False, xreverse=False, xlabel='X coordinate (km)', ylabel='Y coordinate (km)', xlocator=2, ylocator=2,
              ultitle=site, ylim=(y0-dy, y0+dy), xlim=(x0-dx, x0+dx),
              lrtitle='A: ' + date1.strftime('%m/%d %H:%M') + '\n' + \
                      'B: ' + date2.strftime('%m/%d %H:%M'), abc=True)
axs[2].legend(loc='cr', ncols=1)
fig.save('../figures/fig06_co_lsites_drift_wind_cusp.jpg', dpi=300)
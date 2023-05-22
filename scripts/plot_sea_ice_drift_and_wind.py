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

era5_dataloc = '../../../data/era5/'
buoy_dataloc = '../../../data/interpolated_tracks//'

##### Load buoy data #####
buoy_data = {}
metadataloc = '../../../data/adc_dn_tracks/'
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
    buoy_df = drifter.compute_velocity(buoy_df, rotate_uv=False, method='centered', date_index=True)
    buoy_data[buoy]['u_stere'] = buoy_df['u']
    buoy_data[buoy]['v_stere'] = buoy_df['v']
    

df_lon = pd.DataFrame({buoy: buoy_data[buoy]['longitude'] for buoy in buoy_data})
df_lat = pd.DataFrame({buoy: buoy_data[buoy]['latitude'] for buoy in buoy_data})
df_x = pd.DataFrame({buoy: buoy_data[buoy]['x_stere'] for buoy in buoy_data})
df_y = pd.DataFrame({buoy: buoy_data[buoy]['y_stere'] for buoy in buoy_data})
df_u = pd.DataFrame({buoy: buoy_data[buoy]['u_stere'] for buoy in buoy_data})
df_v = pd.DataFrame({buoy: buoy_data[buoy]['v_stere'] for buoy in buoy_data})

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
west_buoys = ['2019P128', '2019P184', '2019P182', '2019P127']
se_buoys = ['2019P155', '2019P123', '2019P112', '2019P113', '2019P114', '2019P22', '2019P119']
far_se_buoys = ['2019P156', '2019P157']
l_sites = ['2019T67', '2019T65', '2019S94']
l_colors = {'2019T67': 'tab:blue',
            '2019T65': 'tab:red',
            '2019S94': 'tab:green'}

pplt.rc['title.bbox'] = True
pplt.rc['title.bboxalpha'] = 1
pplt.rc['xtick.major.width'] = 0
pplt.rc['ytick.major.width'] = 0

fig, axs = pplt.subplots(height=4, nrows=1, ncols=4, share=True, spany=False)
# these values are centered on the storm track
zoom_plot_dates =  ['2020-01-31 16:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
zoom_plot_dates = [pd.to_datetime(x) for x in zoom_plot_dates]
for date, ax in zip(zoom_plot_dates, axs):
    x_dn = df_x.loc[date, '2019T66']/1e3
    y_dn = df_y.loc[date, '2019T66']/1e3
    x0 = storm_track.loc[date, 'x_stere'] # replace with storm track
    y0 = storm_track.loc[date, 'y_stere']
    X = era5_data['msl']['x_stere'].data
    Y = era5_data['msl']['y_stere'].data
    idx_skip = 2
    local_xu = ((X - x0)[::idx_skip, ::idx_skip])*1e-3
    local_yv = ((Y - y0)[::idx_skip, ::idx_skip])*1e-3

    local_x = (X - x0)*1e-3
    local_y = (Y - y0)*1e-3


    ax.contour(local_x, local_y, era5_data['msl'].sel(time=date)['msl']/100, color='k',
                levels=np.arange(972, 1020, 4), lw=1, labels=True, zorder=2)
    
    ax.quiver(local_xu, local_yv,
              era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
              era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip], scale=400)

    ax.format(title=date, ylabel='Y (km)', xlabel='X (km)',
          #lltitle='$P_{min}$: ' + str(int(np.round(storm_track.loc[date, 'center_mslp']/100,0))) + ' hPa',
         ylim=(-0.2e3, 0.5e3), xlim=(-0.2e3, 0.5e3),
          xticks=np.arange(-0.25e3, 0.26e3, 250), xtickminor=False, xrotation=90,
         yticks=np.arange(-0.25e3, 0.26e3, 250), ytickminor=False)
    for buoy in buoy_data:
        if date in buoy_data[buoy].index:
            z = 1
            m = '.'
            if buoy in west_buoys:
                c = 'lilac'
            elif buoy in se_buoys:
                c = 'gold'
            elif buoy in far_se_buoys:
                c = 'orange'
            elif buoy in l_sites:
                c = l_colors[buoy]
                z = 5
                m = '.'
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
                  scale=400, headwidth=4, c = color, zorder=6, width=1/250)

    ax.plot(storm_track['x_stere']/1e3 - storm_track.loc[date, 'x_stere']/1e3,
            storm_track['y_stere']/1e3 - storm_track.loc[date, 'y_stere']/1e3,
            color='gray', lw=1, zorder=0)

ax.quiver(325,
          -100,
          20,
          0,
          scale=400, headwidth=4, c = 'b', zorder=6, width=1/250)
ax.text(250, -175, '20 m/s wind\n20 cm/s ice', c='b')
fig.format(xreverse=False, yreverse=False, abc=True)
fig.save('../figures/janfeb_storm_zoom_buoys.jpg', dpi=300)
"""Scripts for creating Figure 7, the velocity time series and the overview maps with wind speeds

To-do items
- Site specs and array info needs to be in the array_info.csv
- L-sites should be marked as squares from that array


"""

import xarray as xr
import os
import numpy as np
import proplot as pplt
import pandas as pd
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import metpy.calc as mcalc
from metpy.units import units
import sys
import drifter

dataloc = '../data/interpolated_tracks/'
era5_dataloc = '../data/era5_regridded/'

zoom_plot_dates_A= ['2020-01-31 18:00', '2020-02-01 0:00', '2020-02-01 06:00', '2020-02-01 12:00']
zoom_plot_dates_A = [pd.to_datetime(x) for x in zoom_plot_dates_A]

zoom_plot_dates_B = ['2020-01-30 05:00', '2020-01-30 11:00', '2020-01-30 18:00', '2020-01-31 04:00']
zoom_plot_dates_B = [pd.to_datetime(x) for x in zoom_plot_dates_B]


cusp_plot_dates = ['2020-01-31 22:00', '2020-01-31 23:00', '2020-02-01 0:00', '2020-02-01 01:00']
cusp_plot_dates = [pd.to_datetime(x) for x in cusp_plot_dates]

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

array_info = pd.read_csv('../data/array_info.csv')
array_info = {array: group.set_index('buoyID') for array, group in array_info.groupby('array_name')}
array_info['DN_5']['line_style'] = [(1, (4, 1, 1, 1, 1, 1))]*len(array_info['DN_5'])
array_info['l_sites']['color'] = 'tab:blue'
array_info['l_sites']['line_width'] = 1.5


##### Velocity time series plots ########
ts_A = slice('2020-01-30 20:00', '2020-02-02 02:00')
ts_B = slice('2020-01-29 18:00', '2020-02-01 00:00')

for ts, dates, title in zip([ts_A, ts_B], [zoom_plot_dates_A, zoom_plot_dates_B],
                    ['../figures/fig07a_velocity_timeseries_ice_stereographic_uv.png',
                     '../figures/figS1a_velocity_timeseries_ice_stereographic_uv.png']):
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



    for abc, date in zip(['d', 'e', 'f', 'g'], dates):
        for ax in axs:
            ax.axvline(date, color='tab:blue', lw=0.5, zorder=0)

        axs[0].text(date + pd.to_timedelta('30min'), 0.3, abc, color='tab:blue', zorder=4)
        axs[1].text(date + pd.to_timedelta('30min'), 0.3, abc, color='tab:blue', zorder=4)
        axs[2].text(date + pd.to_timedelta('30min'), 0.525, abc, color='tab:blue', zorder=4)

    axs[0].format(ylim=(-0.6, 0.4))
    axs[1].format(ylim=(-0.6, 0.4))
    axs[2].format(ylim=(0, 0.6))
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

    fig.save(title, dpi=300)

#### Next plot the maps

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
variables = ['msl', 'u10', 'v10', 'u_950', 'v_950']
savename = '2020-01-25_2020-02-05'

era5_data = {var: xr.open_dataset(era5_dataloc + 'era5_' + var + '_regridded_' + savename + '.nc') for var in variables}
era5_data['950_wind_speed'] = xr.Dataset({'wind_speed': 
                            np.sqrt(era5_data['u_950']['u_950']**2 + era5_data['v_950']['v_950']**2)})



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

for dates, filename in zip([zoom_plot_dates_A, zoom_plot_dates_B, cusp_plot_dates], 
                               ['../figures/fig07b_snapshot_drift_and_wind.png',
                                '../figures/figS1b_snapshot_drift_and_wind.png',
                                '../figures/figSX_snapshot_drift_and_wind_analysis.png']):
    fig, axs = pplt.subplots(height=6, nrows=2, ncols=2, share=True, spany=False, spanx=False)
    for date, ax in zip(dates, axs):
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
        wind_color = 'sea green'
        
        ax.contour(local_x, local_y, era5_data['950_wind_speed'].sel(time=date)['wind_speed'],
                   color=[wind_color], ls='--', levels=[16], zorder=4, labels=False)
        ax.contour(local_x, local_y, era5_data['950_wind_speed'].sel(time=date)['wind_speed'],
                   color=[wind_color], levels=[20], zorder=4, labels=False)



        ax.quiver(local_xu, local_yv,
                  era5_data['u_stere'].sel(time=date)['u_stere'][::idx_skip, ::idx_skip],
                  era5_data['v_stere'].sel(time=date)['v_stere'][::idx_skip, ::idx_skip],
                  scale=300, width=1/400, headwidth=4, color='tab:blue')
    
        ax.format(title=date.strftime('%y-%m-%d %H:%M'), ylabel='Y (km)', xlabel='X (km)',
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
                      scale=300, headwidth=4, c = 'k',
                      zorder=6, width=1/250)
        if 'XX' in filename:
            buoy_set = dn_buoys
            ax.quiver(df_x.loc[date, buoy_set]/1e3  - x_dn,
                      df_y.loc[date, buoy_set]/1e3 - y_dn,
                      df_u.loc[date, buoy_set]*100,
                      df_v.loc[date, buoy_set]*100,
                      scale=300, headwidth=4, c = 'k',
                      zorder=6, width=1/250)            
        
#         ax.plot(storm_track['x_stere']/1e3 - x_dn,
#                 storm_track['y_stere']/1e3 - y_dn,
#                 color='gray', lw=1, zorder=0)
        
    # Idea: separate color for ice drift speed, wind speed
    # Possibly add the centered hourly average wind speed
    ax.quiver(45,
              -210,
              20,
              0,
              scale=300, headwidth=4, c = 'tab:blue', zorder=6, width=1/250)
    ax.quiver(45,
              -230,
              20,
              0,
              scale=300, headwidth=4, c = 'k', zorder=6, width=1/250)
    ax.text(90, -220, '20 m/s wind', c='tab:blue', zorder=6)
    ax.text(90, -240, '20 cm/s ice', c='k', zorder=6)
    rec = Rectangle((35, -250), 250-35, 60, ) 
    pc = PatchCollection([rec], facecolor='w', alpha=1,
                             edgecolor='k', zorder=5)
    ax.add_collection(pc)
    
    # Generate legend manually for finer control
    h, l = [], []
    for c, ls, label in zip(['k', wind_color, wind_color],
                        ['-', '--', '-'],
                        ['SLP (hPa)', '16 m/s wind', '20 m/s wind']):
        if label == 'SLP (hPa)':
            lw = 1
        else:
            lw = 2
        h.append(ax.plot([],[],color=c,  ls=ls, lw=lw))
        l.append(label)        
    axs[0].legend(h, l, loc='ur', ncols=1)    
    
    axs.format(xreverse=False, yreverse=False, xlocator=[-250, -125, 0, 125, 250], xrotation=89.99, # Weird bug - at 90, only some of the xlabels rotate
              ylocator=[-250, -125, 0, 125, 250])
    for ax, label in zip(axs, ['d','e','f','g']):
        ax.format(ltitle=label)
    
    fig.save(filename, dpi=300)


"""Based on this stackoverflow response: https://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python"""
import sys
from PIL import Image

def merge_images(files, savename):
    """Concatenates images horizontally"""
    images = [Image.open(x) for x in files]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGB', (total_width, max_height))
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    
    new_im.save(savename)


# Fig 6: Velocity
merge_images(['../figures/fig07a_velocity_timeseries_ice_stereographic_uv.png',
             # '../figures/fig07b_snapshot_drift_and_wind.jpg',
             '../figures/collaborators/Fig7d_g_frontal_isotach_analysis.png'],
             '../figures/fig07_velocity.png')

merge_images(['../figures/figS1a_velocity_timeseries_ice_stereographic_uv.png',
              '../figures/figS1b_snapshot_drift_and_wind.png'],
             '../figures/figS1_velocity.png')

